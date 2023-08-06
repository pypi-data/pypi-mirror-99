# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import io
import os
import sys
from collections import Counter

import mock
import pytest
from contrast.extern import six


python2_only = pytest.mark.skipif(sys.version_info[0] > 2, reason="Python 2 only")
python3_only = pytest.mark.skipif(sys.version_info[0] < 3, reason="Python 3 only")
skip_if_python39 = pytest.mark.skipif(
    sys.version_info[:2] == (3, 9), reason="Not supported on Python 3.9"
)


class SimpleFile(object):
    name = "my_file.txt"
    filename = "my_file.txt"
    file = io.BytesIO(b"hello world")


SIMPLE_REQUEST = {
    "HTTP_USER_AGENT": "",
    "wsgi.url_scheme": "http",
    "HTTP_HOST": "google.com",
    "PATH_INFO": "/bing",
    "HTTP_COOKIE": "",
    "QUERY_STRING": "",
    "REMOTE_ADDR": "127.0.0.1",
    "wsgi.input": io.BytesIO(b""),
    "wsgi.errors": io.BytesIO(b""),
    "REQUEST_METHOD": "GET",
    "SERVER_PORT": 8000,
    "SERVER_PROTOCOL": "HTTP/1.1",
}


def get_simple_request():
    return SIMPLE_REQUEST.copy()


def printable_vector(vector):
    if six.PY2:
        return vector.encode("utf-8")

    return vector


skipInCI = pytest.mark.skipif(
    os.environ.get("CI", "") == "true", reason="Bitbucket pipelines symlink"
)

mock_build_update_messages = mock.patch(
    "contrast.agent.service_client.build_update_message"
)

mock_send_messages = mock.patch("contrast.agent.service_client.send_messages")


def compare_two_lists(a, b):
    return Counter(a) == Counter(b)


SETTINGS_LOC = "contrast.agent.settings_state.SettingsState"
protect_enabled = mock.patch(SETTINGS_LOC + ".is_protect_enabled", return_value=True)
assess_enabled = mock.patch(SETTINGS_LOC + ".is_assess_enabled", return_value=True)
protect_disabled = mock.patch(SETTINGS_LOC + ".is_protect_enabled", return_value=False)
assess_disabled = mock.patch(SETTINGS_LOC + ".is_assess_enabled", return_value=False)


@pytest.fixture(autouse=True)
def disable_library_analysis(mocker):
    mocker.patch(
        "contrast.agent.middlewares.base_middleware.BaseMiddleware.initialize_libraries"
    )
