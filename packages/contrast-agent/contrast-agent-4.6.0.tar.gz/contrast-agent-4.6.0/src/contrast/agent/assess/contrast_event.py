# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import inspect
import threading

from contrast.extern import six

from contrast.agent.policy.constants import (
    ALL_ARGS,
    ALL_KWARGS,
    OBJECT,
    RETURN,
    TRIGGER_TYPE,
    CREATION_TYPE,
)
from contrast.agent.assess.utils import get_properties
from contrast.agent.settings_state import SettingsState
from contrast.api.dtm_pb2 import (
    ParentObjectId,
    TraceEvent,
    TraceEventObject,
    TraceEventSource,
    TraceStack,
)
from contrast.utils.assess.tracking_util import recursive_is_tracked
from contrast.utils.base64_utils import base64_encode
from contrast.utils.decorators import fail_quietly
from contrast.utils.object_utils import safe_copy
from contrast.utils.stack_trace_utils import StackTraceUtils
from contrast.utils.string_utils import protobuf_safe
from contrast.utils.timer import Timer
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class ContrastEvent(object):
    """
    This class holds the data about an event in the application
    We'll use it to build an event that TeamServer can consume if
    the object to which this event belongs ends in a trigger.
    """

    ATOMIC_ID = 0
    ELLIPSIS = "..."
    UNTRUNCATED_PORTION_LENGTH = 25
    TRUNCATION_LENGTH = (UNTRUNCATED_PORTION_LENGTH * 2) + len(ELLIPSIS)
    INITIALIZERS = ("__init__", "__new__")
    NONE_STRING = str(None)

    TRACE_EVENT_TYPE_MAP = {"METHOD": 0, "PROPAGATOR": 1, "TAGGER": 2, "TAG": 2}

    def __init__(
        self,
        node,
        tagged,
        self_obj,
        ret,
        args,
        kwargs,
        parent_ids,
        possible_key,
        source_type=None,
        source_name=None,
        frame=None,
    ):
        self.time = Timer.now_ms()

        self.node = node
        self.event_action = self.node.build_action()

        if self._should_get_stack:
            self._stack_trace = _populate_stack_trace()
            self.caller = self._stack_trace[0] if self._stack_trace else None
            self.frameinfo = _getframeinfo(frame)
        else:
            self._stack_trace = []
            self.caller = None
            self.frameinfo = None

        self.thread = threading.current_thread().ident

        self.source_type = source_type
        self.source_name = source_name

        self.event_id = ContrastEvent._atomic_id()
        self.parent_ids = parent_ids

        self.possible_key = possible_key

        self.obj = self_obj
        self.ret = ret
        self.args = safe_copy(args)
        self.kwargs = safe_copy(kwargs)

        self.taint_location = None
        self._update_method_information(tagged)

    def to_dtm_event(self):
        event = TraceEvent()

        event.type = self.TRACE_EVENT_TYPE_MAP.get(self.node.node_type, 1)
        event.action = self.event_action
        event.timestamp_ms = self.time
        event.thread = str(self.thread)

        self._build_event_objects(event)

        self._convert_frameinfo(event)

        for frame in self._stack_trace:
            _convert_stack_frame_element(frame, event)

        safe_source_name = protobuf_safe(self.source_name)
        event.field_name = safe_source_name

        if self.source_type:
            event.event_sources.extend([self.build_source_event(safe_source_name)])

        event.object_id = int(self.event_id)

        if self.parent_ids:
            for parent_id in self.parent_ids:
                parent = ParentObjectId()
                parent.id = parent_id
                event.parent_object_ids.extend([parent])

        self._build_complete_signature(event)
        self._validate_event(event)

        return event

    def build_source_event(self, safe_source_name):
        """
        Create a new TraceEventSource

        :param safe_source_name: source name or empty string
        :return: TraceEvenSource
        """
        trace_event_source = TraceEventSource()

        trace_event_source.type = self.source_type
        trace_event_source.name = safe_source_name

        return trace_event_source

    @property
    def _should_get_stack(self):
        """
        Determine if event.stack should be populated or not.

        Get stacktrace for the event EXCEPT if
          1. assess.stacktraces is configured to NONE
          2. assess.stacktraces is configured to SOME and event action is not
                creation or trigger

        :return: bool if to get stacktrace
        """
        settings = SettingsState()

        reportable_actions = (
            TraceEvent.Action.Value(CREATION_TYPE),
            TraceEvent.Action.Value(TRIGGER_TYPE),
        )

        if settings.config.get("assess.stacktraces") == "NONE" or (
            settings.config.get("assess.stacktraces") == "SOME"
            and self.event_action not in reportable_actions
        ):
            return False

        return True

    @classmethod
    def _atomic_id(cls):
        ret = cls.ATOMIC_ID

        cls.ATOMIC_ID += 1

        return ret

    def _update_method_information(self, tagged):
        """
        For nicer reporting, we lie about the tagged value. For example, a call to
        split() returns a list of strings: ["foo", "bar"]. In the properties for "foo",
        the split event shows a return value of only "foo" instead of the whole list.
        """
        self.taint_location = self._find_taint_location()

        if self.taint_location is None:
            # This would be for trigger nodes without source or target. Trigger rule was
            # violated simply by a method being called. We'll save all the information,
            # but nothing will be marked up, as nothing need be tracked.
            return

        if self.taint_location == OBJECT:
            self.obj = tagged
            return

        if self.taint_location == RETURN:
            self.ret = tagged
            return

    def _add_taint_ranges(self, event, target, splat):
        """
        Populate event.taint_ranges
        """
        if self.taint_location is None:
            return

        if isinstance(target, dict):
            if self.taint_location == ALL_KWARGS and self.possible_key:
                properties = get_properties(target.get(self.possible_key, None))
            else:
                properties = get_properties(target.get(self.taint_location, None))
        else:
            properties = get_properties(target)

        if properties is None:
            return

        if splat is not None:
            tag_ranges = properties.tags_to_dtm(splat_range=(0, splat))
        else:
            tag_ranges = properties.tags_to_dtm()

        event.taint_ranges.extend(tag_ranges)

    def _build_event_args(self, event):
        for index, arg in enumerate(self.args):
            is_taint_target = self.taint_location == index

            trace_object = TraceEventObject()
            splat = self._build_event_object(trace_object, arg, not is_taint_target)
            event.args.extend([trace_object])
            if is_taint_target:
                self._add_taint_ranges(event, arg, splat)

    def _build_event_objects(self, event):
        """
        Populate event.source and event.target
        Populate fields of event.object and event.ret which are TraceEventObject
        """
        self._set_event_source_and_target(event)

        objects = [
            (event.object, self.obj, OBJECT),
            (event.ret, self.ret, RETURN),
        ]

        for event_obj, obj, key in objects:
            is_taint_target = self.taint_location == key
            splat = self._build_event_object(event_obj, obj, not is_taint_target)
            if is_taint_target:
                self._add_taint_ranges(event, obj, splat)

        self._build_event_args(event)
        self._build_event_kwargs(event)

    def _build_event_kwargs(self, event):
        if self.kwargs:
            trace_object = TraceEventObject()
            splat = self._build_event_object(trace_object, self.kwargs, True)
            event.args.extend([trace_object])
            if self.taint_location is ALL_KWARGS or isinstance(
                self.taint_location, six.string_types
            ):
                self._add_taint_ranges(event, self.kwargs, splat)

    def _validate_event(self, event):
        """
        TS is not able to render a vulnerability correctly if the source string index 0
        of the trigger event, ie event.source, is not a known one.

        See TS repo DataFlowSnippetBuilderVersion1.java:buildMarkup

        :param event: TraceEvent
        :return: None
        """
        allowed_trigger_sources = ["O", "P", "R"]
        if (
            event.action == TraceEvent.Action.Value(TRIGGER_TYPE)
            and event.source[0] not in allowed_trigger_sources
        ):
            # If this is logged, check the node in policy.json corresponding to
            # this event and how the agent has transformed the source string
            logger.debug("WARNING: trigger event TS-invalid source %s", event.source)

    def _build_event_object(self, event_object, self_obj, truncate):
        obj_string, splat = _obj_to_str(self_obj)

        if truncate and len(obj_string) > self.TRUNCATION_LENGTH:
            temp = [
                obj_string[0 : self.TRUNCATION_LENGTH],
                self.ELLIPSIS,
                obj_string[
                    len(obj_string)
                    - self.UNTRUNCATED_PORTION_LENGTH : self.UNTRUNCATED_PORTION_LENGTH
                ],
            ]

            obj_string = "".join(temp)

        event_object.value = base64_encode(obj_string)
        event_object.tracked = recursive_is_tracked(self_obj)

        return len(obj_string) if splat else None

    def _build_complete_signature(self, event):
        return_type = type(self.ret).__name__ if self.ret else self.NONE_STRING

        event.signature.return_type = return_type
        # We don't want to report "BUILTIN" as a module name in Team Server
        event.signature.class_name = self.node.location.replace("BUILTIN.", "")
        event.signature.method_name = self.node.method_name

        if self.args:
            for item in self.args:
                arg_type = type(item).__name__ if item else self.NONE_STRING
                event.signature.arg_types.append(arg_type)

        if self.kwargs:
            arg_type = type(self.kwargs).__name__
            event.signature.arg_types.append(arg_type)

        event.signature.constructor = self.node.method_name in self.INITIALIZERS

        # python always returns None if not returned
        event.signature.void_method = False

        if not self.node.instance_method:
            event.signature.flags = 8

    def _find_taint_location(self):
        """
        Based on what we know about the call that caused this event's creation,
        determine the appropriate taint location. Fall back to returning the
        first element in candidate_taint_locations. This method is greedy, so it
        will return the first valid taint location based on the order of candidate
        locations provided.

        Example:

        args = ("irrelevant string",)
        kwargs = {"irrelevant_key": "irrelevant_value", "important_key": "user_input"}
        candidate_taint_locations = [1, 2, "important_key"]

        In this case, we return "important_key" since there is no ARG_1 or ARG_2.

        @return: The appropriate element of candidate_taint_locations, or the first
            element if no suitable matches are found, or None if the list is empty.
        """
        candidate_taint_locations = self.node.targets or self.node.sources

        if not candidate_taint_locations:
            return None

        for candidate_location in candidate_taint_locations:
            found = (
                (candidate_location == RETURN)
                or (candidate_location == OBJECT and self.obj is not None)
                or (candidate_location == ALL_ARGS and self.args)
                or (candidate_location == ALL_KWARGS and self.kwargs)
                or (
                    isinstance(candidate_location, int)
                    and candidate_location < len(self.args)
                )
                or (
                    isinstance(candidate_location, six.string_types)
                    and candidate_location in self.kwargs
                )
            )
            # pylint doesn't like this in an if statement, but an assignment is ok
            if found:
                return candidate_location

        logger.debug(
            "WARNING: unable to find event taint location: %s %s %s %s %s",
            self.obj,
            self.ret,
            self.args,
            self.kwargs,
            candidate_taint_locations,
        )
        return candidate_taint_locations[0]

    def _set_event_source_and_target(self, event):
        """
        We have to do a little work to figure out what our TS appropriate
        target is. To break this down, the logic is as follows:
        1) If my node has a target, work on targets. Else, work on sources.
           Per TS law, each node must have at least a source or a target.
           The only type of node w/o targets is a Trigger, but that may
           change.
        2) I'll set the event's source and target to TS values.
        """
        if self.node.targets:
            event.source = self.node.ts_valid_source
            event.target = self.node.ts_valid_target
        elif self.node.sources:
            event.source = self.node.ts_valid_target or self.node.ts_valid_source

    def _convert_frameinfo(self, event):
        """
        Used to convert actual python frame object
        """
        if not self.frameinfo:
            return

        stack = TraceStack()
        stack.line_number = self.frameinfo.lineno

        stack.method_name = protobuf_safe(self.node.method_name)
        stack.declaring_class = protobuf_safe(self.frameinfo.filename)
        stack.file_name = protobuf_safe(self.frameinfo.filename)
        event.stack.extend([stack])


@fail_quietly("Failed to populate stack trace for event", return_value=[])
def _populate_stack_trace():
    return StackTraceUtils.build(ignore=True, depth=20, for_trace=True)


@fail_quietly("Failed to get frameinfo for event")
def _getframeinfo(frame):
    return inspect.getframeinfo(frame) if frame is not None else frame


def _convert_stack_frame_element(frame, event):
    """
    Used to convert a dtm StackFrameElement to a TraceStack

    protobuf_safe(frame.declaring_class)
    """
    frame.declaring_class = frame.file_name

    file_name = protobuf_safe(frame.file_name)

    frame.file_name = file_name

    event.stack.extend([frame])


def _obj_to_str(self_obj):
    """
    Attempt to get a string representation of an object

    Right now we do our best to decode the object, but we handle any
    decoding errors by replacing with �. This technically is a loss
    of information when presented in TS, but it allows us to preserve
    the taint range information, which arguably is more important for
    Assess. In the future we might want to implement more robust
    handling of non-decodable binary data (i.e. to display escaped
    data with an updated taint range).

    If the object isn't stringy, then just return the string
    representation. In this case, we will need to splat the displayed
    taint range since we're not able to map tag ranges.

    :param self_obj: any python object, str, byte, bytearray, etc
    :return:
        1. str representing the object
        2. whether to splat the taint ranges or not, depending on if we can stringify
           the obj
    """
    splat = False

    try:
        if isinstance(self_obj, bytearray):
            obj_string = self_obj.decode(errors="replace")
        else:
            obj_string = six.ensure_str(self_obj, errors="replace")
    except TypeError:
        obj_string = str(self_obj)
        splat = True

    return obj_string, splat
