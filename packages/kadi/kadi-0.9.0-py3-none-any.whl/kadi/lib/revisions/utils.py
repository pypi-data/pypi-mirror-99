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
from kadi.ext.db import db
from kadi.lib.revisions.models import Revision


def delete_revisions(obj):
    """Delete all revisions of an object.

    :param obj: The object to delete the revisions of.
    """
    # Delete the object revisions first.
    revision_ids = []
    for obj_revision in obj.revisions:
        revision_ids.append(obj_revision.revision_id)
        db.session.delete(obj_revision)

    # And then the corresponding base revision objects.
    for revision in Revision.query.filter(Revision.id.in_(revision_ids)):
        db.session.delete(revision)


def get_revision_columns(model):
    """Parse the list of revision columns for a specific model.

    See also :func:`kadi.lib.revisions.core.setup_revisions`.

    :param model: The model to get the columns from.
    :return: A tuple containing a list of the simple columns (i.e. no relationships) as
        string and a list of relationships. The second list itself is made up of tuples
        consisting of the name of the relationship and a list of colums of the
        relationship to revision as strings, similar to the first list.
    """
    columns = []
    relationships = []

    for value in model.Meta.revision:
        if "[" in value and "]" in value:
            start = value.index("[")
            end = value.index("]")

            relationship = value[:start]
            attrs = value[start + 1 : end].split(",")
            attrs = [attr.strip() for attr in attrs]

            relationships.append((relationship, attrs))
        else:
            columns.append(value)

    return columns, relationships
