# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.utils.exceptions.security_exception import SecurityException

from contrast.extern import structlog as logging
import traceback

logger = logging.getLogger("contrast")


def set_context(flag):
    """
    Decorator to set the context of a method. For instance, multiple methods call the same method but it may want
    to handle some logic differently but the same method does not know who is calling it.

    As long as the attribute, represented as a string exists in the object it will flip it before and after the call.

    :param flag: string of attribute
    :return: decorator that takes in one argument
    """

    def wrap(func):
        def wrapped_func(self, *args, **kwargs):
            if hasattr(self, flag):
                setattr(self, flag, not getattr(self, flag))

            try:
                result = func(self, *args, **kwargs)
            finally:
                if hasattr(self, flag):
                    setattr(self, flag, not getattr(self, flag))

            return result

        return wrapped_func

    return wrap


def fail_safely(log_message, log_level="exception", return_value=None):
    """
    Decorator that will run the decorated function/method and, if
    an exception is raised, return a safe value and log the error.

    Note that SecurityException will always be re-raised.

    :param log_message: message to log in case of failure
    :param log_level: level to log in case of failure
    :param return_value: safe value to return in case of failure
    :return: original func return or return_value
    """

    def wrap(original_func):
        def run_safely(*args, **kwargs):
            try:
                return original_func(*args, **kwargs)
            except SecurityException:
                raise
            except Exception as e:
                try:
                    getattr(logger, log_level)(log_message + ": " + str(e))
                    logger.debug("wrapped function args: %s", args)
                    logger.debug("wrapped function kwargs: %s", kwargs)
                except Exception as e:
                    logger.debug(
                        "Failed to log arguments passed to original_func",
                        exception_thrown=str(e),
                    )

            return return_value

        return run_safely

    return wrap


def fail_quietly(log_message, return_value=None):
    """
    Similar to fail_safely (see above)

    This decorator is intended to handle cases where an exception may occur but won't
    disrupt normal operation of the agent. This decorator should be used to protect
    against external exceptions we can't prevent but still want to handle.

    In these cases, we log an error message and the exception traceback, both at DEBUG
    level.
    """

    def wrap(original_func):
        def run_safely(*args, **kwargs):
            try:
                return original_func(*args, **kwargs)
            except SecurityException:
                raise
            except Exception as e:
                logger.debug("%s: %s", log_message, str(e))
                logger.debug(traceback.format_exc())

            return return_value

        return run_safely

    return wrap


class cached_property(object):
    """
    https://github.com/pydanny/cached-property
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self

        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value
