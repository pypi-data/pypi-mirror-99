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

import sys
import uuid

import click

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import pkg
from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import PolyaxonClient
from polyaxon.constants import NO_AUTH
from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.cli import CliConfigManager
from polyaxon.managers.user import UserConfigManager
from polyaxon.schemas.cli.client_config import ClientConfig
from polyaxon.services.headers import PolyaxonServices
from polyaxon.utils.formatting import Printer
from polyaxon.utils.tz_utils import now
from polyaxon.utils.versions import clean_version_for_compatibility


def session_expired():
    AuthConfigManager.purge()
    UserConfigManager.purge()
    CliConfigManager.purge()
    click.echo("Session has expired, please try again.")
    sys.exit(1)


def get_server_installation(polyaxon_client=None):
    polyaxon_client = polyaxon_client or PolyaxonClient()
    try:
        return polyaxon_client.versions_v1.get_installation(_request_timeout=15)
    except ApiException as e:
        if e.status == 403:
            session_expired()
        handle_cli_error(e, message="Could not get server version.")
    except HTTPError:
        Printer.print_error(
            "Could not connect to remote server to fetch installation version.",
        )


def get_compatibility(
    key: str,
    service: str,
    version: str,
    is_cli: bool = True,
    set_config: bool = True,
):
    if not key:
        installation = CliConfigManager.get_value("installation") or {}
        key = installation.get("key") or uuid.uuid4().hex
    try:
        version = clean_version_for_compatibility(version)
    except Exception as e:
        if set_config:
            CliConfigManager.reset(last_check=now())
        if is_cli:
            handle_cli_error(
                e,
                message="Could parse the version {}.".format(version),
            )
    polyaxon_client = PolyaxonClient(config=ClientConfig(), token=NO_AUTH)
    try:
        return polyaxon_client.versions_v1.get_compatibility(
            uuid=key,
            service=service,
            version=version,
            _request_timeout=2,
        )
    except ApiException as e:
        if e.status == 403 and is_cli:
            session_expired()
        if set_config:
            CliConfigManager.reset(last_check=now())
        if is_cli:
            handle_cli_error(
                e,
                message="Could not reach the compatibility API.",
            )
    except HTTPError:
        if set_config:
            CliConfigManager.reset(last_check=now())
        if is_cli:
            Printer.print_error(
                "Could not connect to remote server to fetch compatibility versions.",
            )
    except Exception as e:
        if set_config:
            CliConfigManager.reset(last_check=now())
        if is_cli:
            Printer.print_error(
                "Unexpected error %s, "
                "could not connect to remote server to fetch compatibility versions."
                % e,
            )


def get_log_handler(polyaxon_client=None):
    polyaxon_client = polyaxon_client or PolyaxonClient()
    try:
        return polyaxon_client.versions_v1.get_log_handler()
    except ApiException as e:
        if e.status == 403:
            session_expired()
        CliConfigManager.reset(last_check=now())
        handle_cli_error(e, message="Could not get cli version.")
    except HTTPError:
        CliConfigManager.reset(last_check=now())
        Printer.print_error("Could not connect to remote server to fetch log handler.")


def set_versions_config(
    polyaxon_client=None,
    set_installation: bool = True,
    set_compatibility: bool = True,
    set_handler: bool = False,
    service=PolyaxonServices.CLI,
    version=pkg.VERSION,
    key: str = None,
    is_cli: bool = True,
):
    polyaxon_client = polyaxon_client or PolyaxonClient()
    server_installation = None
    if set_installation:
        server_installation = get_server_installation(polyaxon_client=polyaxon_client)
        if not key and server_installation and server_installation.key:
            key = server_installation.key
    compatibility = None
    if set_compatibility:
        compatibility = get_compatibility(
            key=key, service=service, version=version, is_cli=is_cli
        )
    log_handler = None
    if set_handler:
        log_handler = get_log_handler(polyaxon_client=polyaxon_client)
    return CliConfigManager.reset(
        last_check=now(),
        current_version=version,
        installation=server_installation.to_dict() if server_installation else {},
        compatibility=compatibility.to_dict() if compatibility else {},
        log_handler=log_handler.to_dict() if log_handler else {},
    )
