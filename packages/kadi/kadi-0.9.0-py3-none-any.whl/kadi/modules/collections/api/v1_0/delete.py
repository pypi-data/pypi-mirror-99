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
from kadi.lib.resources.api import remove_link
from kadi.lib.resources.api import remove_role
from kadi.modules.accounts.models import User
from kadi.modules.collections.core import delete_collection as _delete_collection
from kadi.modules.collections.models import Collection
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import permission_required
from kadi.modules.records.models import Record


route = partial(bp.route, methods=["DELETE"])


@route("/collections/<int:id>")
@permission_required("delete", "collection", "id")
@scopes_required("collection.delete")
@status(204, "Collection deleted successfully.")
def delete_collection(id):
    """Delete the collection specified by the given *id*."""
    collection = Collection.query.get_active_or_404(id)

    _delete_collection(collection)
    db.session.commit()

    return json_response(204)


@route("/collections/<int:collection_id>/records/<int:record_id>")
@permission_required("link", "collection", "collection_id")
@scopes_required("collection.link")
@status(204, "Record successfully removed from collection.")
def remove_collection_record(collection_id, record_id):
    """Remove a record from a collection.

    Will remove the record specified by the given *record_id* from the collection
    specified by the given *collection_id*.
    """
    collection = Collection.query.get_active_or_404(collection_id)
    record = Record.query.get_active_or_404(record_id)

    return remove_link(collection.records, record)


@route("/collections/<int:collection_id>/roles/users/<int:user_id>")
@permission_required("permissions", "collection", "collection_id")
@scopes_required("collection.permissions")
@status(204, "User role successfully removed from collection.")
@status(409, "When trying to remove the creator's role.")
def remove_collection_user_role(collection_id, user_id):
    """Remove a user role from a collection.

    Will remove the role of the user specified by the given *user_id* from the
    collection specified by the given *collection_id*.
    """
    collection = Collection.query.get_active_or_404(collection_id)
    user = User.query.get_or_404(user_id)

    return remove_role(user, collection)


@route("/collections/<int:collection_id>/roles/groups/<int:group_id>")
@permission_required("permissions", "collection", "collection_id")
@scopes_required("collection.permissions")
@status(204, "Group role successfully removed from collection.")
def remove_collection_group_role(collection_id, group_id):
    """Remove a group role from a collection.

    Will remove the role of the group specified by the given *group_id* from the
    collection specified by the given *collection_id*.
    """
    collection = Collection.query.get_active_or_404(collection_id)
    group = Group.query.get_active_or_404(group_id)

    return remove_role(group, collection)
