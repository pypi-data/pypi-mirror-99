# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
# pylint: disable=too-many-lines
import copy
import os
import six  # pylint: disable=did-not-import-extern
import sys

import pytest
from app import settings
from app.urls import urlpatterns

import django
from django.utils.html import escape
from contrast.agent.protect.rule.deserialization_rule import Deserialization
from contrast.api.dtm_pb2 import AttackResult, ObservedRoute
from contrast.api.settings_pb2 import ProtectionRule
from contrast.test import mocks

from contrast.test.library_analysis import (
    assert_files_loaded,
    import_sample_package_onefile,
    TEST_MODULES_RELATIVE_IMPORT_DIST,
    TEST_MODULES_NAMESPACE_DIST,
    TEST_MODULE_ONEFILE,
    TEST_MODULES_MULTIPLE_TLDS_DIST,
)

from contrast.test.contract.findings import (
    assert_event_sources,
    param_is_tracked,
    remove_redos_findings,
    validate_finding_in_context,
    validate_source_finding_in_context,
    validate_header_sources,
    validate_cookies_sources,
)
from contrast.test.framework_test_utils import (
    assert_route_appended,
    assert_routes_count,
    current_routes_by_url,
    validate_observed_route,
)

from contrast.test.helper import (
    mock_build_update_messages,
    mock_send_messages,
)
from contrast.test.mongo import skip_no_mongo_db


from contrast.test.helper import python3_only

URLPATTERNS_COPY = copy.copy(urlpatterns)
DATA_DIR = os.path.join(settings.BASE_DIR, os.pardir, "data")

django_ver = django.__version__
django_2_0_1 = django_ver.startswith("2.0") or django_ver.startswith("2.1")

SOURCE_OPTIONS = (
    "parameter",
    "host",
    "port",
    "raw_uri",
    "scheme",
    "referer_header",
)

# full_path_info is only in newer versions of django.
# We do not test full_path* for POST requests since in this case the path does not
# contain a query, and so the entire path is actually sanitized.
GET_SOURCES = (
    SOURCE_OPTIONS
    + ("full_path",)
    + (("full_path_info",) if django.VERSION >= (2, 1) else ())
)
POST_SOURCES = ("files", "body",) + SOURCE_OPTIONS

re_methods = ["match", "search", "finditer", "findall", "sub", "subn", "split"]
re_pattern_methods = [method + "-compiled" for method in re_methods]

REDOS_TRIGGERS = re_methods + re_pattern_methods

if six.PY3:
    REDOS_TRIGGERS.extend(["fullmatch", "fullmatch-compiled"])


class DjangoTestLibraryAnalysisBuiltinImport(object):
    def test_relative_import_hook(self):
        response = self.client.get(
            "/import_package_with_relative_imports/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(
            self.request_context.activity, TEST_MODULES_RELATIVE_IMPORT_DIST
        )

    def test_namespace_sample_package_import_hook(self):
        response = self.client.get(
            "/import_namespace_package/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(self.request_context.activity, TEST_MODULES_NAMESPACE_DIST)

    def test_module_import_onefile(self):
        response = self.client.get(
            "/import_package_onefile/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(self.request_context.activity, TEST_MODULE_ONEFILE)

    def test_sample_module_multiple_tlds(self):
        response = self.client.get(
            "/import_sample_dist_multiple_tlds/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(
            self.request_context.activity, TEST_MODULES_MULTIPLE_TLDS_DIST
        )

    def test_module_already_imported(self):
        import_sample_package_onefile()

        response = self.client.get("/import_package_onefile/")

        assert response.status_code == 200

        assert len(self.request_context.activity.library_usages) == 0


class DjangoProtectNoSqliTestMixin(object):
    """
    Screener does not currently test nosqli protect so we test it more thoroughly.
    """

    def make_nosqli_request(self, method, param_val, with_kwarg):
        self.client.post(
            "/nosqli/",
            {
                "user_input": param_val,
                "method_to_test": method,
                "with_kwarg": with_kwarg,
            },
            status=403,
        )

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_find_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = "Record One"

        self.make_nosqli_request("find", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 1

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_insert_one_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = '{"title": "Record One"}'

        self.make_nosqli_request("insert_one", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 1

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_insert_many_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = "Record One"

        self.make_nosqli_request("insert_many", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 1

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_update_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = "Record One"

        self.make_nosqli_request("update", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 2

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_delete_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = "Record One"

        self.make_nosqli_request("delete", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 1


class DjangoProtectTestMixinBlock(DjangoProtectNoSqliTestMixin):
    """
    Provides test cases to be used across all django protect framework tests
    """

    PROTECT_RULES_MODE_BLOCK = [
        {
            "id": "cmd-injection",
            "name": "Command Injection",
            "mode": ProtectionRule.BLOCK,
        },
        {
            "id": "path-traversal",
            "name": "Path Traversal",
            "mode": ProtectionRule.BLOCK,
        },
        {
            "mode": ProtectionRule.BLOCK,
            "id": Deserialization.NAME,
            "name": "Untrusted Deserialization",
        },
        {"id": "nosql-injection", "name": "NosQLI", "mode": ProtectionRule.BLOCK},
    ]

    @pytest.mark.parametrize("path", ["os-system", "subprocess-popen"])
    def test_cmdi(self, path):
        self.client.get(
            "/vulnpy/cmdi/{}".format(path),
            {"user_input": "; echo /etc/passwd | nc"},
            status=403,
        )
        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "cmd-injection"

    @pytest.mark.parametrize("method_name", ["get", "post"])
    @pytest.mark.parametrize("trigger", ["pickle-load", "pickle-loads"])
    def test_pickle(self, trigger, method_name):
        param_val = "csubprocess\ncheck_output\n(S'ls'\ntR."

        params = dict(user_input=param_val)
        method = getattr(self.client, method_name)

        method("/vulnpy/deserialization/{}".format(trigger), params, status=403)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert (
            self.request_context.activity.results[0].rule_id
            == "untrusted-deserialization"
        )


class DjangoAssessTestMixin(object):
    """
    Provides test cases to be used across all django assess framework tests
    """

    def test_track_django_sources(self):
        param_val = "; echo /etc/passwd | nc"
        response = self.client.get("/vulnpy/cmdi/os-system", {"user_input": param_val})

        assert response is not None
        assert param_is_tracked(param_val)

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

    def test_xss_django_autoescape(self):
        """Autoescaping is enabled by default and should not lead to an xss finding"""
        param_val = "im an attack!"
        response = self.client.get("/xss-autoescape/", {"user_input": param_val})
        assert response.status_code == 200

        findings = remove_redos_findings(self.request_context.activity.findings, "xss")

        assert len(findings) == 0

    def test_xss_django_autoescape_safe(self):
        """
        Autoescaping is enabled but the value is marked as safe in the template
        which prevents it from being escaped. This should result in a finding.
        """
        param_val = "im an attack!"
        response = self.client.get("/xss-autoescape-safe/", {"user_input": param_val})
        assert response.status_code == 200

        validate_finding_in_context(self.request_context, "reflected-xss", param_val)

    def test_xss_django_no_autoescape(self):
        """Autoescaping is disabled so we should get a finding"""
        param_val = "im an attack!"
        response = self.client.get("/xss-no-autoescape/", {"user_input": param_val})
        assert response.status_code == 200

        validate_finding_in_context(self.request_context, "reflected-xss", param_val)

    def test_byte_file_contents_are_tracked(self):
        filename = "logo.png"
        file_path = os.path.join(DATA_DIR, filename)

        self.client.post("/file-contents/", upload_files=[("upload", file_path)])

        assert param_is_tracked(filename)

        contents = open(file_path, "rb").read()
        file_start = contents[:6]
        file_end = contents[-18:]

        # we cannot simply assert param_is_tracked(contents) because the contents
        # are split up into chunks in the string tracker and tracked in these chunks
        assert param_is_tracked(file_start)
        assert param_is_tracked(file_end)

    def test_uce_base64(self):
        # this string is "__import__('os').system('echo hacked')" b64 encoded
        encoded_input = "X19pbXBvcnRfXygnb3MnKS5zeXN0ZW0oJ2VjaG8gaGFja2VkJyk="
        response = self.client.get("/uce-base64/", {"user_input": encoded_input})

        assert response.status_code == 200
        findings = remove_redos_findings(
            self.request_context.activity.findings, "unsafe-code-execution"
        )

        assert len(findings) == 1

        assert findings[0].rule_id == u"unsafe-code-execution"
        assert len(findings[0].events[-1].args) == 1
        # Coincidentally, we base-64 encode our values to send to TS, so we can make
        # this assertion
        assert findings[0].events[-1].args[0].value == encoded_input

    @skip_no_mongo_db
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_find(self, with_kwarg):
        param_val = "book title"
        self.client.post(
            "/nosqli/",
            {
                "user_input": param_val,
                "method_to_test": "find",
                "with_kwarg": with_kwarg,
            },
        )

        validate_finding_in_context(self.request_context, "nosql-injection", param_val)

    @skip_no_mongo_db
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_insert_one(self, with_kwarg):
        values = ("Record One", "PyMongo is fun!", "Dani")
        param_val = (
            '{"title": "'
            + values[0]
            + '", "content": "'
            + values[1]
            + '", "author": "'
            + values[2]
            + '"}'
        )

        self.client.post(
            "/nosqli/",
            {
                "user_input": param_val,
                "method_to_test": "insert_one",
                "with_kwarg": with_kwarg,
            },
        )

        # pymongo rewrites the query quite a bit before trigger time, so we can't assert
        # that the entire query we pass in makes it to the trigger. It's still a pretty
        # good check that one of our query values makes it to the trigger instead. Also,
        # older versions of python have different behavior, so we skip the check when
        # appropriate by setting user_input to an empty string.
        validate_finding_in_context(
            self.request_context,
            "nosql-injection",
            "" if sys.version_info < (3, 6) else values[0],
        )

    @skip_no_mongo_db
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_insert_many(self, with_kwarg):
        example_title = "Record One"
        param_val = (
            '{{"title": "'
            + example_title
            + '", "content": "PyMongo is fun!", "author":'
            ' "Dani"},{"title": "Record Two", "content": "PyMongo is alright",'
            ' "author": "Dani"}}'
        )

        self.client.post(
            "/nosqli/",
            {
                "user_input": param_val,
                "method_to_test": "insert_many",
                "with_kwarg": with_kwarg,
            },
        )

        validate_finding_in_context(
            self.request_context,
            "nosql-injection",
            "" if sys.version_info < (3, 6) else example_title,
        )

    @skip_no_mongo_db
    def test_nosqli_rule_post_update(self):
        param_val = "New Title"

        self.client.post(
            "/nosqli/", {"user_input": param_val, "method_to_test": "update"},
        )

        validate_finding_in_context(
            self.request_context, "nosql-injection", param_val, trigger_arg=1
        )

    @skip_no_mongo_db
    def test_nosqli_rule_post_delete(self):
        param_val = (
            '{"title": "Record One", "content": "PyMongo is fun!", "author": "Dani"}'
        )

        self.client.post(
            "/nosqli/", {"user_input": param_val, "method_to_test": "delete"},
        )

        validate_finding_in_context(self.request_context, "nosql-injection", param_val)

    def test_xss_escaped_no_vuln(self):
        param_val = "<script>alert(1)</script>"
        response = self.client.get(
            "/xss/", {"user_input": param_val, "django_escape": "True"},
        )

        assert response is not None
        assert param_is_tracked(param_val)
        assert param_is_tracked(escape(param_val))

        findings = remove_redos_findings(self.request_context.activity.findings, "xss")

        assert len(findings) == 0

    def test_xss_jinja(self):
        param_val = "im an attack!"
        self.client.get("/xss-jinja/", {"user_input": param_val})

        validate_finding_in_context(self.request_context, "reflected-xss", param_val)

    def test_xss_mako(self):
        if django.VERSION[:1] == (3,):
            pytest.xfail("djangomako is broken in Django 3")

        param_val = "im an attack!"
        self.client.get("/xss-mako/", {"user_input": param_val})

        validate_finding_in_context(self.request_context, "reflected-xss", param_val)

    @pytest.mark.parametrize("route", ["/vulnpy/xss/raw", "/raw-xss-streaming/"])
    def test_xss_raw(self, route):
        param_val = "im an attack!"

        response = self.client.get(route, {"user_input": param_val})
        assert response.status_code == 200

        if "streaming" in route:
            # Make sure that our middleware doesn't consume streaming content
            content = response.body
            assert content == b"<p>Looks like xss: im an attack!</p>"
        else:
            assert "<p>XSS: {}</p>".format(param_val) in str(response.body)

        validate_finding_in_context(self.request_context, "reflected-xss", param_val)

    def test_xss_csv_does_not_send_finding(self):
        param_val = "im an attack!"
        response = self.client.get("/xss-csv/", {"user_input": param_val})

        assert response.status_code == 200

        findings = remove_redos_findings(self.request_context.activity.findings, "xss")

        assert len(findings) == 0

    def test_cmdi_from_filename_and_contents(self):
        filename = "testfile.txt"
        file_path = os.path.join(DATA_DIR, filename)

        self.client.post("/cmdi-file/", upload_files=[("upload", file_path)])

        validate_finding_in_context(self.request_context, "cmd-injection", filename)

        file_contents = (
            b"This file contains extremely dangerous data. Use at your own risk!\n"
        )
        param_is_tracked(file_contents)

    def test_stream_source(self):
        response = self.client.get("/stream-source/")
        assert response.status_code == 200

        # This endpoint is pretty contrived and marks a stream as a source directly.
        # As such, we don't have any user input for validation
        validate_finding_in_context(
            self.request_context, "untrusted-deserialization", "see comment above"
        )

    @pytest.mark.parametrize(
        "trigger_method", REDOS_TRIGGERS,
    )
    def test_redos(self, trigger_method):
        user_input = "anything"

        response = self.client.get(
            "/vulnpy/redos/re-{}".format(trigger_method), {"user_input": user_input},
        )

        assert response.status_code == 200

        regex = "((a)+)+"
        if (
            os.environ.get("USE_WSGI")
            and len(self.request_context.activity.findings) == 2
        ):
            # we see multiple redos findings with django WSGI
            # We only care about the second one
            self.request_context.activity.findings.pop(0)
        validate_finding_in_context(self.request_context, "redos", regex)

    @pytest.mark.parametrize("permanent_redirect", [True, False])
    def test_unvalidated_redirect(self, permanent_redirect):
        """
        By passing a permanent redirect bool flag, we can test that both
        HttpResponsePermanentRedirect and HttpResponseRedirect are patched
        because they inherit from HttpResponseRedirectBase
        """
        redirect_route = "/vulnpy"
        self.client.get(
            "/unvalidated-redirect/",
            {"user_input": redirect_route, "permanent": permanent_redirect},
        )

        validate_finding_in_context(
            self.request_context, "unvalidated-redirect", redirect_route
        )

    def test_preflight_hash_same_request(self):
        """
        Two requests that look exactly the same should generate the same hash
        """
        # This test will pass in isolation on django-1.10.8, but when the full test
        # suite runs, it will not. The findings are both present, but the first one
        # has way more events than the second one for some reason. It seems like
        # something in the test environment is polluting this test state somehow.
        if django.VERSION[:2] == (1, 10):
            pytest.xfail("Known weirdness with events on django-1.10.8 framework test")

        self.client.get("/vulnpy/cmdi/os-system", {"user_input": "first attack"})

        findings = remove_redos_findings(self.request_context.activity.findings, "cmdi")
        assert len(findings) == 1
        first_finding = findings[0]

        self.client.get("/vulnpy/cmdi/os-system", {"user_input": "second attack"})
        findings = remove_redos_findings(self.request_context.activity.findings, "cmdi")
        assert len(findings) == 1
        second_finding = findings[0]

        assert second_finding is not first_finding
        assert second_finding.hash_code == first_finding.hash_code
        assert second_finding.preflight == first_finding.preflight

    def test_preflight_hash_different_requests(self):
        """
        Two different requests that find the same vuln should have different hashes

        In this case, the two requests are the same except one uses GET and the
        other uses POST. Since the HTTP method contributes to the hash, we
        should get different preflight values.
        """
        param_val = "im an attack!"
        self.client.get("/vulnpy/cmdi/subprocess-popen", {"user_input": param_val})

        findings = remove_redos_findings(self.request_context.activity.findings, "cmdi")
        assert len(findings) == 1

        first_finding = findings[0]

        self.client.post("/vulnpy/cmdi/subprocess-popen", {"user_input": param_val})
        findings = remove_redos_findings(self.request_context.activity.findings, "cmdi")
        assert len(findings) == 1
        second_finding = findings[0]

        assert second_finding is not first_finding
        assert second_finding.hash_code != first_finding.hash_code
        assert second_finding.preflight != first_finding.preflight

    def test_preflight_hash_same_request_different_vulns(self):
        """
        The same request that generates two different vulns should have different hashes
        """
        param_val = "im an attack!"
        self.client.get("/two-vulns/", {"user_input": param_val})

        findings = remove_redos_findings(self.request_context.activity.findings, "xss")
        assert len(findings) == 2

        first_finding = self.request_context.activity.findings[0]
        second_finding = self.request_context.activity.findings[1]

        assert second_finding.hash_code != first_finding.hash_code
        assert second_finding.preflight != first_finding.hash_code

    @pytest.mark.xfail(django.VERSION[:2] == (1, 9), reason="TODO: PYT-1050")
    @pytest.mark.parametrize(
        "test_type",
        [
            "create_method",
            "init_direct",
            "filter",
            # TODO: PYT-583 still need to test multi-trigger / multi findings
            "multi-column",
        ],
    )
    @pytest.mark.django_db(transaction=False)
    def test_stored_xss(self, test_type):
        param_val = "hello"
        self.client.get(
            "/stored-xss/", {"user_input": param_val, "test_type": test_type}
        )

        findings = self.request_context.activity.findings

        validate_finding_in_context(self.request_context, "reflected-xss", param_val)

        assert_event_sources(findings, "database", {"database": "TAINTED_DATABASE"})

    @pytest.mark.parametrize("module_name", ["xml", "lxml"])
    def test_xpath_injection(self, module_name):
        query = ".//*[@name='whatever']"
        self.client.get("/xpath-injection/", dict(query=query, module=module_name))

        validate_finding_in_context(self.request_context, "xpath-injection", query)

    @pytest.mark.django_db(transaction=False)
    @pytest.mark.parametrize("method", ["get", "post"])
    def test_sqli_via_django_orm(self, method):
        param_val = "doesnt matter"
        getattr(self.client, method)("/sqli/", {"user_input": param_val})

        validate_finding_in_context(self.request_context, "sql-injection", param_val)


class DjangoAssessTestNondataflowMixin(object):
    def test_crypto_bad_ciphers(self):
        self.client.get("/crypto-bad-ciphers/")

        validate_finding_in_context(
            self.request_context, "crypto-bad-ciphers", None, nondataflow=True
        )


class DjangoRouteCoverageTestMixin(object):
    @mock_build_update_messages
    def test_finds_app_routes(self, build_update_message):
        self.client.get("/vulnpy")

        routes = build_update_message.call_args[0][0]
        cmdi_routes = current_routes_by_url(routes, "vulnpy/cmdi/os-system")
        assert_routes_count(cmdi_routes, 2)

    @mock_build_update_messages
    def test_reports_dynamic_route_in_discovery(self, build_update_message):
        """
        Tests that a dynamically-created route is found because the first request
        made is to the endpoint that creates this route. The dynamically-created
        route is not visited.
        """
        new_view = "new_dynamic"
        original_url_names = [x.name for x in URLPATTERNS_COPY[1:]]
        assert new_view not in original_url_names

        self.client.get("/dynamic_url_view/", {"user_input": new_view})

        routes = build_update_message.call_args[0][0]
        dynamic_routes = current_routes_by_url(routes, new_view)
        assert_routes_count(dynamic_routes, 2)

    @mock_send_messages
    @mock_build_update_messages
    def test_reports_dynamic_route_by_observed_route(
        self, build_update_message, send_messages
    ):
        """
        Tests that a dynamically-created route is found because it is visited. The
        endpoint that created this route was not the first request to the app.
        """
        new_view = "other_dynamic"
        original_url_names = [x.name for x in URLPATTERNS_COPY[1:]]
        assert new_view not in original_url_names
        self.client.get("/")

        routes = build_update_message.call_args[0][0]
        current_routes = current_routes_by_url(routes, new_view)
        # new_dynamic has not been created so it is not found
        assert_routes_count(current_routes, 0)

        assert len(send_messages.call_args[0][0]) == 4

        self.client.get("/dynamic_url_view/?user_input=" + new_view)

        assert len(send_messages.call_args[0][0]) == 3

        new_path = "/" + new_view + "/"
        self.client.get(new_path)
        call_args = send_messages.call_args[0][0]
        assert len(call_args) == 3

        observed_route = call_args[2]
        assert isinstance(observed_route, ObservedRoute)
        assert observed_route.url == new_path
        assert (
            observed_route.signature
            == "contrast.test.framework_test.django_views.other_dynamic(request,)"
        )

    def test_route_appended_to_xss_vuln(self):
        param_val = "im an attack!"
        response = self.client.get("/xss/", {"user_input": param_val})

        assert response
        assert len(self.request_context.activity.findings) > 0
        assert_route_appended(self.request_context.activity.findings, "xss", "GET")

    @pytest.mark.django_db(transaction=False)
    def test_observed_route_appended(self):
        param_val = "im an attack!"
        param_name = "user_input"
        url = "/sqli"
        response = self.client.get(url, {param_name: param_val})

        assert response
        findings = remove_redos_findings(
            self.request_context.activity.findings, "sql-injection"
        )

        assert len(findings) == 1
        validate_observed_route(
            self.request_context, "GET", url[1:], param_name, "PARAMETER"
        )

    @pytest.mark.parametrize("setdefault", ["False", "True"])
    def test_trust_boundary_violation(self, setdefault):
        user_input = "does not matter"

        self.client.get(
            "/trust-boundary-violation/",
            {"user_input": user_input, "setdefault": setdefault},
        )
        findings = remove_redos_findings(
            self.request_context.activity.findings, "trust-boundary-violation"
        )

        # the wsgi middleware is early enough to see a crypto-bad-mac in an earlier middleware
        # the django middleware is last in the middleware stack, so it misses this vulnerability
        if os.environ.get("USE_WSGI"):  # TODO: PYT-1102
            assert len(findings) == 2
        else:
            validate_finding_in_context(
                self.request_context,
                "trust-boundary-violation",
                user_input,
                trigger_arg=1,
            )

    @pytest.mark.skipif(
        not (django.VERSION[:2] == (1, 9) and os.environ.get("USE_WSGI")),
        reason="see comment; only applies to django 1.9 + djangoWSGI",
    )
    def test_django19_source_tagging_196(self):
        """
        There's an unfortunate interaction in django 1.9 using the WSGI-based mdw:

        - in the django 1.9 implementation, only the url-encoded parts of the string are
          explicitly urldecoded. This is unfortunate for us because other parts of the
          string are still tagged as encoded (safe).
        - if the string doesn't have any characters that require url encoding / decoding
          then the entire string is still tagged with the encoded tag
        - this means that for vulnerabilities to trigger with query parameters in django
          1.9, they must have at least one character that is URL-decoded

        This test demonstrates the behavior so that we don't forget about it. It's not
        correct behavior, but fixing it would be quite difficult.
        """
        self.client.get(
            "/xss/", {"user_input": "noUrlDecodableCharactersInThisString"},
        )
        findings = remove_redos_findings(
            self.request_context.activity.findings, "trust-boundary-violation"
        )
        assert len(findings) == 0


class DjangoAssessTestDynamicSourcesMixin(object):

    ATTACK_VALUE = "im an attack!"
    DYNAMIC_SOURCE_RULE_ID = "cmd-injection"

    def set_dangerous_cookie(self):
        self.client.set_cookie("user_input", self.ATTACK_VALUE)

    def test_xss_from_cookie(self):
        self.set_dangerous_cookie()
        self.client.get("/xss-cookie/")

        findings = remove_redos_findings(self.request_context.activity.findings, "xss")
        assert len(findings) == 0

    @pytest.mark.parametrize("source", GET_SOURCES)
    def test_all_get_sources(self, source):

        self.set_dangerous_cookie()
        self.client.get(
            "/dynamic-sources/",
            {"user_input": self.ATTACK_VALUE, "source": source},
            headers={"Referer": "www.python.org"},
        )

        validate_source_finding_in_context(
            self.request_context, self.DYNAMIC_SOURCE_RULE_ID, source,
        )

    @pytest.mark.parametrize("source", POST_SOURCES)
    def test_all_post_sources(self, source):

        self.set_dangerous_cookie()
        if source == "files":
            file_path = os.path.join(DATA_DIR, "testfile.txt")
            self.client.post(
                "/dynamic-sources/",
                {"source": source},
                upload_files=[("user_input", file_path)],
                headers={"Referer": "www.python.org"},
            )

        else:
            self.client.post(
                "/dynamic-sources/",
                {"user_input": self.ATTACK_VALUE, "source": source},
                headers={"Referer": "www.python.org"},
                # **{source: self.ATTACK_VALUE}
            )

        validate_source_finding_in_context(
            self.request_context, self.DYNAMIC_SOURCE_RULE_ID, source,
        )

    def test_cookie_get(self):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.set_dangerous_cookie()
        self.client.get("/cookie-source/")
        validate_cookies_sources(self.request_context.activity.findings)

    def test_cookie_post(self):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.set_dangerous_cookie()
        self.client.post("/cookie-source/")
        validate_cookies_sources(self.request_context.activity.findings)

    @pytest.mark.parametrize(
        "route,source_name",
        [("/header-source/", "header"), ("/header-key-source/", "header_key")],
    )
    @pytest.mark.parametrize("method_name", ["get", "post"])
    @pytest.mark.parametrize("use_environ", [False, True])
    def test_header_source(self, use_environ, method_name, route, source_name):
        method = getattr(self.client, method_name)
        method(route, headers={"Test-Header": "whatever"})

        validate_header_sources(self.request_context.activity.findings, source_name)

    @pytest.mark.parametrize("method_name", ["get", "post"])
    def test_http_method_not_source(self, method_name):
        method = getattr(self.client, method_name)
        method("/dynamic-sources/", dict(source="http_method"))

        findings = remove_redos_findings(self.request_context.activity.findings, "xss")
        assert len(findings) == 0
