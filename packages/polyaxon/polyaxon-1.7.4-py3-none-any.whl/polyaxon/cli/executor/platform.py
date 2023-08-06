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

from typing import Dict, List

import click

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.operations import approve
from polyaxon.cli.operations import logs as run_logs
from polyaxon.cli.operations import statuses
from polyaxon.cli.operations import upload as run_upload
from polyaxon.client import RunClient
from polyaxon.managers.run import RunConfigManager
from polyaxon.polyflow import V1CompiledOperation, V1Operation
from polyaxon.utils import cache
from polyaxon.utils.formatting import Printer


def run(
    ctx,
    name: str,
    owner: str,
    project_name: str,
    description: str,
    tags: List[str],
    op_spec: V1Operation,
    log: bool,
    upload: bool,
    upload_to: str,
    upload_from: str,
    watch: bool,
    eager: bool,
):
    if eager and upload:
        Printer.print_error("You can't use upload` and `eager` at the same.")
        sys.exit(1)

    polyaxon_client = RunClient(owner=owner, project=project_name)

    def cache_run(data):
        config = polyaxon_client.client.sanitize_for_serialization(data)
        cache.cache(
            config_manager=RunConfigManager,
            config=config,
            owner=owner,
            project=project_name,
        )

    def create_run(is_managed: bool = True, meta_info: Dict = None):
        is_approved = False if upload else None
        try:
            response = polyaxon_client.create(
                name=name,
                description=description,
                tags=tags,
                content=op_spec,
                is_managed=is_managed,
                is_approved=is_approved,
                meta_info=meta_info,
            )
            Printer.print_success("A new run `{}` was created".format(response.uuid))
            if not eager:
                cache_run(response)
                click.echo(
                    "You can view this run on Polyaxon UI: {}".format(
                        get_dashboard_url(
                            subpath="{}/{}/runs/{}".format(
                                owner, project_name, response.uuid
                            )
                        )
                    )
                )
                return response.uuid
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e,
                message="Could not create a run.",
                http_messages_mapping={
                    404: "Make sure you have a project initialized in your current workdir, "
                    "otherwise you need to pass a project with `-p/--project`. "
                    "The project {}/{} does not exist.".format(owner, project_name)
                },
            )
            sys.exit(1)

    def refresh():
        try:
            polyaxon_client.refresh_data()
        except (ApiException, HTTPError) as e:
            handle_cli_error(
                e, message="The current eager operation does not exist anymore."
            )
            sys.exit(1)

    click.echo("Creating a new run...")
    run_meta_info = {"eager": True} if eager or upload else None
    run_uuid = create_run(not eager, run_meta_info)
    if eager:
        from polyaxon.polyaxonfile.manager import get_eager_matrix_operations

        refresh()
        click.echo("Starting eager mode...")
        compiled_operation = V1CompiledOperation.read(polyaxon_client.run_data.content)
        op_specs = get_eager_matrix_operations(
            content=polyaxon_client.run_data.raw_content,
            compiled_operation=compiled_operation,
            is_cli=True,
        )
        click.echo("Creating {} operations".format(len(op_specs)))
        for op_spec in op_specs:
            create_run()
        return

    ctx.obj = {"project": "{}/{}".format(owner, project_name), "run_uuid": run_uuid}
    if upload:
        ctx.invoke(
            run_upload, path_to=upload_to, path_from=upload_from, sync_failure=True
        )
        ctx.invoke(approve)

    # Check if we need to invoke logs
    if watch and not eager:
        ctx.invoke(statuses, watch=True)

    # Check if we need to invoke logs
    if log and not eager:
        ctx.invoke(run_logs)
