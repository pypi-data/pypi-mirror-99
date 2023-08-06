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
import os

from polyaxon import settings
from polyaxon.api import VERSION_V1
from polyaxon.env_vars.keys import POLYAXON_KEYS_PLATFORM_HOST
from polyaxon.exceptions import PolypodException
from polyaxon.polypod.common.env_vars import get_service_env_vars
from polyaxon.polypod.compiler.converters import BaseConverter
from polyaxon.polypod.compiler.converters.base import PlatformConverterMixin
from polyaxon.services.auth import AuthenticationTypes
from polyaxon.services.headers import PolyaxonServiceHeaders, PolyaxonServices
from tests.utils import BaseTestCase


class DummyConverter(PlatformConverterMixin, BaseConverter):
    SPEC_KIND = "dummy"
    API_VERSION = "v1alpha1"
    PLURAL = "dummies"
    GROUP = "dummy"
    K8S_ANNOTATIONS_KIND = "dummies_name"
    K8S_LABELS_COMPONENT = "dummies_component"
    K8S_LABELS_PART_OF = "dummies_part_of"

    def get_main_env_vars(self, external_host: bool = False, **kwargs):
        pass

    def get_resource(self):
        pass


class TestBaseConverter(BaseTestCase):
    SET_AGENT_SETTINGS = True

    def setUp(self):
        super().setUp()
        settings.AGENT_CONFIG.app_secret_name = "polyaxon"
        settings.AGENT_CONFIG.agent_secret_name = "agent"
        settings.CLIENT_CONFIG.host = "https://polyaxon.com"
        self.converter = DummyConverter(
            owner_name="owner-name",
            project_name="project-name",
            run_name="run-name",
            run_uuid="run_uuid",
        )

    def test_get_service_env_vars(self):
        # Call with default
        env_vars = self.converter.get_service_env_vars(service_header=None)
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.SERVICE,
            service_header=None,
            authentication_type=None,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=False,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )

        self.converter.internal_auth = True
        env_vars = self.converter.get_service_env_vars(
            service_header="sa-foo",
            header="header-foo",
            include_secret_key=True,
            include_internal_token=True,
            include_agent_token=False,
            authentication_type="internal",
        )
        assert env_vars == get_service_env_vars(
            header="header-foo",
            service_header="sa-foo",
            authentication_type="internal",
            include_secret_key=True,
            include_internal_token=True,
            include_agent_token=False,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )

        self.converter.internal_auth = False
        env_vars = self.converter.get_service_env_vars(
            service_header="sa-foo",
            header="header-foo",
            authentication_type="internal",
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
        )
        assert env_vars == get_service_env_vars(
            service_header="sa-foo",
            header="header-foo",
            authentication_type="internal",
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        env_vars = self.converter.get_service_env_vars(
            service_header="sa-foo",
            header="header-foo",
            authentication_type="internal",
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
            external_host=True,
        )
        # Default platform host
        assert env_vars == get_service_env_vars(
            service_header="sa-foo",
            header="header-foo",
            authentication_type="internal",
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        # Setting an env var for the POLYAXON_KEYS_PLATFORM_HOST
        current = os.environ.get(POLYAXON_KEYS_PLATFORM_HOST)
        os.environ[POLYAXON_KEYS_PLATFORM_HOST] = "foo"
        env_vars = self.converter.get_service_env_vars(
            service_header="sa-foo",
            header="header-foo",
            authentication_type="internal",
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
            external_host=True,
        )
        assert env_vars == get_service_env_vars(
            service_header="sa-foo",
            header="header-foo",
            authentication_type="internal",
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host="foo",
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        if current:
            os.environ[POLYAXON_KEYS_PLATFORM_HOST] = current
        else:
            del os.environ[POLYAXON_KEYS_PLATFORM_HOST]

        with self.assertRaises(PolypodException):
            self.converter.get_service_env_vars(
                service_header="sa-foo",
                header="header-foo",
                include_secret_key=False,
                include_internal_token=True,
                include_agent_token=True,
                authentication_type="internal",
            )

    def test_get_auth_service_env_vars(self):
        self.converter.internal_auth = True
        env_vars = self.converter.get_auth_service_env_vars()
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.INTERNAL,
            service_header=PolyaxonServices.INITIALIZER,
            authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
            include_secret_key=False,
            include_internal_token=True,
            include_agent_token=False,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )

        self.converter.internal_auth = False
        env_vars = self.converter.get_auth_service_env_vars()
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.SERVICE,
            service_header=PolyaxonServices.INITIALIZER,
            authentication_type=AuthenticationTypes.TOKEN,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        env_vars = self.converter.get_auth_service_env_vars(external_host=True)
        # Default platform host
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.SERVICE,
            service_header=PolyaxonServices.INITIALIZER,
            authentication_type=AuthenticationTypes.TOKEN,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        # Setting an env var for the POLYAXON_KEYS_PLATFORM_HOST
        current = os.environ.get(POLYAXON_KEYS_PLATFORM_HOST)
        os.environ[POLYAXON_KEYS_PLATFORM_HOST] = "foo"
        env_vars = self.converter.get_auth_service_env_vars(external_host=True)
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.SERVICE,
            service_header=PolyaxonServices.INITIALIZER,
            authentication_type=AuthenticationTypes.TOKEN,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=True,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host="foo",
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        if current:
            os.environ[POLYAXON_KEYS_PLATFORM_HOST] = current
        else:
            del os.environ[POLYAXON_KEYS_PLATFORM_HOST]

    def test_get_polyaxon_sidecar_service_env_vars(self):
        self.converter.internal_auth = True
        env_vars = self.converter.get_polyaxon_sidecar_service_env_vars()
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.SERVICE,
            service_header=PolyaxonServices.SIDECAR,
            authentication_type=AuthenticationTypes.TOKEN,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=False,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )

        self.converter.internal_auth = False
        env_vars = self.converter.get_polyaxon_sidecar_service_env_vars()
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.SERVICE,
            service_header=PolyaxonServices.SIDECAR,
            authentication_type=AuthenticationTypes.TOKEN,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=False,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        env_vars = self.converter.get_polyaxon_sidecar_service_env_vars(
            external_host=True
        )
        # Default platform host
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.SERVICE,
            service_header=PolyaxonServices.SIDECAR,
            authentication_type=AuthenticationTypes.TOKEN,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=False,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=settings.CLIENT_CONFIG.host,
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        # Setting an env var for the POLYAXON_KEYS_PLATFORM_HOST
        current = os.environ.get(POLYAXON_KEYS_PLATFORM_HOST)
        os.environ[POLYAXON_KEYS_PLATFORM_HOST] = "foo"
        env_vars = self.converter.get_polyaxon_sidecar_service_env_vars(
            external_host=True
        )
        assert env_vars == get_service_env_vars(
            header=PolyaxonServiceHeaders.SERVICE,
            service_header=PolyaxonServices.SIDECAR,
            authentication_type=AuthenticationTypes.TOKEN,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=False,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host="foo",
            api_version=VERSION_V1,
            run_instance=self.converter.run_instance,
        )
        if current:
            os.environ[POLYAXON_KEYS_PLATFORM_HOST] = current
        else:
            del os.environ[POLYAXON_KEYS_PLATFORM_HOST]
