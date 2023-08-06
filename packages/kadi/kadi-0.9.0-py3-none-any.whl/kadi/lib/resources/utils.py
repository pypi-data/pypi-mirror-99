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
from flask_login import current_user

from kadi.lib.exceptions import KadiPermissionError
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import has_permission


def add_link(relationship, resource, user=None):
    """Convenience function to link two resources together.

    :param relationship: The many-to-many relationship to append the resource to.
    :param resource: The resource to link, an instance of :class:`.Record` or
        :class:`.Collection`.
    :param user: (optional) The user performing the operation. Defaults to the current
        user.
    :return: ``True`` if the link was established successfully, ``False`` if the link
        already exists.
    :raises KadiPermissionError: If the user performing the operation does not have the
        necessary permission.
    """
    user = user if user is not None else current_user

    if not has_permission(user, "link", resource.__tablename__, resource.id):
        raise KadiPermissionError("No permission to link to other resource.")

    if resource not in relationship:
        relationship.append(resource)
        return True

    return False


def remove_link(relationship, resource, user=None):
    """Convenience function to remove the link between two resources.

    :param relationship: The many-to-many relationship to remove the resource from.
    :param resource: The resource to remove, an instance of :class:`.Record` or
        :class:`.Collection`.
    :param user: (optional) The user performing the operation. Defaults to the current
        user.
    :return: ``True`` if the link was removed successfully, ``False`` if the link does
        not exist.
    :raises KadiPermissionError: If the user performing the operation does not have the
        necessary permission.
    """
    user = user if user is not None else current_user

    if not has_permission(user, "link", resource.__tablename__, resource.id):
        raise KadiPermissionError("No permission to unlink with other resource.")

    if resource in relationship:
        relationship.remove(resource)
        return True

    return False


def get_linked_resources(model, relationship, actions=None, user=None):
    """Convenience function to get all linked resources that a user can access.

    In this context having access to a resource means having read permission for that
    resource.

    :param model: The resource model of which to get the links from, one of
        :class:`.Record` or :class:`.Collection`.
    :param relationship: The many-to-many relationship that represents the linked
        resources to get.
    :param actions: (optional) Further actions to check the access permissions for.
    :param user: (optional) The user that will be checked for access permission.
        Defaults to the current user.
    :return: The resulting query of the linked resources, ordered by their title.
    """
    actions = actions if actions is not None else []
    user = user if user is not None else current_user
    object_name = model.__tablename__

    filter_query = (
        get_permitted_objects(user, "read", object_name)
        .active()
        .with_entities(model.id)
    )

    for action in actions:
        filter_query = (
            get_permitted_objects(user, action, object_name)
            .with_entities(model.id)
            .intersect(filter_query)
        )

    resources_query = relationship.filter(
        model.id.in_(filter_query), model.state == "active"
    ).order_by(model.title)

    return resources_query


def search_resources(
    model, query=None, sort="_score", filter_ids=None, page=1, per_page=10
):
    """Convenience function to query the search index for a specific model.

    Uses :meth:`.SearchableMixin.search` for the given model.

    :param model: The resource model to query, one of :class:`.Record`,
        :class:`.Collection` or :class:`.Group`.
    :param query: (optional) See :meth:`.SearchableMixin.search`.
    :param sort: (optional) The name of a field to sort on. One of ``"_score"``,
        ``"last_modified"``, ``"-last_modified"``, ``"created_at"``, ``"-created_at"``,
        ``"title"``, ``"-title"``, ``"identifier"`` or ``"-identifier"``. Defaults to
        ``"_score"`` if a query is given and to ``"-last_modified"`` otherwise.
    :param filter_ids: (optional) See :meth:`.SearchableMixin.search`.
    :param page: (optional) The current page.
    :param per_page: (optional) Search results per page.
    :return: A tuple containing a list of the search results and the total amount of
        hits.
    """
    start = (page - 1) * per_page
    end = start + per_page
    filter_ids = filter_ids if filter_ids is not None else []

    # We assume all models index those fields and they are sortable.
    if sort not in [
        "_score",
        "last_modified",
        "-last_modified",
        "created_at",
        "-created_at",
        "title",
        "-title",
        "identifier",
        "-identifier",
    ]:
        sort = "_score"

    if sort == "_score":
        if not query:
            sort = "-last_modified"
        else:
            # Sort by score first and by last_modified second.
            sort = ["_score", "-last_modified"]

    elif sort in ["title", "-title", "identifier", "-identifier"]:
        # We need to use the keyword field to sort by text property.
        sort += ".keyword"

    return model.search(
        query=query, sort=sort, filter_ids=filter_ids, start=start, end=end
    )
