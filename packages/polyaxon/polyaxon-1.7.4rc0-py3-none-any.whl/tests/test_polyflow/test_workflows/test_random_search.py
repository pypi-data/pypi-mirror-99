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

from marshmallow.exceptions import ValidationError

from polyaxon.polyflow import V1RunKind
from polyaxon.polyflow.matrix.random_search import V1RandomSearch
from polyaxon.polyflow.operations import V1CompiledOperation
from tests.utils import BaseTestCase, assert_equal_dict


@pytest.mark.workflow_mark
class TestWorkflowV1RandomSearch(BaseTestCase):
    def test_random_search_config(self):
        config_dict = {
            "kind": "random",
            "numRuns": 10,
            "params": {"lr": {"kind": "choice", "value": [[0.1], [0.9]]}},
        }
        config = V1RandomSearch.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["numRuns"] = -5
        with self.assertRaises(ValidationError):
            V1RandomSearch.from_dict(config_dict)

        config_dict["numRuns"] = -0.5
        with self.assertRaises(ValidationError):
            V1RandomSearch.from_dict(config_dict)

        # Add n_runs percent
        config_dict["numRuns"] = 0.5
        with self.assertRaises(ValidationError):
            V1RandomSearch.from_dict(config_dict)

        config_dict["numRuns"] = 5
        config = V1RandomSearch.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_random_search_without_num_runs(self):
        config_dict = {
            "kind": "compiled_operation",
            "matrix": {
                "kind": "random",
                "concurrency": 1,
                "params": {"lr": {"kind": "choice", "value": [1, 2, 3]}},
                "seed": 1,
                "earlyStopping": [],
            },
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        with self.assertRaises(ValidationError):
            V1CompiledOperation.from_dict(config_dict)

        config_dict["matrix"]["numRuns"] = 10
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict
