# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class DisableReaction(object):
    ENABLE = "enable"
    MESSAGE = "Contrast received instructions to disable itself - Disabling now"

    @staticmethod
    def run(settings):
        logger.warning(DisableReaction.MESSAGE)

        if settings.config:
            settings.config.put(DisableReaction.ENABLE, False)
