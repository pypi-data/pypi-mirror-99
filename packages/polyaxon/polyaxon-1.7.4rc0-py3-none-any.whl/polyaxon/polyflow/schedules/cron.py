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
from datetime import datetime

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.polyflow.schedules.kinds import V1ScheduleKind
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class CronScheduleSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1ScheduleKind.CRON))
    start_at = fields.DateTime(allow_none=True)
    end_at = fields.DateTime(allow_none=True)
    cron = fields.String(required=True)
    max_runs = fields.Int(allow_none=True, validate=validate.Range(min=1))
    depends_on_past = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return V1CronSchedule


class V1CronSchedule(BaseConfig, polyaxon_sdk.V1CronSchedule):
    """Cron schedules is an interface to trigger components repeatedly using a cron definition.

    Args:
        kind: str, should be equal to `cron`
        start_at: datetime, optional
        end_at: datetime, optional
        max_runs: int, optional
        cron: str, required
        depends_on_past: bool, optional


    ## YAML usage

    ```yaml
    >>> schedule:
    >>>   kind:
    >>>   startAt:
    >>>   endAt:
    >>>   maxRuns:
    >>>   cron:
    >>>   dependsOnPast:
    ```

    ## Python usage

    ```python
    >>> from datetime import datetime
    >>> from polyaxon.polyflow import V1CronSchedule
    >>> schedule = V1CronSchedule(
    >>>   start_at=datetime(...),
    >>>   end_at=datetime(...),
    >>>   max_runs=20,
    >>>   cron="0 0 * * *",
    >>>   dependsOnPast=False,
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this schedule is a cron schedule.

    If you are using the python client to create the schedule,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: cron
    ```

    ### startAt

    Optional field to set the start time for kicking the first execution,
    all following executions will be relative to this time.

    ```yaml
    >>> run:
    >>>   startAt: "2019-06-24T21:20:07+00:00"
    ```

    ### endAt

    Optional field to set the end time for stopping this schedule.

    ```yaml
    >>> run:
    >>>   endAt: "2019-06-24T21:20:07+00:00"
    ```

    ### maxRuns

    The maximum number of times to execute the component.
    If used with end date, the schedule will terminate if one of the conditions is met.

    ```yaml
    >>> run:
    >>>   maxRuns: 10
    ```

    ### cron

    The cron expression to generate the component executions.

    ```yaml
    >>> run:
    >>>   cron: "0 0 * * *"
    ```

    ### dependsOnPast

    Optional field to tell Polyaxon to check if the
    previous execution was done before scheduling a new one, by default this is set to `false`.

    ```yaml
    >>> run:
    >>>   dependsOnPast: true
    ```
    """

    SCHEMA = CronScheduleSchema
    IDENTIFIER = V1ScheduleKind.CRON
    REDUCED_ATTRIBUTES = ["startAt", "endAt", "maxRuns", "dependsOnPast"]
