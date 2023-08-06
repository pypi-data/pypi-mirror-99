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
from functools import partial

from flask import abort
from flask_login import current_user
from flask_login import login_required

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import reqschema
from kadi.lib.api.utils import status
from kadi.lib.resources.api import add_role
from kadi.modules.accounts.models import User
from kadi.modules.groups.core import create_group
from kadi.modules.groups.core import purge_group as _purge_group
from kadi.modules.groups.core import restore_group as _restore_group
from kadi.modules.groups.models import Group
from kadi.modules.groups.schemas import GroupSchema
from kadi.modules.permissions.core import permission_required
from kadi.modules.permissions.schemas import UserRoleSchema

route = partial(bp.route, methods=["POST"])


@route("/groups")
@permission_required("create", "group", None)
@scopes_required("group.create")
@reqschema(GroupSchema(exclude=["id"]), description="The metadata of the new group.")
@status(201, "Return the new group.")
@status(409, "A conflict occured while trying to create the group.")
def new_group(schema):
    """Create a new group."""
    group = create_group(**schema.load_or_400())
    if not group:
        return json_error_response(409, description="Error creating group.")

    db.session.commit()

    return json_response(201, GroupSchema().dump(group))


@route("/groups/<int:id>/members")
@permission_required("members", "group", "id")
@scopes_required("group.members")
@reqschema(
    UserRoleSchema(only=["user.id", "role.name"]),
    description="The member and corresponding role to add.",
)
@status(201, "Member successfully added to group.")
@status(409, "Member already exists.")
def add_group_member(id, schema):
    """Add a member to the group specified by the given *id*."""
    group = Group.query.get_active_or_404(id)
    data = schema.load_or_400()
    user = User.query.get_or_404(data["user"]["id"])

    return add_role(user, group, data["role"]["name"])


@route("/groups/<int:id>/restore")
@login_required
@scopes_required("misc.manage_trash")
@status(200, "Return the restored group.")
def restore_group(id):
    """Restore the deleted group specified by the given *id*.

    Only the creator of a group can restore it.
    """
    group = Group.query.get_or_404(id)

    if group.state != "deleted" or current_user != group.creator:
        abort(404)

    _restore_group(group)
    db.session.commit()

    return json_response(200, GroupSchema().dump(group))


@route("/groups/<int:id>/purge")
@login_required
@scopes_required("misc.manage_trash")
@status(204, "Group purged successfully.")
def purge_group(id):
    """Purge a deleted group specified by the given *id*.

    Will delete the group permanently. Only the creator of a group can permanently
    delete it.
    """
    group = Group.query.get_or_404(id)

    if group.state != "deleted" or current_user != group.creator:
        abort(404)

    _purge_group(group)
    db.session.commit()

    return json_response(204)
