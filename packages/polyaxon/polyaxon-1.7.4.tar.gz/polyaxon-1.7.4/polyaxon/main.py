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

import click
import click_completion

from polyaxon import settings
from polyaxon.cli.admin import admin
from polyaxon.cli.auth import login, logout, whoami
from polyaxon.cli.check import check
from polyaxon.cli.completion import completion
from polyaxon.cli.config import config
from polyaxon.cli.dashboard import dashboard
from polyaxon.cli.hub import hub
from polyaxon.cli.init import init
from polyaxon.cli.operations import ops
from polyaxon.cli.port_forward import port_forward
from polyaxon.cli.projects import project
from polyaxon.cli.registry import registry
from polyaxon.cli.run import run
from polyaxon.cli.session import set_versions_config
from polyaxon.cli.version import check_cli_version, upgrade, version
from polyaxon.logger import clean_outputs, configure_logger
from polyaxon.utils.bool_utils import to_bool
from polyaxon.utils.formatting import Printer

DOCS_GEN = to_bool(os.environ.get("POLYAXON_DOCS_GEN", False))
click_completion.init()


@click.group()
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Turn on debug logging"
)
@click.option(
    "--offline",
    is_flag=True,
    default=False,
    help="Run command in offline mode if supported. "
    "Currently used for run command in --local mode.",
)
@click.pass_context
@clean_outputs
def cli(context, verbose, offline):
    """Polyaxon - Cloud Native Machine Learning Automation & Experimentation tool.

    This CLI provides tools to:

      - Parse, Validate, and Check Polyaxonfiles.

      - Interact with Polyaxon server.

      - Run and Monitor experiments and jobs.

    This CLI tool comes with a caching mechanism:

      - You can initialize a project with: polyaxon init -p [project name]

      - Otherwise Polyaxon will use the default global path for the cache.

    You can check the version of your CLI by running:

      - polyaxon version

    To can check the version of the CLI and the server, and check the compatibility matrix:

      - polyaxon version --check

    To Enable debug mode, you can use the `-v` flag:

      - polyaxon -v ...

    To configure your host:

      - polyaxon config set --host=...

    To check your current config:

      - polyaxon config show

    Common commands:

      - polyaxon project get

      - polyaxon run [-f] [-l]

      - polyaxon ops ls

      - polyaxon ops logs

      - polyaxon ops get

      - polyaxon config set ...

    Admin deployment commands:

      - polyaxon admin deploy [-f] [--check]

      - polyaxon admin upgrade [-f] [--check]

      - polyaxon admin teardown [-f]

    For more information, please visit https://polyaxon.com/docs/core/cli/

    Check the help available for each command listed below by appending `-h`.
    """
    settings.set_cli_config()
    configure_logger(verbose)
    if settings.CLIENT_CONFIG.no_op:
        Printer.print_warning(
            "POLYAXON_NO_OP is set to `true`, some commands will not function correctly."
        )
    context.obj = context.obj or {}
    if not settings.CLIENT_CONFIG.client_header:
        settings.CLIENT_CONFIG.set_cli_header()
    context.obj["offline"] = offline
    if offline:
        os.environ["POLYAXON_IS_OFFLINE"] = "true"
        settings.CLIENT_CONFIG.is_offline = True
    non_check_cmds = [
        "completion",
        "config",
        "version",
        "login",
        "logout",
        "deploy",
        "admin",
        "teardown",
        "docker",
        "initializer",
        "sidecar",
        "proxy",
        "notify",
        "upgrade",
        "port-forward",
    ]
    if not settings.CLI_CONFIG.installation:
        pass
    if (
        not (
            context.invoked_subcommand in non_check_cmds
            or offline
            or settings.CLIENT_CONFIG.no_api
            or settings.CLIENT_CONFIG.is_ops
            or DOCS_GEN
        )
        and not settings.CLI_CONFIG.installation
    ):
        cli_config = set_versions_config(is_cli=False)
        settings.CLI_CONFIG = cli_config
        check_cli_version(cli_config, is_cli=False)


cli.add_command(login)
cli.add_command(logout)
cli.add_command(whoami)
cli.add_command(upgrade)
cli.add_command(version)
cli.add_command(config)
cli.add_command(check)
cli.add_command(init)
cli.add_command(project)
cli.add_command(ops)
cli.add_command(hub)
cli.add_command(registry)
cli.add_command(run)
cli.add_command(dashboard)
cli.add_command(admin)
cli.add_command(port_forward)
cli.add_command(completion)
if settings.CLIENT_CONFIG.is_ops:

    from polyaxon.cli.components.agent import agent
    from polyaxon.cli.components.clean_artifacts import clean_artifacts
    from polyaxon.cli.components.clean_ops import clean_ops
    from polyaxon.cli.components.docker import docker
    from polyaxon.cli.components.initializer import initializer
    from polyaxon.cli.components.notifier import notify
    from polyaxon.cli.components.proxies import proxy
    from polyaxon.cli.components.sidecar import sidecar
    from polyaxon.cli.components.tuner import tuner
    from polyaxon.cli.components.wait import wait

    cli.add_command(agent)
    cli.add_command(clean_artifacts)
    cli.add_command(clean_ops)
    cli.add_command(docker)
    cli.add_command(initializer)
    cli.add_command(notify)
    cli.add_command(proxy)
    cli.add_command(sidecar)
    cli.add_command(tuner)
    cli.add_command(wait)
