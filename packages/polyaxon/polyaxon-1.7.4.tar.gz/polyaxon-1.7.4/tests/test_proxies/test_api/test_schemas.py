#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from polyaxon.proxies.schemas.locations import get_api_locations_config
from tests.utils import BaseTestCase


@pytest.mark.proxies_mark
class TestApiSchemas(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_api_locations(self):
        expected = """
location /static/ {
    alias /static/v1/;
    autoindex on;
    expires                   30d;
    add_header                Cache-Control private;
    gzip_static on;
}


location /tmp/ {
    alias                     /tmp/;
    expires                   0;
    add_header                Cache-Control private;
    internal;
}
"""  # noqa
        assert get_api_locations_config() == expected
