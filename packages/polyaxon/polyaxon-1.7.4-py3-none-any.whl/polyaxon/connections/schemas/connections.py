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

from marshmallow import INCLUDE, ValidationError, fields, post_dump

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig, BaseOneOfSchema


class BucketConnectionSchema(BaseCamelSchema):
    bucket = fields.Str(required=True)

    @staticmethod
    def schema_config():
        return V1BucketConnection


class V1BucketConnection(BaseConfig, polyaxon_sdk.V1BucketConnection):
    SCHEMA = BucketConnectionSchema
    IDENTIFIER = "bucket"

    def patch(self, schema: "V1BucketConnection"):
        self.bucket = schema.bucket or self.bucket


class ClaimConnectionSchema(BaseCamelSchema):
    volume_claim = fields.Str(required=True)
    mount_path = fields.Str(required=True)
    read_only = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return V1ClaimConnection


class V1ClaimConnection(BaseConfig, polyaxon_sdk.V1ClaimConnection):
    SCHEMA = ClaimConnectionSchema
    IDENTIFIER = "volume_claim"

    def patch(self, schema: "V1ClaimConnection"):
        self.volume_claim = schema.volume_claim or self.volume_claim
        self.mount_path = schema.mount_path or self.mount_path
        self.read_only = schema.read_only or self.read_only


class HostPathConnectionSchema(BaseCamelSchema):
    host_path = fields.Str(required=True)
    mount_path = fields.Str(required=True)
    read_only = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HostPathConnection


class V1HostPathConnection(BaseConfig, polyaxon_sdk.V1HostPathConnection):
    SCHEMA = HostPathConnectionSchema
    IDENTIFIER = "host_path"

    def patch(self, schema: "V1HostPathConnection"):
        self.host_path = schema.host_path or self.host_path
        self.mount_path = schema.mount_path or self.mount_path
        self.read_only = schema.read_only or self.read_only


class HostConnectionSchema(BaseCamelSchema):
    url = fields.Str(required=True)
    insecure = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HostConnection


class V1HostConnection(BaseConfig, polyaxon_sdk.V1HostConnection):
    SCHEMA = HostConnectionSchema
    IDENTIFIER = "host"

    def patch(self, schema: "V1HostConnection"):
        self.url = schema.url or self.url
        self.insecure = schema.insecure or self.insecure


class GitConnectionSchema(BaseCamelSchema):
    url = fields.Str(allow_none=True)
    revision = fields.Str(allow_none=True)
    flags = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1GitConnection


class V1GitConnection(BaseConfig, polyaxon_sdk.V1GitConnection):
    SCHEMA = GitConnectionSchema
    IDENTIFIER = "git"
    REDUCED_ATTRIBUTES = ["url", "revision", "flags"]

    def get_name(self):
        if self.url:
            return self.url.split("/")[-1].split(".")[0]
        return None

    def patch(self, schema: "GitConnectionSchema"):
        self.url = schema.url or self.url
        self.revision = schema.revision or self.revision
        self.flags = schema.flags or self.flags


class CustomConnectionSchema(BaseCamelSchema):
    class Meta(BaseCamelSchema.Meta):
        unknown = INCLUDE

    @staticmethod
    def schema_config():
        return V1CustomConnection

    @post_dump(pass_original=True)
    def unmake_custom(self, data, obj, **kwargs):
        value = self.schema_config().remove_reduced_attrs(data)
        value.update({k: getattr(obj, k) for k in obj._schema_keys})
        return value


class V1CustomConnection(BaseConfig):
    UNKNOWN_BEHAVIOUR = INCLUDE
    IDENTIFIER = "custom"
    SCHEMA = CustomConnectionSchema

    def __init__(self, **kwargs):
        self._schema_keys = set([])
        for k, v in kwargs.items():
            self._schema_keys.add(k)
            self.__setattr__(k, v)

    @classmethod
    def from_dict(cls, value, unknown=None, partial: bool = False):
        return super().from_dict(
            value=value, unknown=cls.UNKNOWN_BEHAVIOUR, partial=partial
        )

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1CustomConnection):
            return False

        return self.to_dict() == other.to_dict()

    def patch_git(self, schema: "GitConnectionSchema"):
        if schema.url:
            if "url" not in self._schema_keys:
                self._schema_keys.add("url")
            setattr(self, "url", schema.url)
        if schema.revision:
            if "revision" not in self._schema_keys:
                self._schema_keys.add("revision")
            setattr(self, "revision", schema.revision)

        if schema.flags:
            if "flags" not in self._schema_keys:
                self._schema_keys.add("flags")
            setattr(self, "flags", schema.flags)


def validate_connection(kind, definition):
    if kind not in V1ConnectionKind.allowable_values:
        raise ValidationError("Connection with kind {} is not supported.".format(kind))

    if kind in V1ConnectionKind.BLOB_VALUES:
        V1BucketConnection.from_dict(definition)

    if kind == V1ConnectionKind.VOLUME_CLAIM:
        V1ClaimConnection.from_dict(definition)

    if kind == V1ConnectionKind.HOST_PATH:
        V1HostPathConnection.from_dict(definition)

    if kind == V1ConnectionKind.REGISTRY:
        V1HostConnection.from_dict(definition)

    if kind == V1ConnectionKind.GIT:
        V1GitConnection.from_dict(definition)


class ConnectionSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = True
    UNKNOWN_BEHAVIOUR = INCLUDE

    class Meta:
        unknown = INCLUDE

    SCHEMAS = {
        V1BucketConnection.IDENTIFIER: BucketConnectionSchema,
        V1ClaimConnection.IDENTIFIER: ClaimConnectionSchema,
        V1HostPathConnection.IDENTIFIER: HostPathConnectionSchema,
        V1HostConnection.IDENTIFIER: HostConnectionSchema,
        V1GitConnection.IDENTIFIER: GitConnectionSchema,
        V1CustomConnection.IDENTIFIER: CustomConnectionSchema,
    }
