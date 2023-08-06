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

from polyaxon.polypod.compiler.converters.base import PlatformConverterMixin
from polyaxon.polypod.compiler.converters.job import JobConverter
from polyaxon.polypod.mixins import (
    CleanerMixin,
    NotifierMixin,
    TunerMixin,
    WatchDogMixin,
)
from polyaxon.utils.fqn_utils import (
    get_cleaner_instance,
    get_cleaner_resource_name,
    get_notifier_instance,
    get_notifier_resource_name,
    get_tuner_instance,
    get_tuner_resource_name,
    get_watchdog_instance,
    get_watchdog_resource_name,
)


class NotifierConverter(NotifierMixin, JobConverter):
    def get_instance(self):
        return get_notifier_instance(
            owner=self.owner_name, project=self.project_name, run_uuid=self.run_uuid
        )

    def get_resource_name(self):
        return get_notifier_resource_name(self.run_uuid)


class CleanerConverter(CleanerMixin, JobConverter):
    def get_instance(self):
        return get_cleaner_instance(
            owner=self.owner_name, project=self.project_name, run_uuid=self.run_uuid
        )

    def get_resource_name(self):
        return get_cleaner_resource_name(self.run_uuid)


class TunerConverter(TunerMixin, JobConverter):
    def get_instance(self):
        return get_tuner_instance(
            owner=self.owner_name, project=self.project_name, run_uuid=self.run_uuid
        )

    def get_resource_name(self):
        return get_tuner_resource_name(self.run_uuid)


class WatchDogConverter(WatchDogMixin, JobConverter):
    def get_instance(self):
        return get_watchdog_instance(
            owner=self.owner_name, project=self.project_name, run_uuid=self.run_uuid
        )

    def get_resource_name(self):
        return get_watchdog_resource_name(self.run_uuid)


class PlatformNotifierConverter(PlatformConverterMixin, NotifierConverter):
    pass


class PlatformCleanerConverter(PlatformConverterMixin, CleanerConverter):
    pass


class PlatformTunerConverter(PlatformConverterMixin, TunerConverter):
    pass


class PlatformWatchDogConverter(PlatformConverterMixin, WatchDogConverter):
    pass
