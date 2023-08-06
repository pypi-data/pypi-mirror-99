# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.extern.wrapt import register_post_import_hook

import contrast
from contrast.agent import scope
from contrast.agent.policy import patch_manager
from contrast.agent.settings_state import SettingsState
from contrast.agent.assess.apply_trigger import cs__apply_trigger
from contrast.agent.policy.trigger_node import TriggerNode
from contrast.agent.policy.loader import Policy
from contrast.utils.decorators import fail_safely
from contrast.utils.patch_utils import patch_cls_or_instance

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


@fail_safely("Failed to apply rule for crypto-bad-mac")
def apply_rule(args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is None or not SettingsState().is_assess_enabled():
        return

    if scope.in_contrast_scope():
        return

    with scope.contrast_scope():
        policy = Policy()

        bad_mac_rule = policy.triggers["crypto-bad-mac"]

        self_obj = args[0]

        trigger_node = TriggerNode(
            self_obj.__class__.__module__,
            self_obj.__class__.__name__,
            True,
            "__init__",
            None,
            dataflow=False,
        )

        cs__apply_trigger(
            context,
            bad_mac_rule,
            trigger_node,
            None,
            self_obj,
            None,
            None,
            args,
            kwargs,
        )


def __init__(orig_func, patch_policy=None, *args, **kwargs):
    orig_func(*args, **kwargs)
    # TODO: PYT-798 This may be currently broken because there are not policy nodes associated
    # with these patch locations. These need to be added and this rule needs to be tested.
    apply_rule(args, kwargs)


def build_hash_patch(name):
    def patch_hash(module):
        hasher = getattr(module, name, None)
        if hasher is None:
            logger.debug(
                "WARNING: failed to instrument %s.%s. "
                "Unsupported pycryptodome version likely",
                module.__name__,
                name,
            )
            return

        patch_cls_or_instance(hasher, "__init__", __init__)

    return patch_hash


def register_patches():
    # TODO: PYT-797 pycryptodomex patches are exactly the same, except they have Cryptodome as
    # the top-level module name. It's possible that Crypto calls Cryptodome under the
    # hood, and so we end up patching both. More investigation required.
    register_post_import_hook(build_hash_patch("MD2Hash"), "Crypto.Hash.MD2")
    register_post_import_hook(build_hash_patch("MD4Hash"), "Crypto.Hash.MD4")
    register_post_import_hook(build_hash_patch("MD5Hash"), "Crypto.Hash.MD5")
    register_post_import_hook(build_hash_patch("SHA1Hash"), "Crypto.Hash.SHA1")


def reverse_patches():
    crypto_module = sys.modules.get("Crypto")
    if not crypto_module:
        return

    patch_manager.reverse_patches_by_owner(crypto_module.Hash.MD2.MD2Hash)
    patch_manager.reverse_patches_by_owner(crypto_module.Hash.MD4.MD4Hash)
    patch_manager.reverse_patches_by_owner(crypto_module.Hash.MD5.MD5Hash)
    patch_manager.reverse_patches_by_owner(crypto_module.Hash.SHA1.SHA1Hash)
