# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import iteritems
from contrast.api.dtm_pb2 import Finding as FindingDtm
from contrast.utils.string_utils import protobuf_safe

from contrast.agent.policy.constants import (
    CURRENT_FINDING_VERSION,
    MINIMUM_FINDING_VERSION,
)


from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class Finding(object):
    """
    Wrapper around api.dtm_pb2.Finding
    """

    def __init__(self, rule, properties, **kwargs):
        self.finding = FindingDtm()

        rule.add_events_to_finding(self.finding, **kwargs)

        self.finding.rule_id = protobuf_safe(rule.name)

        for key, value in iteritems(properties):
            self.finding.properties[key] = value

        hash_code = rule.generate_preflight_hash(**kwargs)

        self.finding.hash_code = hash_code
        self.finding.preflight = ",".join([rule.name, hash_code])

        logger.debug("Created finding for %s", rule.name)
        logger.debug("initial preflight value: %s", self.finding.preflight)

    def get_finding_msg(self):
        return self.finding

    @staticmethod
    def pick_version(finding):
        """
        Given a finding dtm message, determine the finding version.

        Note:  This is a staticmethod and not applied when the create method is called
        because sometimes the finding version cannot be determined until later in the
        request lifecycle.

        :param finding: instance of dtm_pb2.Finding
        :return: finding version
        """
        # dataflow or non-dataflow finding with route(s)
        if finding.routes:
            return CURRENT_FINDING_VERSION

        # non-dataflow rules without routes
        if not finding.events:
            return CURRENT_FINDING_VERSION

        # dataflow finding without routes
        return MINIMUM_FINDING_VERSION
