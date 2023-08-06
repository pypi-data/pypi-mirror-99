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

from datetime import datetime
from typing import Optional

from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS_FORMAT,
    CONTEXT_MOUNT_ARTIFACTS_RELATED,
    CONTEXT_MOUNT_ARTIFACTS_RELATED_FORMAT,
)
from polyaxon.stores.manager import get_artifacts_connection, upload_file_or_dir
from polyaxon.utils.date_utils import path_last_modified


def sync_artifacts(last_check: Optional[datetime], run_uuid: str):
    connection_type = get_artifacts_connection()
    path_from = CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_uuid)
    new_check = path_last_modified(path_from)
    # check if there's a path to sync
    if os.path.exists(path_from):
        path_to = os.path.join(connection_type.store_path, run_uuid)

        upload_file_or_dir(
            path_from=path_from,
            path_to=path_to,
            is_file=False,
            workers=5,
            last_time=last_check,
            connection_type=connection_type,
            exclude=["plxlogs"],
        )

    # Check if this run has trigger some related run paths
    if os.path.exists(CONTEXT_MOUNT_ARTIFACTS_RELATED):
        for sub_path in os.listdir(CONTEXT_MOUNT_ARTIFACTS_RELATED):
            # check if there's a path to sync
            path_from = CONTEXT_MOUNT_ARTIFACTS_RELATED_FORMAT.format(sub_path)
            if os.path.exists(path_from):
                path_to = os.path.join(connection_type.store_path, sub_path)

                upload_file_or_dir(
                    path_from=path_from,
                    path_to=path_to,
                    is_file=False,
                    workers=5,
                    last_time=last_check,
                    connection_type=connection_type,
                )

    return new_check
