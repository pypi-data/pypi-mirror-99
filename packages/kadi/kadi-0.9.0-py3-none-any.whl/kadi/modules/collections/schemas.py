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
from marshmallow import post_load
from marshmallow.validate import Length
from marshmallow.validate import OneOf

from .models import Collection
from kadi.lib.conversion import lower
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.schemas import check_duplicate_identifier
from kadi.lib.schemas import KadiSchema
from kadi.lib.schemas import NonEmptyString
from kadi.lib.schemas import SortedPluck
from kadi.lib.schemas import validate_identifier
from kadi.lib.tags.schemas import TagSchema
from kadi.lib.web import url_for
from kadi.modules.accounts.schemas import UserSchema


class CollectionSchema(KadiSchema):
    """Schema to represent collections.

    See :class:`.Collection`.

    :param previous_collection: (optional) A collection whose identifier should be
        excluded when checking for duplicates while deserializing.
    :param linked_record: (optional) A record that is linked to each collection that
        should be serialized. Will be used to build endpoints for corresponding
        actions.
    """

    id = fields.Integer(required=True)

    identifier = NonEmptyString(
        required=True,
        filters=[lower, strip],
        validate=[
            Length(
                max=Collection.Meta.check_constraints["identifier"]["length"]["max"]
            ),
            validate_identifier,
        ],
    )

    title = NonEmptyString(
        required=True,
        filters=[normalize],
        validate=Length(
            max=Collection.Meta.check_constraints["title"]["length"]["max"]
        ),
    )

    description = fields.String(
        validate=Length(
            max=Collection.Meta.check_constraints["description"]["length"]["max"]
        )
    )

    visibility = fields.String(
        validate=OneOf(Collection.Meta.check_constraints["visibility"]["values"])
    )

    tags = SortedPluck(TagSchema, "name", many=True)

    plain_description = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    state = fields.String(dump_only=True)

    creator = fields.Nested(UserSchema, dump_only=True)

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    def __init__(self, previous_collection=None, linked_record=None, **kwargs):
        super().__init__(**kwargs)
        self.previous_collection = previous_collection
        self.linked_record = linked_record

    @post_load
    def _post_load(self, data, **kwargs):
        check_duplicate_identifier(data, Collection, exclude=self.previous_collection)

        if "tags" in data:
            data["tags"] = list({tag["name"] for tag in data["tags"]})

        return data

    def _generate_links(self, obj):
        links = {
            "self": url_for("api.get_collection", id=obj.id),
            "records": url_for("api.get_collection_records", id=obj.id),
            "user_roles": url_for("api.get_collection_user_roles", id=obj.id),
            "group_roles": url_for("api.get_collection_group_roles", id=obj.id),
            "revisions": url_for("api.get_collection_revisions", id=obj.id),
        }

        if self._internal:
            links["view"] = url_for("collections.view_collection", id=obj.id)

        return links

    def _generate_actions(self, obj):
        actions = {
            "edit": url_for("api.edit_collection", id=obj.id),
            "delete": url_for("api.delete_collection", id=obj.id),
            "link_record": url_for("api.add_collection_record", id=obj.id),
            "add_user_role": url_for("api.add_collection_user_role", id=obj.id),
            "add_group_role": url_for("api.add_collection_group_role", id=obj.id),
        }

        if self.linked_record:
            actions["remove_link"] = url_for(
                "api.remove_record_collection",
                record_id=self.linked_record.id,
                collection_id=obj.id,
            )

        return actions
