# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import defaultdict
from inspect import isclass

from contrast.assess_extensions import smart_setattr
from contrast.utils import Namespace

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class module(Namespace):
    # map from id(orig_attr) -> patch
    patch_map = {}
    # map from id(patch) -> orig_attr
    inverse_patch_map = {}
    # list of modules we've visited, whose relevant
    # attributes we've at least initially patched
    visited_modules = set()
    # allows lookup of patches by owner ID
    # this is what enables reverse patching
    patches_by_owner = defaultdict(set)
    # allows lookup of patches by owner name
    # this is currently just for debugging but may eventually be useful for
    # reverse patching by name
    patches_by_name = defaultdict(set)


def get_name(obj):
    return "{0.__module__}.{0.__name__}".format(obj) if isclass(obj) else obj.__name__


def patch(owner, name, patch=None):
    """
    Set attribute `name` of `owner` to `patch`.

    If `patch` is not provided, we look up the appropriate existing patch in
    the patch book and apply it. This behavior is used during repatching.

    :param owner: module or class that owns the original attribute
    :param name: str name of the attribute being patched
    :param patch: object replacing owner.name, or None to use an existing patch
    """
    orig_attr = getattr(owner, name, None)
    underlying = as_func(orig_attr)

    if underlying is None:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: failed to patch %s of %s: no such attribute", name, owner
        )
        return
    if patch is None:
        patch = module.patch_map.get(id(underlying))
        if patch is None:
            # TODO: PYT-692 investigate unexpected patching
            logger.debug(
                "WARNING: failed to repatch %s of %s: no entry in the patch map",
                name,
                owner,
            )
            return

    if id(underlying) in module.inverse_patch_map:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: patching over already patched method %s of %s", name, owner
        )

    smart_setattr(owner, name, patch)
    register_patch(owner, name, orig_attr)


def _reverse_patch(owner, name):
    """
    Restore a patched attribute back to its original

    :param owner: module or class that owns the attribute being reverse patched
    :param name: name of the attribute as a string
    """
    patch = as_func(getattr(owner, name, None))

    if patch is None:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: failed to reverse patch %s of %s: no such attribute", name, owner
        )
        return

    if not is_patched(patch):
        return

    orig_attr = module.inverse_patch_map[id(patch)]

    smart_setattr(owner, name, orig_attr)
    _deregister_patch(patch, owner, name, orig_attr)


def reverse_patches_by_owner(owner):
    """
    Restore all patched attributes that belong to the owning module/class

    If the owner is a module, any patched classes in this module will not be
    automatically reversed by this method. For example, if the following are patched:

        foo.a
        foo.b
        foo.FooClass.foo_method

    in order to reverse the patches, it will be necessary to call this method twice:

        reverse_patches_by_owner(foo)
        reverse_patches_by_owner(foo.FooClass)

    :param owner: module or class that owns the attribute being reverse patched
    """
    if not id(owner) in module.patches_by_owner:
        return

    for name in list(module.patches_by_owner[id(owner)]):
        _reverse_patch(owner, name)


def register_patch(owner, name, orig_attr):
    """
    Register patch in the patch map to prevent us from patching twice

    :param owner: module or class that owns the original function
    :param name: name of the patched attribute
    :param orig_attr: original attribute, which is being replaced
    """
    mark_visited(owner)

    patch = as_func(getattr(owner, name))
    underlying = as_func(orig_attr)

    if id(module.patch_map.get(id(underlying))) == id(patch):
        return
    if patch is underlying:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: attempt to register %s as a patch for itself - "
            "skipping patch map registration",
            orig_attr,
        )
        return

    module.patch_map[id(underlying)] = patch
    module.inverse_patch_map[id(patch)] = orig_attr
    module.patches_by_owner[id(owner)].add(name)
    module.patches_by_name[get_name(owner)].add(name)


def _deregister_patch(patch, owner, name, orig_attr):
    """
    Remove the patch from all locations in the patch manager.
    """
    owner_name = get_name(owner)
    underlying = as_func(orig_attr)
    module.patches_by_owner[id(owner)].discard(name)
    module.patches_by_name[owner_name].discard(name)
    # if by removing the `name` value from id(owner) set the set becomes
    # empty, remove the key from the dict, too.
    if not module.patches_by_owner[id(owner)]:
        del module.patches_by_owner[id(owner)]
        del module.patches_by_name[owner_name]

    del module.patch_map[id(underlying)]
    del module.inverse_patch_map[id(patch)]
    remove_visited(owner)

    from contrast.agent.policy.applicator import remove_patch_location

    remove_patch_location(owner, name)


def is_patched(attr):
    """
    If the given attribute is a key in the inverse patch map, it means that it is being
    used as a patch.

    :param attr: attribute in question
    :return: True if the attribute is a key in the inverse patch map, False otherwise
    """
    return id(as_func(attr)) in module.inverse_patch_map


def has_associated_patch(attr):
    """
    If we come across an attribute that's a value in the patch_map (a key in
    the inverse patch map), it should be patched. This is most useful during
    re-patching, where we might see an old reference to the unpatched original
    attribute.

    :param attr: attribute in question
    :return: True if the attribute is a key in the patch map, False otherwise
    """
    return id(as_func(attr)) in module.patch_map


def is_visited(module_):
    """
    Check if we've visited a given module.

    :param module_: module object in question
    :return: True if we've visited this module in the context of patching,
        False otherwise
    """
    return id(module_) in module.visited_modules


def mark_visited(module_):
    """
    Mark a module as visited.

    :param module_: module object in question
    """
    module.visited_modules.add(id(module_))


def remove_visited(module_):
    if is_visited(module_):
        module.visited_modules.remove(id(module_))


def clear_visited_modules():
    """
    Clear the set of visited modules.
    """
    module.visited_modules.clear()


def as_func(attr):
    """
    In python 2, we can't trust the id of unbound methods. For example, if we have
    class Foo with instance method bar, Foo.bar returns a wrapper around the actual
    function object, and that wrapper may change between accesses to Foo.bar.

    This is due to the descriptor protocol; in python2 methods are descriptors,
    like properties.

    However, unbound methods should have a __func__ attribute, which references the
    raw underlying function. This value does not change, so we want to enter its id
    in the patch map.
    """
    return getattr(attr, "__func__", attr)
