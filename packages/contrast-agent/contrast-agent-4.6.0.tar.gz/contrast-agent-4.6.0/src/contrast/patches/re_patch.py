# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implementation of patches for the `re` module.

Other methods of the `re` module such as `split` and `escape` can be patched directly,
so they are implemented in policy.
"""
import functools
from contrast.extern import structlog as logging
import sys

from contrast.extern.wrapt import register_post_import_hook
from contrast.extern import six

import contrast
from contrast.agent import scope
from contrast.agent.policy import patch_manager
from contrast.agent.policy.loader import Policy
from contrast.agent.assess.apply_trigger import cs__apply_trigger
from contrast.agent.assess.policy.analysis import analyze
from contrast.agent.assess.policy.propagators import regex_propagator
from contrast.utils.decorators import fail_safely
from contrast.utils.patch_utils import patch_cls_or_instance

logger = logging.getLogger("contrast")

SPLIT = "split"
SUB = "sub"
SUBN = "subn"
MATCH = "match"
SEARCH = "search"
FINDALL = "findall"
FINDITER = "finditer"
FULLMATCH = "fullmatch"


def _group_propagator(method, propagator, *args, **kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()
    result = method(*args, **kwargs)
    if context is not None and context.propagate_assess:
        with scope.propagation_scope():
            propagator(args[0], result, *args[1:])
    return result


def group_hook(original_func, patch_policy, *args, **kwargs):
    propagator = regex_propagator.propagate_group
    return _group_propagator(original_func, propagator, *args, **kwargs)


def groups_hook(original_func, patch_policy, *args, **kwargs):
    propagator = regex_propagator.propagate_groups
    return _group_propagator(original_func, propagator, *args, **kwargs)


def groupdict_hook(original_func, patch_policy, *args, **kwargs):
    propagator = regex_propagator.propagate_groupdict
    return _group_propagator(original_func, propagator, *args, **kwargs)


def wrap_repl(repl):
    repl_results = []

    def new_repl(match):
        result = repl(match)
        repl_results.append(result)
        return result

    functools.update_wrapper(new_repl, repl)
    return new_repl, repl_results


@fail_safely("Failed to get propagation node")
def _get_propagation_node(name):
    policy = Policy().policy_by_name[name]
    return policy.propagator_nodes[0] if policy.propagator_nodes else None


@fail_safely("Failed to propagate sub(n)")
def _analyze_sub(node, retval, repl_results, args, kwargs, new_args):
    if node.method_name == "subn":
        result, count = retval
    else:
        # Account for the fact that count could either be positional or kwarg
        count = args[3] if len(args) == 4 else kwargs.pop("count", 0)
        result = retval

    # Omit count (and flags) if they are part of posargs since they are being passed
    # explicitly to our propagator
    new_args = new_args[:3]
    new_kwargs = dict(count=count)
    if not node.instance_method:
        # Account for the fact that flags could either be positional or kwarg
        new_kwargs["flags"] = args[4] if len(args) > 4 else kwargs.get("flags", 0)

    with scope.propagation_scope():
        regex_propagator.propagate_sub(
            node, result, repl_results, *new_args[:3], **new_kwargs
        )


def _sub_hook_impl(name, original_func, *args, **kwargs):
    """
    Hook for re.sub and re.subn used for propagation in assess

    The following explains why we can't simply patch these methods using
    policy.

    It is possible for the repl argument to be a callable. In this case, the
    callable is passed a Match object, and it returns the string to be used for
    the replacement. In order to correctly propagate the substitution
    operation, we need to keep track of the results of calling the replacement
    function.

    It might seem like we should just call the replacement function again
    during our propagation action. But this is not practicable for several
    reasons:

      1. We're in scope at the time, so any propagation that needs to occur
         within the replacement callable itself will be missed.
      2. Related to above, but methods of Match do not return the same object
         even when called multiple times with the same arguments, so we would
         not be tracking the strings that actually get used in the substitution
         result.
      3. There's no guarantee that the replacement function does not cause any
         side effects or rely on any state in application code. We definitely
         don't want to mess around with this.

    The solution is to wrap the replacement callable with our own function that
    records the results of each call. We then pass our wrapped callable to the
    original function, and we pass the accumulated results to the propagator.
    This has the additional benefit of allowing us to wrap the match object
    that is passed to the repl function with our proxied object so that we
    propagate any calls that are made within this function if necessary.
    """
    # Get the non-propagation case out of the way here
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None or not context.propagate_assess:
        return original_func(*args, **kwargs)

    node = _get_propagation_node(name)
    if not node:
        return original_func(*args, **kwargs)

    try:
        repl = args[1]
        new_repl, repl_results = wrap_repl(repl) if callable(repl) else (repl, None)
        new_args = tuple(args[:1]) + (new_repl,) + tuple(args[2:])
    except Exception:
        # This indicates that the original caller passed garbage, so call the original
        # function and let the error propagate back up to where they can clean up their
        # own mess.
        return original_func(*args, **kwargs)

    retval = original_func(*new_args, **kwargs)

    _trigger_redos(name, retval, args, kwargs)
    _analyze_sub(node, retval, repl_results, args, kwargs, new_args)

    return retval


@fail_safely("Failed to analyze redos trigger")
def _trigger_redos(name, result, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None:
        return

    policy = Policy()
    rule = policy.triggers["redos"]

    if rule.disabled:
        # Given how often these patches are called within apps, it's well worth
        # returning early here even though this logic exists further down the stack.
        return

    if not scope.in_trigger_scope() and not scope.in_contrast_scope():
        trigger_node = _get_redos_trigger_node(name, rule)

        # Both trigger and contrast scope are needed here.
        with scope.trigger_scope(), scope.contrast_scope():
            # we cannot use trigger_policy.apply here due to the instance_method
            # logic it uses to remove self_obj from args. For the redos action,
            # specifically for re.Pattern.method nodes, we NEED the self_obj
            # to be in the args at this time.
            source = trigger_node.get_matching_sources(None, result, args, kwargs)[0]
            cs__apply_trigger(
                context, rule, trigger_node, source, None, result, None, args, kwargs,
            )


def _get_redos_trigger_node(trigger_name, rule):
    trigger_loc = "re"
    if "Pattern" in trigger_name:
        trigger_loc = "re.Pattern"

    func_name = trigger_name.split(".")[-1]
    trigger_nodes = rule.find_trigger_nodes(trigger_loc, func_name)

    return trigger_nodes[0]


def sub_hook(original_sub, patch_policy, *args, **kwargs):
    """See docstring for _sub_hook_impl above"""
    return _sub_hook_impl("re.sub", original_sub, *args, **kwargs)


def subn_hook(original_subn, patch_policy, *args, **kwargs):
    """See docstring for _sub_hook_impl above"""
    return _sub_hook_impl("re.subn", original_subn, *args, **kwargs)


def pattern_sub_hook(original_sub, patch_policy, *args, **kwargs):
    """See docstring for _sub_hook_impl above"""
    return _sub_hook_impl("re.Pattern.sub", original_sub, *args, **kwargs)


def pattern_subn_hook(original_subn, patch_policy, *args, **kwargs):
    """See docstring for _sub_hook_impl above"""
    return _sub_hook_impl("re.Pattern.subn", original_subn, *args, **kwargs)


def pattern_findall_hook(original_func, patch_policy, *args, **kwargs):
    retval = original_func(*args, **kwargs)
    _trigger_redos("re.Pattern.findall", retval, args, kwargs)
    _analyze_policy("re.Pattern.findall", retval, args, kwargs)
    return retval


@fail_safely("Failed to analyze")
def _analyze_policy(name, result, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None or not context.propagate_assess:
        return

    with scope.contrast_scope():
        policy = Policy()
        patch_policy = policy.policy_by_name.get(name)
        if not patch_policy:
            return

    analyze(context, patch_policy, result, args, kwargs)


def pattern_split_hook(original_split, patch_policy, *args, **kwargs):
    result = original_split(*args, **kwargs)
    _trigger_redos("re.Pattern.split", result, args, kwargs)
    _analyze_policy("re.Pattern.split", result, args, kwargs)
    return result


def pattern_match_hook(original_func, patch_policy, *args, **kwargs):
    retval = original_func(*args, **kwargs)
    _trigger_redos("re.Pattern.match", retval, args, kwargs)
    return retval


def pattern_search_hook(original_func, patch_policy, *args, **kwargs):
    retval = original_func(*args, **kwargs)
    _trigger_redos("re.Pattern.search", retval, args, kwargs)
    return retval


def pattern_finditer_hook(original_func, patch_policy, *args, **kwargs):
    retval = original_func(*args, **kwargs)
    _trigger_redos("re.Pattern.finditer", retval, args, kwargs)
    return retval


def pattern_fullmatch_hook(original_func, patch_policy, *args, **kwargs):
    retval = original_func(*args, **kwargs)
    _trigger_redos("re.Pattern.fullmatch", retval, args, kwargs)
    return retval


def patch_re(re_module):
    # The re.Pattern and re.Match classes are not directly accessible in all versions
    # of Python, so we do this somewhat hacky workaround to get a reference to them.
    pattern_cls = re_module.compile("").__class__
    match_cls = re_module.match("", "").__class__

    patch_cls_or_instance(re_module, SUB, sub_hook)
    patch_cls_or_instance(re_module, SUBN, subn_hook)

    patch_cls_or_instance(pattern_cls, SUB, pattern_sub_hook)
    patch_cls_or_instance(pattern_cls, SUBN, pattern_subn_hook)
    patch_cls_or_instance(pattern_cls, SPLIT, pattern_split_hook)
    patch_cls_or_instance(pattern_cls, FINDALL, pattern_findall_hook)

    patch_cls_or_instance(pattern_cls, MATCH, pattern_match_hook)
    patch_cls_or_instance(pattern_cls, SEARCH, pattern_search_hook)
    patch_cls_or_instance(pattern_cls, FINDITER, pattern_finditer_hook)

    if six.PY3:
        # fullmatch method is new in Py3
        patch_cls_or_instance(pattern_cls, FULLMATCH, pattern_fullmatch_hook)

    patch_cls_or_instance(match_cls, "group", group_hook)
    patch_cls_or_instance(match_cls, "groups", groups_hook)
    patch_cls_or_instance(match_cls, "groupdict", groupdict_hook)


def register_patches():
    register_post_import_hook(patch_re, "re")


def reverse_patches():
    re_module = sys.modules.get("re")
    if not re_module:
        return

    pattern_cls = re_module.compile("").__class__
    match_cls = re_module.match("", "").__class__

    patch_manager.reverse_patches_by_owner(re_module)
    patch_manager.reverse_patches_by_owner(pattern_cls)
    patch_manager.reverse_patches_by_owner(match_cls)
