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

from polyaxon.deploy.operators.cmd_operator import CmdOperator


class PipOperator(CmdOperator):
    CMD = "pip"

    @classmethod
    def params(cls, args):
        params = [cls.CMD] + args
        return params

    @classmethod
    def check(cls):
        command_exist = cls.execute(args=["-V"])
        if not command_exist:
            return False
        return True

    @classmethod
    def execute(cls, args, stream=False):
        params = cls.params(args)
        return cls._execute(params=params, env=None, stream=stream)
