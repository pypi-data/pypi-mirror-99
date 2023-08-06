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

from kadi.lib.schemas import KadiSchema
from kadi.lib.web import url_for


class AccessTokenScopeSchema(KadiSchema):
    """Schema to represent access token scopes.

    See :class:`.AccessTokenScope`.
    """

    object = fields.String(dump_only=True)

    action = fields.String(dump_only=True)


class AccessTokenSchema(KadiSchema):
    """Schema to represent personal access tokens.

    See :class:`.AccessToken`.
    """

    id = fields.Integer(dump_only=True)

    name = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    expires_at = fields.DateTime(dump_only=True)

    is_expired = fields.Boolean(dump_only=True)

    last_used = fields.DateTime(dump_only=True)

    scopes = fields.Nested(AccessTokenScopeSchema, many=True, dump_only=True)

    _actions = fields.Method("_generate_actions")

    def _generate_actions(self, obj):
        return {"remove": url_for("api.remove_access_token", id=obj.id)}
