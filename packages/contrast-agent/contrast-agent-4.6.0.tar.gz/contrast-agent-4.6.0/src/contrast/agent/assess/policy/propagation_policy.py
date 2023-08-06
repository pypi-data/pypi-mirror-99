# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import iteritems, PY2, PY3

import contrast
from contrast.agent.assess.contrast_event import ContrastEvent
from contrast.agent.policy.loader import Policy
from contrast.agent.assess.policy.propagation_node import PropagationNode
from contrast.agent.assess.policy.propagators import (
    IGNORE_LENGTH_ACTIONS,
    PROPAGATOR_ACTIONS,
    STREAM_ACTIONS,
    TAG_ACTION,
    BasePropagator,
    stream_propagator,
)
from contrast.agent.assess.policy.source_policy import SourceNode, apply_stream_source
from contrast.agent.assess.properties import Properties
from contrast.agent.assess.policy.preshift import Preshift
from contrast.agent.assess.utils import (
    copy_tags_to_offset,
    copy_events,
    copy_from,
    is_tracked,
    get_properties,
    set_properties,
    track_string,
)
from contrast.utils.assess.duck_utils import (
    is_filelike,
    is_iterable,
    safe_getattr,
    safe_iterator,
    len_or_zero,
)
from contrast.agent.settings_state import SettingsState

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


def apply(nodes, preshift, ret):  # pylint: disable=redefined-builtin
    if not nodes:
        return

    for node in nodes:
        if not preshift:
            continue

        target = node.get_matching_first_target(
            preshift.obj, ret, preshift.args, preshift.kwargs
        )

        apply_propagator(node, preshift, target, ret, None)


def is_target_valid_length(target, action):
    if action in IGNORE_LENGTH_ACTIONS:
        return True

    return len_or_zero(target) > 0


def track_copy_without_new_event(target, self_obj):
    """
    In general, when a string propagation event results in a copy of the
    original object we track the newly created copy but don't record an event.
    This behavior might be modified in the future.

    Usually, python is smart enough not to create a new string object that is
    simply a copy of the original. However, there are several exceptions to
    this rule.

    This method should only be invoked in these special cases, and they should
    be documented heavily.
    """
    if is_tracked(self_obj):
        track_string(target)
        copy_from(target, self_obj, 0, set())


STREAM_SOURCES = ["read", "read1", "readline", "readlines", "getvalue"]
STREAM_WRITE_METHODS = ["write", "writelines"]


def create_stream_event(node_type, stream, frame, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None or not SettingsState().is_assess_enabled():
        return None

    module = stream.__class__.__module__
    class_name = stream.__class__.__name__

    source_type = safe_getattr(stream, "cs__source_type", None) or "BODY"

    if node_type == "source":
        node = SourceNode(
            module, class_name, True, "__init__", "ARG_0", source_type, None
        )
    else:
        node = PropagationNode(
            module, class_name, True, "__init__", "ARG_0", "RETURN", source_type, None
        )

    return ContrastEvent(
        node, stream, stream, None, args, kwargs, [], 0, None, frame=frame
    )


def create_stream_source_event(stream, frame, args, kwargs):
    """
    Called directly from C extensions to create source events for __init__
    """
    init_event = create_stream_event("source", stream, frame, args, kwargs)
    stream.cs__source_event = init_event

    if len(args) > 0:
        properties = get_properties(args[0])
        if properties is not None:
            stream_props = Properties(stream)
            set_properties(stream, stream_props)
            copy_tags_to_offset(stream_props, properties.tags, 0)
            copy_events(stream_props, properties)
            prop_event = create_stream_event("propagation", stream, frame, args, kwargs)
            if prop_event is not None:
                if len(properties.events) > 0:
                    prop_event.parent_ids = [properties.events[-1].event_id]
                stream_props.add_event(prop_event)
            stream.cs__tracked = True


def propagate_stream(method_name, target, self_obj, ret, frame, args, kwargs):
    """
    Called directly from C extensions to propagate stream operations.
    """
    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    preshift = Preshift(self_obj, args, kwargs)

    if method_name in STREAM_WRITE_METHODS:
        stream_propagator.propagate_stream_write(
            method_name, preshift, target, args, kwargs
        )

    elif (
        self_obj.cs__tracked
        and get_properties(self_obj)
        and get_properties(self_obj).tags
    ):
        propagation_method = STREAM_ACTIONS.get(method_name)
        if propagation_method is None:
            return

        propagation_method(method_name, preshift, target, ret, frame)

    # If the stream is already considered tracked, it will not be treated as a
    # source.
    elif self_obj.cs__source and method_name in STREAM_SOURCES:
        apply_stream_source(method_name, target, self_obj, ret, args, kwargs)


def propagate(method_name, target, self_obj, ret, frame, args, kwargs):
    """Called directly from C extensions to propagate string operations"""
    if not isinstance(self_obj, bytearray) and ret is self_obj:
        return

    if is_filelike(self_obj) and self_obj.closed:
        return

    if cast_special_case(method_name, args, target):
        return

    # Copies of strings (unicode) and bytes objects usually return the same
    # object. However, copies of bytearrays return a new object, so it is
    # necessary for us to track the new string, even if it hasn't changed.
    if isinstance(self_obj, bytearray) and ret == self_obj and method_name != "concat":
        track_copy_without_new_event(target, self_obj)
        return

    if translate_special_case(method_name, self_obj, ret):
        track_copy_without_new_event(target, self_obj)
        return

    # Account for the fact that None is a valid argument for cformat, and it
    # also may be a single object. The preshift requires an argument arrary.
    # Eventually this should maybe just move into the C hook for cformat,
    # although it is a bit easier to implement (and debug) where it is here
    if method_name == "cformat" and not isinstance(args, tuple):
        args = (args,)

    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    preshift = Preshift(self_obj, args, kwargs)

    policy = Policy()

    for node in policy.propagators_by_name["BUILTIN.str." + method_name]:
        apply_propagator(node, preshift, target, ret, frame)
        break


# These methods return lists and are handled by the SPLIT propagation action.
# We don't want to iterate over the lists during propagation, but instead need
# to make sure we call the right propagation action first.
SPLIT_PROPAGATOR_METHODS = ["split", "rsplit", "splitlines", "partition", "rpartition"]
REGEX_MODULE = "re"
REGEX_SPLIT = "split"
REGEX_FINDALL = "findall"


def cast_special_case(method_name, args, target):
    """
    We don't want to record an event when `target is source`.

    This will never happen for bytearrays, because they are always at least copied.
    For bytearrays, we check if the source and target are ==, and if so we copy
    tags over without recording a new event.

    It would be better if there were some way to check for this slightly later,
    based on the policy node's information.

    Currently, every other string function is an instance method, so we short-
    circuit out of propagation if `self_obj is ret`. For casting, self_obj is None
    because casting (which is really __new__ for unicode/bytes) is a module method
    """
    if method_name == "CAST":
        source = args and args[0]
        if target is source:
            return True
        if (
            isinstance(source, bytearray)
            and isinstance(target, bytearray)
            and target == source
        ):
            track_copy_without_new_event(target, source)
            return True
    return False


def translate_special_case(method_name, self_obj, ret):
    """
    py27 unicode objects and py3x str objects returned by str.translate()
    are always new objects, so in order to keep our behavior consistent we
    do not create a new event in the case where new == original

    If this method returns True, we should copy all tags from
    self_obj to target without creating a new event.
    """
    return (
        method_name == "translate"
        and ret == self_obj
        and (
            (PY2 and isinstance(self_obj, unicode))
            or (PY3 and isinstance(self_obj, str))
        )
    )


def has_iterable_retval(propagator_node):
    """
    Returns True if given propagator node expects iterable list/tuple return value

    Ordinarily, if we encounter a return value that is a list/tuple, we recurse down in
    order to find simple strings. However, some propagators expect the return value to
    be in an iterable, in which case we need to use the iterable itself to build the
    preshift.
    """
    if propagator_node.module == REGEX_MODULE and propagator_node.method_name in [
        REGEX_SPLIT,
        REGEX_FINDALL,
    ]:
        return True
    if propagator_node.class_name != "str":
        return False
    return propagator_node.method_name in SPLIT_PROPAGATOR_METHODS


def apply_propagator(propagator_node, preshift, target, ret, frame):
    if not propagator_node or not target:
        return

    if not is_target_valid_length(target, propagator_node.action):
        return

    if isinstance(target, dict):
        for key, value in iteritems(target):
            apply_propagator(propagator_node, preshift, key, ret, frame)
            apply_propagator(propagator_node, preshift, value, ret, frame)
    elif is_iterable(target) and not has_iterable_retval(propagator_node):
        for item in safe_iterator(target):
            apply_propagator(propagator_node, preshift, item, ret, frame)
    else:
        propagate_string(propagator_node, preshift, target, ret, frame)


def propagate_string(propagator_node, preshift, target, ret, frame):
    action = propagator_node.action
    propagator_class = PROPAGATOR_ACTIONS.get(action, BasePropagator)
    if propagator_class is BasePropagator and action != TAG_ACTION:
        logger.warning(
            "Unknown action type %s. Using default propagation for %s.%s.",
            propagator_node.action,
            propagator_node.location,
            propagator_node.method_name,
        )

    propagator = propagator_class(propagator_node, preshift, target)

    if not propagator.needs_propagation:
        return

    propagator.track_and_propagate(ret, frame)
    logger.debug(
        "Propagator %s found: propagated to %s", propagator_node.name, id(target)
    )
