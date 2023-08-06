# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.middlewares.route_coverage.pyramid_routes import PyramidRoutesMixin
from contrast.agent.middlewares.wsgi_middleware import WSGIMiddleware
from contrast.utils.assess.duck_utils import safe_getattr

from contrast.extern import structlog as logging

from pyramid.registry import Registry

logger = logging.getLogger("contrast")


class PyramidWSGIMiddleware(PyramidRoutesMixin, WSGIMiddleware):
    """
    A subclass of the WSGI middleware that provides pyramid route coverage.
    "configuration scanning" in pyramid is handled dynamically with triggers.

    This is not a pyramid-style tween - it must wrap pyramid's WSGI application
    directly. The WSGI app is typically returned by a call to some Configurator
    instance's `make_wsgi_app()`.
    """

    def __init__(self, wsgi_app, registry=None):
        """
        This deviates slightly from typical WSGI Middleware API, because we need
        `registry` to get framework-specific information about the application.

        The application's `Registry` is commonly available as an attribute on the
        `Configurator` instance used to construct the application. It is also available
        as an attribute of the original WSGI application object returned by
        `Configurator.make_wsgi_app()`. Note that we can't guarantee that the WSGI app
        passed to this constructor has a `registry` attribute, since the original
        Pyramid WSGI app might have already been wrapped by other WSGI middlewares.

        @param wsgi_app: a WSGI application object for the Pyramid application to be
            instrumented by Contrast
        @param registry: (optional) the `pyramid.registry.Registry` instance
            corresponding to the wsgi_app - if not provided, we make a best effort to
            find it on the provided app
        """
        self.registry = (
            registry if registry is not None else _get_registry_or_fail(wsgi_app)
        )
        app_name = self._get_app_name()
        super(PyramidWSGIMiddleware, self).__init__(wsgi_app, app_name)

    def _get_app_name(self):
        try:
            return self.registry.package_name
        except Exception:
            return "Pyramid Application"


def _get_registry_or_fail(wsgi_app):
    registry = safe_getattr(wsgi_app, "registry", None)
    if isinstance(registry, Registry):
        return registry
    msg = (
        "Unable to find pyramid Registry object. "
        "Please provide the Registry as the second argument to ContrastMiddleware"
    )
    logger.error(msg)
    raise RuntimeError(msg)
