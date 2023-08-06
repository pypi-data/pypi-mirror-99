# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.triggers.trigger_config_rule import TriggerConfigRule
from contrast.agent.assess.rules.config.secure_flag_rule import SecureFlagRuleMixin


class SecureFlagMissingRule(TriggerConfigRule, SecureFlagRuleMixin):
    def is_violated_properties(*args, **kwargs):
        """Override for safety. In theory, this should never be called."""
        return False

    def is_violated(self, node, source, **kwargs):
        return SecureFlagRuleMixin.is_violated(self, source)
