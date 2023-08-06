# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

from contrast.extern.six import string_types
from contrast.agent.protect.mixins.path_traversal_sink_features import (
    PathTraversalSinkFeatures,
)
from contrast.agent.protect.rule.base_rule import BaseRule

from contrast.utils.decorators import fail_quietly

PARENT_CHECK = ".."
SLASH = "/"
SAFE_PATHS = ["tmp", "public", "docs", "static", "template", "templates"]


class PathTraversal(BaseRule, PathTraversalSinkFeatures):
    NAME = "path-traversal"

    def __init__(self, settings):
        BaseRule.__init__(self, settings)

    def find_attack(self, candidate_string=None, **kwargs):
        """
        Finds the attacker in the original string if present
        """
        attack = super(PathTraversal, self).find_attack(candidate_string, **kwargs)
        if self.in_infilter:
            attack = self.check_sink_features(candidate_string, attack)

        return attack

    def build_sample(self, evaluation, path, **kwargs):
        sample = self.build_base_sample(evaluation)
        if path is not None:
            sample.path_traversal.path = path
        return sample

    @fail_quietly(
        "Failed to run path traversal skip_protect_analysis", return_value=False
    )
    def skip_protect_analysis(self, user_input, args, kwargs):
        write = possible_write(args, kwargs)
        if write:
            # any write is a risk so we should not skip analysis
            return False

        return not actionable_path(user_input)

    def infilter_kwargs(self, user_input, patch_policy):
        return dict(method=patch_policy.method_name)


def possible_write(args, kwargs):
    if "w" in kwargs.get("mode", ""):
        return True

    return len(args) > 1 and args[1] is not None and "w" in args[1]


def actionable_path(path):
    if not path or not isinstance(path, string_types):
        return False

    # moving up directory structure is a risk and hence actionable
    if path.find(PARENT_CHECK) > 1:
        return True

    if "/contrast/" in path or "/site-packages/" in path:
        return False

    if path.startswith(SLASH):
        for prefix in _safer_abs_paths():
            if path.startswith(prefix):
                return False
    else:
        for prefix in SAFE_PATHS:
            if path.startswith(prefix):
                return False

    return True


def _safer_abs_paths():
    pwd = os.getcwd()

    return ["{}/{}".format(pwd, item) for item in SAFE_PATHS] if pwd else []
