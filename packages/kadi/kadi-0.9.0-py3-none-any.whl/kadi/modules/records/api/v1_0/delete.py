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

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import status
from kadi.lib.resources.api import remove_link
from kadi.lib.resources.api import remove_role
from kadi.modules.accounts.models import User
from kadi.modules.collections.models import Collection
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import has_permission
from kadi.modules.permissions.core import permission_required
from kadi.modules.records.core import delete_record as _delete_record
from kadi.modules.records.files import delete_file as _delete_file
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.records.models import RecordLink
from kadi.modules.records.models import Upload
from kadi.modules.records.uploads import delete_upload as _delete_upload


route = partial(bp.route, methods=["DELETE"])


@route("/records/<int:id>")
@permission_required("delete", "record", "id")
@scopes_required("record.delete")
@status(204, "Record deleted successfully.")
def delete_record(id):
    """Delete the record specified by the given *id*."""
    record = Record.query.get_active_or_404(id)

    _delete_record(record)
    db.session.commit()

    return json_response(204)


@route("/records/<int:record_id>/records/<int:link_id>")
@permission_required("link", "record", "record_id")
@scopes_required("record.link")
@status(204, "Record link removed successfully.")
def remove_record_link(record_id, link_id):
    """Remove a record link.

    Will remove the (outgoing) record link specified by the given *link_id* from the
    record specified by the given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    record_link = RecordLink.query.get_or_404(link_id)

    if record.id != record_link.record_from_id:
        abort(404)

    if not has_permission(
        current_user, "link", "record", object_id=record_link.record_to_id
    ):
        abort(403)

    db.session.delete(record_link)
    db.session.commit()

    return json_response(204)


@route("/records/<int:record_id>/collections/<int:collection_id>")
@permission_required("link", "record", "record_id")
@scopes_required("record.link")
@status(204, "Record successfully removed from collection.")
def remove_record_collection(record_id, collection_id):
    """Remove a record from a collection.

    Will remove the record specified by the given *record_id* from the collection
    specified by the given *collection_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    collection = Collection.query.get_active_or_404(collection_id)

    return remove_link(record.collections, collection)


@route("/records/<int:record_id>/roles/users/<int:user_id>")
@permission_required("permissions", "record", "record_id")
@scopes_required("record.permissions")
@status(204, "User role successfully removed from record.")
@status(409, "When trying to remove the creator's role.")
def remove_record_user_role(record_id, user_id):
    """Remove a user role from a record.

    Will remove the role of the user specified by the given *user_id* from the record
    specified by the given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    user = User.query.get_or_404(user_id)

    return remove_role(user, record)


@route("/records/<int:record_id>/roles/groups/<int:group_id>")
@permission_required("permissions", "record", "record_id")
@scopes_required("record.permissions")
@status(204, "Group role successfully removed from record.")
def remove_record_group_role(record_id, group_id):
    """Remove a group role from a record.

    Will remove the role of the group specified by the given *group_id* from the record
    specified by the given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    group = Group.query.get_active_or_404(group_id)

    return remove_role(group, record)


@route("/records/<int:record_id>/files/<uuid:file_id>")
@permission_required("update", "record", "record_id")
@scopes_required("record.update")
@status(204, "File deleted successfully.")
def delete_file(record_id, file_id):
    """Delete a file of a record.

    Will delete the file specified by the given *file_id* of the record specified by the
    given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    file = File.query.get_active_or_404(file_id)

    if record.id != file.record.id:
        abort(404)

    _delete_file(file)
    return json_response(204)


@route("/records/<int:record_id>/uploads/<uuid:upload_id>")
@permission_required("update", "record", "record_id")
@scopes_required("record.update")
@status(204, "Upload deleted successfully.")
def delete_upload(record_id, upload_id):
    """Delete an upload of a record.

    Will delete the upload specified by the given *upload_id* of the record specified by
    the given *record_id*. Only uploads owned by the current user can be deleted.
    """
    record = Record.query.get_active_or_404(record_id)
    upload = Upload.query.get_active_or_404(upload_id)

    if record.id != upload.record.id or upload.creator != current_user:
        abort(404)

    _delete_upload(upload)
    db.session.commit()

    return json_response(204)
