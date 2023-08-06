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

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.polyflow.references.mixin import RefMixin
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class UrlRefSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("url_ref"))
    url = fields.Str(required=True)

    @staticmethod
    def schema_config():
        return V1UrlRef


class V1UrlRef(BaseConfig, RefMixin, polyaxon_sdk.V1UrlRef):
    SCHEMA = UrlRefSchema
    IDENTIFIER = "url_ref"

    def get_kind_value(self):
        return self.url
