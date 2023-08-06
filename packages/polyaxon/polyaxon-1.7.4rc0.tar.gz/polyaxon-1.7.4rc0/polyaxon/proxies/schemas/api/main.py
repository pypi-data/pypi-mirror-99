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

from polyaxon.proxies.schemas.base import get_config

OPTIONS = """
upstream polyaxon {{
  server unix:{root}/web/polyaxon.sock;
}}

server {{
    include polyaxon/polyaxon.base.conf;
}}
"""


def get_main_config(root=None):
    root = root or "/polyaxon"
    return get_config(options=OPTIONS, indent=0, root=root)
