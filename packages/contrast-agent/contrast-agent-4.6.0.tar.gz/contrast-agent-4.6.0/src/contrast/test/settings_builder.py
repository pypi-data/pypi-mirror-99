# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import time

from contrast.extern.six import iteritems

from contrast.agent.settings_state import SettingsState
from contrast.api.settings_pb2 import (
    AgentSettings,
    ProtectionRule,
)

from contrast.configuration import AgentConfig

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class SettingsBuilder(object):
    DEFAULT_FEATURES = {
        "defend": {"enabled": True},
        "log_file": "contrast_test.log",
        "log_level": "INFO",
    }

    DEFAULT_SETTINGS = {
        "protection_rules": [
            {
                "id": "cmd-injection",
                "name": "Command Injection",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "method-tampering",
                "name": "Http Method Tampering",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "path-traversal",
                "name": "Path Traversal",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "sql-injection",
                "name": "SQL Injection",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "reflected-xss",
                "name": "Cross-Site Scripting",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "untrusted-deserialization",
                "name": "Untrusted Deserialization",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "xxe",
                "name": "XML External Entity Processing",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "reflected-xss",
                "name": "Cross-Site Scripting",
                "mode": ProtectionRule.BLOCK_AT_PERIMETER,
            },
            {
                "id": "unsafe-code-execution",
                "name": "Unsafe Code Execution",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "ssrf",
                "name": "Server-Side Request Forgery",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "unsafe-file-upload",
                "name": "Server-Side Request Forgery",
                "mode": ProtectionRule.BLOCK_AT_PERIMETER,
            },
            {
                "id": "nosql-injection",
                "name": "Command Injection",
                "mode": ProtectionRule.BLOCK,
            },
        ],
        "disabled_assess_rules": ["test_application_disabled"],
    }

    def __init__(self):
        self._settings = None

    def settings(self, settings_dict=None, features_dict=None, defend_rules=None):
        self._settings = SettingsState()
        self._settings.config = AgentConfig()

        if settings_dict or features_dict or defend_rules:
            agent_settings = self.service_response(
                settings_dict=self._defend_rule_settings(defend_rules),
                features_dict=features_dict,
            )
        else:

            agent_settings = self.service_response(
                settings_dict=self.DEFAULT_SETTINGS, features_dict=self.DEFAULT_FEATURES
            )

        self._settings.process_service_response(agent_settings)

        self._settings.set_protect_rules()

        if defend_rules:
            needed_rules = [dr["id"] for dr in defend_rules]

            self._settings.defend_rules = {
                k: v
                for k, v in iteritems(self._settings.defend_rules)
                if k in needed_rules
            }

        return self._settings

    def build(self, settings_dict=None, features_dict=None, defend_rules=None):
        return self.settings(
            settings_dict=settings_dict,
            features_dict=features_dict,
            defend_rules=defend_rules,
        )

    def build_assess(self):
        settings = self.settings()
        settings.server_features.defend.enabled = False
        settings.server_features.assess.enabled = True

        settings.config.put("assess.enable", True)
        settings.config.put("protect.enable", False)

        return settings

    def service_response(self, settings_dict=None, features_dict=None):
        obj = AgentSettings()
        obj.sent_ms = int(time.time() * 1000)

        SettingsBuilder.populate_from_dict(
            obj.server_features,
            features_dict if features_dict else self.DEFAULT_FEATURES,
        )

        SettingsBuilder.populate_from_dict(
            obj.application_settings,
            settings_dict if settings_dict else self.DEFAULT_SETTINGS,
        )

        return obj

    def _defend_rule_settings(self, defend_rules=None):
        if defend_rules:
            return {
                "protection_rules": [
                    SettingsBuilder._defend_rule_entry(rule) for rule in defend_rules
                ]
            }

        return self.DEFAULT_SETTINGS

    @staticmethod
    def _defend_rule_entry(rule):
        if isinstance(rule, dict):
            return rule

        return {"id": str(rule), "name": str(rule), "mode": ProtectionRule.BLOCK}

    @staticmethod
    def populate_from_dict(pb, values):
        """
        Initialize the given protobuf instance from a python dictionary
        """
        for key, value in iteritems(values):
            if isinstance(value, dict):
                SettingsBuilder.populate_from_dict(getattr(pb, key), value)
            elif isinstance(value, list):
                SettingsBuilder.populate_from_list(getattr(pb, key), value)
            else:
                try:
                    setattr(pb, key, value)
                except AttributeError:
                    logger.error(
                        "Unable to set protobuf instance %s : %s=%s",
                        type(pb),
                        key,
                        value,
                    )

        return pb

    @staticmethod
    def populate_from_list(pb, values):
        """
        Initialize the given protobuf instance from a python list
        """
        if len(values) > 0:
            if isinstance(values[0], dict):
                for value in values:
                    child = pb.add()
                    SettingsBuilder.populate_from_dict(child, value)
            else:
                pb.extend(values)
