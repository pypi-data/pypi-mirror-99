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

from polyaxon.exceptions import PolyaxonSchemaError


def get_queue_info(queue: str):
    if not queue:
        raise PolyaxonSchemaError("Received an invalid queue {}".format(queue))

    parts = queue.replace(".", "/").split("/")
    agent = None
    queue_name = queue
    if len(parts) == 2:
        agent, queue_name = parts
    elif len(parts) > 2:
        raise PolyaxonSchemaError(
            "Please provide a valid queue. "
            "The queue name should be: queue-name to use the default agent or agent-name/queue."
        )

    return agent, queue_name
