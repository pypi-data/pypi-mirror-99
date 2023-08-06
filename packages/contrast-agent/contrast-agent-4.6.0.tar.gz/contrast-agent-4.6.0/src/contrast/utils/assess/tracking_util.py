# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import io

from contrast.extern.six import iteritems

from contrast.agent.assess.utils import is_tracked
from contrast.utils.decorators import fail_quietly
from contrast.utils.assess.duck_utils import safe_getattr, safe_iterator

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


@fail_quietly("Failed check if obj is tracked", return_value=False)
def recursive_is_tracked(obj):
    if obj is None:
        return False

    if isinstance(obj, dict):
        for key, value in iteritems(obj):
            if recursive_is_tracked(key) or recursive_is_tracked(value):
                return True
    elif isinstance(obj, io.IOBase):
        return safe_getattr(obj, "cs__tracked", False) or safe_getattr(
            obj, "cs__source", False
        )
    # These are the only safe objects where we can guarantee that we won't
    # destructively modify the object such that the application may see
    # different results.
    elif isinstance(obj, (list, tuple)):
        return any(recursive_is_tracked(item) for item in safe_iterator(obj))

    return is_tracked(obj)
