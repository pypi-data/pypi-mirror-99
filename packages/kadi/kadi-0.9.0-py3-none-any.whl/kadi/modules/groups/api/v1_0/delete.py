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

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import status
from kadi.lib.resources.api import remove_role
from kadi.modules.accounts.models import User
from kadi.modules.groups.core import delete_group as _delete_group
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import permission_required


route = partial(bp.route, methods=["DELETE"])


@route("/groups/<int:id>")
@permission_required("delete", "group", "id")
@scopes_required("group.delete")
@status(204, "Group deleted successfully.")
def delete_group(id):
    """Delete the group specified by the given *id*."""
    group = Group.query.get_active_or_404(id)

    _delete_group(group)
    db.session.commit()

    return json_response(204)


@route("/groups/<int:group_id>/members/<int:user_id>")
@permission_required("members", "group", "group_id")
@scopes_required("group.members")
@status(204, "Member successfully removed from group.")
@status(409, "When trying to remove the creator.")
def remove_group_member(group_id, user_id):
    """Remove a member from a group.

    Will remove the member specified by the given *user_id* from the group specified by
    the given *group_id*.
    """
    group = Group.query.get_active_or_404(group_id)
    user = User.query.get_or_404(user_id)

    return remove_role(user, group)
