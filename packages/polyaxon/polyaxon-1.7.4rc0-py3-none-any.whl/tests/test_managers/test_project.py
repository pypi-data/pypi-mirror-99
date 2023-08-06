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

from polyaxon_sdk import V1Project

from polyaxon.managers.project import ProjectConfigManager
from tests.utils import BaseTestCase


@pytest.mark.managers_mark
class TestProjectConfigManager(BaseTestCase):
    def test_default_props(self):
        assert ProjectConfigManager.is_all_visibility() is True
        assert ProjectConfigManager.IS_POLYAXON_DIR is True
        assert ProjectConfigManager.CONFIG_FILE_NAME == ".project"
        assert ProjectConfigManager.CONFIG == V1Project
