# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Controller for global scope state

Basically we use scoping to prevent us from assessing our own code. Scope
improves performance but it also prevents us from accidentally recursing
inside our analysis code. For example, we don't want to inadvertently cause
string propagation events while we're doing string building for reporting
purposes.
"""
import sys

from contextlib import contextmanager

from contrast.assess_extensions import cs_str


__SCOPE_LEVELS = ("contrast", "propagation", "trigger", "eval")


def __build_func(func, level):
    func = getattr(cs_str, func)

    def _func():
        return func(level)

    return _func


def __build_context(enter, exit_):
    def _func():
        enter()
        try:
            yield
        finally:
            exit_()

    return _func


def __generate_scope_functions(scope_levels):
    """
    Auto-generates scope control API based on scope level names
    """
    mod = sys.modules[__name__]

    for name in scope_levels:
        level = getattr(cs_str, "{}_SCOPE".format(name.upper()))

        enter = __build_func("enter_scope", level)
        exit_ = __build_func("exit_scope", level)
        in_ = __build_func("in_scope", level)
        context = __build_context(enter, exit_)

        exit_.__doc__ = "Exit {} scope".format(name)
        in_.__doc__ = "Returns True if in {} scope".format(name)
        context.__doc__ = "Context manager for {} scope".format(name)

        setattr(mod, "enter_{}_scope".format(name), enter)
        setattr(mod, "exit_{}_scope".format(name), exit_)
        setattr(mod, "in_{}_scope".format(name), in_)
        setattr(mod, "{}_scope".format(name), contextmanager(context))


__generate_scope_functions(__SCOPE_LEVELS)


enter_contrast_scope.__doc__ = """
    Enter contrast scope

    Contrast scope is global. It should prevent us from taking *any*
    further analysis action, whether it be propagation or evaluating
    triggers.
"""
enter_propagation_scope.__doc__ = """
    Enter propagation scope
     
    While in propagation scope, prevent any further propagation actions.
    Basically this means that no string propagation should occur while in
    propagation scope.
"""
enter_trigger_scope.__doc__ = """
    Enter trigger scope

    While in trigger scope, prevent analysis inside of any other trigger
    methods that get called.
"""
enter_eval_scope.__doc__ = """
    Enter eval scope

    This is a special case that prevents multiple trigger events when calling eval in
    PY2.
"""


def in_scope():
    """Indicates we are in either contrast scope or propagation scope"""
    return in_contrast_scope() or in_propagation_scope()


@contextmanager
def pop_contrast_scope():
    """
    Context manager that pops contrast scope level and restores it when it exits

    Scope is implemented as a stack. If the thread is in contrast scope at the time
    this is called, the scope level will be reduced by one for the lifetime of the
    context manager. If the prior scope level was 1, this has the effect of temporarily
    disabling contrast scope. The original scope level will be restored when the
    context manager exits. If the thread is **not** already in contrast scope when this
    is called, it has no effect.
    """
    in_scope = in_contrast_scope()
    # This has no effect if we're not already in scope
    exit_contrast_scope()
    try:
        yield
    finally:
        # For safety, only restore scope if we were in it to begin with
        if in_scope:
            enter_contrast_scope()
