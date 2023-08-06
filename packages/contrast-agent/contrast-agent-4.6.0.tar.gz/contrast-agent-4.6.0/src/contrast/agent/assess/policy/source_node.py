# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from pip._vendor.pkg_resources import Requirement

from contrast.agent.policy import constants
from contrast.agent.assess.assess_exceptions import ContrastAssessException
from contrast.agent.policy.policy_node import PolicyNode
from contrast.agent.settings_state import SettingsState
from contrast.api.dtm_pb2 import TraceEvent
from contrast.utils.string_utils import equals_ignore_case


class SourceNode(PolicyNode):
    ALL = "ALL"

    SOURCE_TAG = "UNTRUSTED"

    def __init__(
        self,
        module,
        class_name,
        instance_method,
        method_name,
        target,
        node_type,
        package,
        tags=None,
        source_name=None,
        version=ALL,
        policy_patch=True,
        python2_only=False,
        python3_only=False,
    ):
        super(SourceNode, self).__init__(
            module,
            class_name,
            instance_method,
            method_name,
            source_name,
            target,
            tags,
            policy_patch=policy_patch,
            python2_only=python2_only,
            python3_only=python3_only,
        )

        self.package = package
        self.version = version
        self.type = node_type

        if tags is None:
            self.tags = {self.SOURCE_TAG}
        else:
            self.tags.add(self.SOURCE_TAG)

        self.validate()

    @staticmethod
    def create_source_node(module, class_name, column_name, tags, policy_patch=True):
        instance_method = True
        method_name = column_name
        target = "RETURN"
        file_name = "dynamic_source"

        node = SourceNode(
            module,
            class_name,
            instance_method,
            method_name,
            target,
            constants.DB_SOURCE_TYPE,
            file_name,
            tags=tags,
            policy_patch=policy_patch,
        )

        node.add_property("dynamic_source_id", node.name)

        return node

    @property
    def node_type(self):
        """
        This is confusing. Sources are Creation action but Propagation type. Oh
        and also Type refers to input type, like parameter, so we have to call
        this node_type. :-/
        """
        return TraceEvent.TYPE_PROPAGATION

    def should_apply(self):
        if equals_ignore_case(self.version, self.ALL) or not self.package:
            return True

        settings = SettingsState()

        if not settings:
            return False

        libraries = [
            lib
            for lib in settings.libraries
            if lib.file_path.lower() == self.package.lower()
        ]

        if not libraries:
            return False

        applicable_library = libraries[0]

        return self._compare_requirement(
            self.package, applicable_library.version, self.version
        )

    @staticmethod
    def _compare_requirement(package, library_version, required_version):
        requirement = SourceNode._convert_to_requirement(package, required_version)

        return requirement and library_version in requirement

    @staticmethod
    def _convert_to_requirement(package, version):
        return Requirement.parse(package + version)

    def validate(self):

        super(SourceNode, self).validate()

        if not self.targets:
            raise ContrastAssessException(
                "Source {} did not have a proper target. Unable to create.".format(
                    self.name
                )
            )

        if not self.type:
            raise ContrastAssessException(
                "Source {} did not have a proper type. Unable to create.".format(
                    self.name
                )
            )

    @staticmethod
    def from_dict(framework, obj):
        return SourceNode(
            obj[constants.JSON_MODULE],
            obj.get(constants.JSON_CLASS_NAME, ""),
            obj.get(constants.JSON_INSTANCE_METHOD, True),
            obj[constants.JSON_METHOD_NAME],
            obj[constants.JSON_TARGET],
            obj[constants.JSON_TYPE],
            framework,
            obj.get(constants.JSON_TAGS, []),
            obj.get(constants.JSON_SOURCE_NAME, None),
            obj.get(constants.JSON_VERSION, SourceNode.ALL),
            policy_patch=obj.get(constants.JSON_POLICY_PATCH, True),
            python2_only=obj.get(constants.JSON_PY2_ONLY, False),
            python3_only=obj.get(constants.JSON_PY3_ONLY, False),
        )
