# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re
from contrast.extern import six

from contrast.agent.assess.policy.trigger_actions.default_action import DefaultAction
from contrast.agent.assess.tag import Tag
from contrast.utils.assess.tag_utils import intersection

if six.PY2:
    from urllib2 import Request
else:
    from urllib.request import Request


class SsrfAction(DefaultAction):
    """
    Custom trigger action that implements SSRF rule logic.

    For SSRF, only tag ranges within specific regions of the URL are considered
    to be vulnerable. For a more detailed description, see the dataflow rule
    for SSRF in https://bitbucket.org/contrastsecurity/assess-specifications.
    """

    # Used to parse URLs into components for SSRF post-trigger analysis.
    # This follows the specification, linked above.
    SSRF_REGEX = (
        r"(?P<protocol>http|https|ftp|sftp|telnet|gopher|rtsp|rtsps|ssh|svn):\/\/"
        r"(?P<host>[^\/?]+)(?P<path>\/?[^?]*)(?P<querystring>\?.*)?"
    )

    # Protocol/host (NOT path/querystring) are the labs-approved URL components that trigger SSRF
    VULNERABLE_GROUPS = ["protocol", "host"]

    def find_all_tag_ranges(self, properties, desired_tags):
        vulnerable_tag_ranges = super(SsrfAction, self).find_all_tag_ranges(
            properties, desired_tags
        )
        return self.trim_tag_ranges(properties.origin, vulnerable_tag_ranges)

    def find_any_tag_ranges(self, properties, desired_tags):
        vulnerable_tag_ranges = super(SsrfAction, self).find_any_tag_ranges(
            properties, desired_tags
        )
        return self.trim_tag_ranges(properties.origin, vulnerable_tag_ranges)

    def trim_tag_ranges(self, source, tag_ranges):
        """
        Reduce the span of all vulnerable tags to only cover regions of the source URL
        that are actually vulnerable to SSRF.
        """
        if not isinstance(source, six.string_types):
            return tag_ranges

        match = re.match(self.SSRF_REGEX, source, flags=re.IGNORECASE)

        if match is None:
            return []

        ssrf_tag_ranges = []
        for group in self.VULNERABLE_GROUPS:
            start, end = match.span(group)
            if start != end:
                ssrf_tag_ranges.append(Tag(end - start, start))

        return intersection(tag_ranges, ssrf_tag_ranges)

    def extract_source(self, source):
        """
        In py27, urllib2 provides the url via the Request object's get_full_url() method
        In py37, urllib.request does the same, via full_url()
        """
        if isinstance(source, Request):
            return source.get_full_url() if six.PY2 else source.full_url
        return source
