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
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import permission_required
from kadi.modules.templates.core import delete_template as _delete_template
from kadi.modules.templates.models import Template


route = partial(bp.route, methods=["DELETE"])


@route("/templates/<int:id>")
@permission_required("delete", "template", "id")
@scopes_required("template.delete")
@status(204, "Template deleted successfully.")
def delete_template(id):
    """Delete the template specified by the given *id*."""
    template = Template.query.get_or_404(id)

    _delete_template(template)
    db.session.commit()

    return json_response(204)


@route("/templates/<int:template_id>/roles/users/<int:user_id>")
@permission_required("permissions", "template", "template_id")
@scopes_required("template.permissions")
@status(204, "User role successfully removed from template.")
@status(409, "When trying to remove the creator's role.")
def remove_template_user_role(template_id, user_id):
    """Remove a user role from a template.

    Will remove the role of the user specified by the given *user_id* from the template
    specified by the given *template_id*.
    """
    template = Template.query.get_or_404(template_id)
    user = User.query.get_or_404(user_id)

    return remove_role(user, template)


@route("/templates/<int:template_id>/roles/groups/<int:group_id>")
@permission_required("permissions", "template", "template_id")
@scopes_required("template.permissions")
@status(204, "Group role successfully removed from template.")
def remove_template_group_role(template_id, group_id):
    """Remove a group role from a template.

    Will remove the role of the group specified by the given *group_id* from the
    template specified by the given *template_id*.
    """
    template = Template.query.get_or_404(template_id)
    group = Group.query.get_active_or_404(group_id)

    return remove_role(group, template)
