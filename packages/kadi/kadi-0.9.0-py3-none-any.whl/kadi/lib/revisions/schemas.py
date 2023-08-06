# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from marshmallow import fields
from marshmallow import post_dump

from .utils import get_revision_columns
from kadi.lib.schemas import KadiSchema
from kadi.lib.web import url_for
from kadi.modules.accounts.schemas import UserSchema


class RevisionSchema(KadiSchema):
    """Schema to represent general revisions.

    See :class:`.Revision`.
    """

    timestamp = fields.DateTime(dump_only=True)

    user = fields.Nested(UserSchema, dump_only=True)


class ObjectRevisionSchema(KadiSchema):
    """Schema to represent specific object revisions.

    See :class:`.Revision`.

    :param schema: (optional) The schema to represent the revisioned object with.
    :param api_endpoint: (optional) An API endpoint to get the current object revision.
    :param view_endpoint: (optional) An endpoint to view the current object revision.
        Only relevant for internal usage.
    :param endpoint_args: (optional) Additional keyword arguments to append to the API
        and/or view endpoints when building the corresponding URL.
    :param view_object_url: (optional) A URL to view the actual object the current
        revision refers to. Only relevant for internal usage.
    """

    id = fields.Integer(dump_only=True)

    revision = fields.Nested(RevisionSchema, dump_only=True)

    object_id = fields.Method("_generate_object_id")

    data = fields.Method("_generate_data")

    diff = fields.Method("_generate_diff")

    _links = fields.Method("_generate_links")

    def __init__(
        self,
        schema=None,
        api_endpoint=None,
        view_endpoint=None,
        endpoint_args=None,
        view_object_url=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.schema = schema
        self.api_endpoint = api_endpoint
        self.view_endpoint = view_endpoint
        self.endpoint_args = endpoint_args if endpoint_args is not None else {}
        self.view_object_url = view_object_url

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "data" in data and data["data"] is None:
            del data["data"]

        if "diff" in data and data["diff"] is None:
            del data["diff"]

        if "_links" in data and data["_links"] is None:
            del data["_links"]

        return data

    def _generate_object_id(self, obj):
        return getattr(obj, obj._model_class.__tablename__ + "_id")

    def _generate_data(self, obj):
        if self.schema:
            cols, rels = get_revision_columns(obj._model_class)
            schema = self.schema(only=cols + [rel[0] for rel in rels])
            return schema.dump(obj)

        return None

    def _generate_diff(self, obj):
        if self.schema:
            cols, rels = get_revision_columns(obj._model_class)
            schema = self.schema(only=cols + [rel[0] for rel in rels])

            data = schema.dump(obj)
            prev_data = schema.dump(obj.parent) if obj.parent else {}

            diff = {}
            for key, value in data.items():
                prev_value = prev_data.get(key)

                # A simple comparison should be sufficient after the deserialization.
                if value != prev_value:
                    diff[key] = {"new": value, "prev": prev_value}

            return diff

        return None

    def _generate_links(self, obj):
        if self.api_endpoint or (
            self._internal and (self.view_endpoint or self.view_object_url)
        ):
            links = {}

            if self.api_endpoint:
                links["self"] = url_for(
                    self.api_endpoint, revision_id=obj.id, **self.endpoint_args
                )

            if self._internal:
                if self.view_endpoint:
                    links["view"] = url_for(
                        self.view_endpoint, revision_id=obj.id, **self.endpoint_args
                    )

                if self.view_object_url:
                    links["view_object"] = self.view_object_url

            return links

        return None
