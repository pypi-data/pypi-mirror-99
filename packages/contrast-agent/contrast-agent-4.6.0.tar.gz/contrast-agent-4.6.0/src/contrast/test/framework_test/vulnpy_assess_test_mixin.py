# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

import pytest

from contrast.test.framework_test.base_django_test import BaseDjangoTest
from contrast.test.framework_test_utils import assert_subprocess_popen_finding_events
from contrast.test.contract.findings import (
    validate_finding_in_context,
    validate_ssrf_finding_no_mock,
    remove_redos_findings,
)
from contrast.test.helper import python2_only
from contrast.test.helper import python3_only


class VulnpyAssessTestMixin(object):
    @pytest.mark.xfail(reason="TODO: PYT-1235 No finding reported for cmdi")
    @python3_only
    def test_non_utf8_decoding_cmdi(self):
        """
        param_val a non utf8 encoded string. This is the result of shift_jis encoding of
        '手袋'. This encoding is automatically done by chrome, not in our test client. So
        we manually provide the encoded bytes here.
        """
        trigger = "os-system"
        rule_id = "cmd-injection"
        # Couldn't rely on passing 手袋 in the request because the test client doesn't
        # use shift_jis to encode.
        param_val = b"\x8e\xe8\x91\xdc"
        # Since we fail to decode param_value using utf-8 we rely on replace error
        # handling to get this new string
        expected_value = "���"
        path = "/vulnpy/cmdi/{}".format(trigger)

        self.client.get(path, {"user_input": param_val})

        validate_finding_in_context(self.request_context, rule_id, expected_value)

    @pytest.mark.parametrize("trigger", ["os-system", "subprocess-popen"])
    def test_cmdi(self, trigger):
        user_input = "echo attack"
        self.client.get("/vulnpy/cmdi/{}".format(trigger), {"user_input": user_input})

        validate_finding_in_context(self.request_context, "cmd-injection", user_input)

        if (
            isinstance(self, BaseDjangoTest)
            and trigger == "subprocess-popen"
            and not os.environ.get("USE_WSGI")  # TODO: PYT-1102
        ):
            assert_subprocess_popen_finding_events(
                self.request_context.activity.findings
            )

    @pytest.mark.parametrize(
        "trigger", ["pickle-load", "pickle-loads", "yaml-load", "yaml-load-all"]
    )
    def test_untrusted_deserialization(self, trigger):
        user_input = "some data to deserialize"
        try:
            self.client.get(
                "/vulnpy/deserialization/{}".format(trigger), {"user_input": user_input}
            )
        except Exception:
            # this view function doesn't handle its own errors, so we do it here
            pass

        validate_finding_in_context(
            self.request_context, "untrusted-deserialization", user_input
        )

    @pytest.mark.parametrize("trigger", ["io-open", "open"])
    def test_path_traversal(self, trigger):
        user_input = "does not matter"
        self.client.get("/vulnpy/pt/{}".format(trigger), {"user_input": user_input})

        validate_finding_in_context(self.request_context, "path-traversal", user_input)

    @python2_only
    def test_path_traversal_execfile(self):
        user_input = "does not matter"
        self.client.get("/vulnpy/pt/execfile", {"user_input": user_input})

        validate_finding_in_context(self.request_context, "path-traversal", user_input)

    @pytest.mark.parametrize(
        "trigger", ["sqlite3-execute", "sqlite3-executemany", "sqlite3-executescript"]
    )
    def test_sqli(self, trigger):
        user_input = "any value works"
        self.client.get(
            "/vulnpy/sqli/{}".format(trigger), params={"user_input": user_input}
        )

        # 3 queries per vulnpy request: database reset, attack, fetch results
        assert self.request_context.activity.query_count == 3
        validate_finding_in_context(self.request_context, "sql-injection", user_input)

    @pytest.mark.parametrize(
        "trigger", ["legacy-urlopen", "urlopen-str", "urlopen-obj"]
    )
    @pytest.mark.parametrize("safe", [False, True])
    def test_ssrf_urllib(self, trigger, safe):
        user_input = "not.a.url" if safe else "http://attacker.com/?q=foobar"
        self.client.get("/vulnpy/ssrf/{}".format(trigger), {"user_input": user_input})

        if not safe:
            validate_ssrf_finding_no_mock(trigger, self.request_context)
        else:
            findings = remove_redos_findings(
                self.request_context.activity.findings, "ssrf"
            )
            assert len(findings) == 0

    @pytest.mark.parametrize("trigger_class", ["httpconnection", "httpsconnection"])
    @pytest.mark.parametrize(
        "trigger_method", ["request-method", "putrequest-method", "init"]
    )
    def test_ssrf_httplib(self, trigger_method, trigger_class):
        trigger = "-".join([trigger_class, trigger_method])
        user_input = "www.attacker.com" if trigger_method == "init" else "DELETE"
        self.client.get("/vulnpy/ssrf/{}".format(trigger), {"user_input": user_input})

        validate_ssrf_finding_no_mock(trigger, self.request_context)

    @pytest.mark.parametrize("trigger_class", ["httpconnection", "httpsconnection"])
    @pytest.mark.parametrize("trigger_method", ["request", "putrequest"])
    def test_ssrf_httplib_safe(self, trigger_method, trigger_class):
        """
        HTTP*Connection.*request isn't vulnerable to SSRF via the "url" argument.
        This is because it only takes a path / querystring, which isn't vulnerable
        to ssrf.
        """
        trigger = "-".join([trigger_class, trigger_method, "url"])
        self.client.get("/vulnpy/ssrf/{}".format(trigger), {"user_input": "/some/path"})

        findings = remove_redos_findings(self.request_context.activity.findings, "ssrf")

        assert len(findings) == 0

    @pytest.mark.parametrize("trigger", ["random", "randint", "randrange", "uniform"])
    def test_weak_randomness(self, trigger):
        user_input = "abc123"
        self.client.get("/vulnpy/rand/{}".format(trigger), {"user_input": user_input})

        validate_finding_in_context(
            self.request_context, "crypto-weak-randomness", user_input, nondataflow=True
        )

    @pytest.mark.parametrize("trigger", ["hashlib-md5", "hashlib-sha1", "hashlib-new"])
    def test_insecure_hash(self, trigger):
        self.settings.disabled_assess_rules.discard("crypto-bad-mac")

        user_input = "def456"
        self.client.get("/vulnpy/hash/{}".format(trigger), {"user_input": user_input})

        validate_finding_in_context(
            self.request_context, "crypto-bad-mac", user_input, nondataflow=True
        )

    @pytest.mark.parametrize("trigger", ["exec", "eval", "compile"])
    def test_untrusted_code_exec(self, trigger):
        user_input = "1 + 2 + 3"
        self.client.get(
            "/vulnpy/unsafe_code_exec/{}".format(trigger), {"user_input": user_input}
        )

        validate_finding_in_context(
            self.request_context, "unsafe-code-execution", user_input
        )

    def test_raw_xss(self):
        user_input = "im an attack!"
        self.client.get("/vulnpy/xss/raw", {"user_input": user_input})

        validate_finding_in_context(self.request_context, "reflected-xss", user_input)

    @pytest.mark.parametrize(
        "trigger",
        ["xml-dom-pulldom-parsestring", "lxml-etree-fromstring", "xml-sax-parsestring"],
    )
    def test_xxe(self, trigger):
        user_input = "some input"

        try:
            self.client.get(
                "/vulnpy/xxe/{}".format(trigger), {"user_input": user_input}
            )
        except Exception:
            # this view function doesn't handle its own errors, so we do it here
            pass

        validate_finding_in_context(self.request_context, "xxe", user_input)
