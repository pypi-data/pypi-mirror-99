# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent.settings_state import SettingsState

DATABASE_CASSANDRA = "Cassandra"
DATABASE_MYSQL = "MySQL"
DATABASE_PG = "PostgreSQL"
DATABASE_SQL_ALCHEMY = "SQLAlchemy"
DATABASE_SQLITE = "SQLite3"

ACTION_EXEC = "exec"
ACTION_EXECUTE = "execute"


def apply_rule(patch_policy, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None and SettingsState().is_protect_enabled():
        for node in patch_policy.trigger_nodes:
            rule_name = node.rule.name
            rule = SettingsState().defend_rules.get(rule_name)
            if not rule or not rule.enabled:
                continue

            for source in node.get_protect_sources(args, kwargs):
                rule.protect(patch_policy, source, args, kwargs)

    return orig_func(*args, **kwargs)
