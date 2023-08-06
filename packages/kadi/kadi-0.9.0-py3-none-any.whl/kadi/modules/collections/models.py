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
from kadi.lib.db import generate_check_constraints
from kadi.lib.db import TimestampMixin
from kadi.lib.search.core import SearchableMixin
from kadi.lib.tags.core import TaggingMixin
from kadi.lib.utils import SimpleReprMixin


class Collection(
    SimpleReprMixin, SearchableMixin, TimestampMixin, TaggingMixin, db.Model
):
    """Model to represent record collections."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "user_id", "identifier", "state", "visibility"]
        """See :class:`.SimpleReprMixin`."""

        search_mapping = "kadi.modules.collections.mappings.CollectionMapping"
        """See :class:`.SearchableMixin`."""

        revision = [
            "identifier",
            "title",
            "description",
            "state",
            "visibility",
            "tags[name]",
        ]
        """See :func:`kadi.lib.revisions.core.setup_revisions`."""

        permissions = {
            "actions": [
                ("read", "View this collection."),
                ("update", "Edit this collection."),
                ("link", "Manage links of this collection with other resources."),
                ("permissions", "Manage permissions of this collection."),
                ("delete", "Delete this collection."),
            ],
            "roles": [
                ("member", ["read"]),
                ("editor", ["read", "update", "link"]),
                ("admin", ["read", "update", "link", "permissions", "delete"]),
            ],
            "default_permissions": {"read": {"visibility": "public"}},
            "global_actions": [
                ("create", "Create collections."),
                ("read", "View any collection."),
                ("update", "Edit any collection."),
                ("link", "Manage links of any collection with other resources."),
                ("permissions", "Manage permissions of any collection."),
                ("delete", "Delete any collection."),
            ],
        }
        """Possible permissions and roles for collections.

        See :mod:`kadi.modules.permissions`.
        """

        check_constraints = {
            "identifier": {"length": {"max": 50}},
            "title": {"length": {"max": 150}},
            "description": {"length": {"max": 10000}},
            "state": {"values": ["active", "deleted"]},
            "visibility": {"values": ["private", "public"]},
        }
        """See :func:`kadi.lib.db.generate_check_constraints`."""

    __tablename__ = "collection"

    __table_args__ = generate_check_constraints(Meta.check_constraints)

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the collection, auto incremented."""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    """The ID of the user that created the collection."""

    identifier = db.Column(db.Text, index=True, unique=True, nullable=False)
    """The unique identifier of the collection.

    Restricted to a maximum length of 50 characters.
    """

    title = db.Column(db.Text, nullable=False)
    """The title of the collection.

    Restricted to a maximum length of 150 characters.
    """

    description = db.Column(db.Text, nullable=False)
    """The description of the collection.

    Restricted to a maximum length of 10,000 characters.
    """

    plain_description = db.Column(db.Text, nullable=False)
    """The plain description of the collection.

    Equal to the normal description with the difference that most markdown is stripped
    out.
    """

    state = db.Column(db.Text, index=True, nullable=False)
    """The state of the collection.

    One of ``"active"`` or ``"deleted"``.
    """

    visibility = db.Column(db.Text, index=True, nullable=False)
    """The default visibility of the collection.

    One of ``"private"`` or ``"public"``.
    """

    creator = db.relationship("User", back_populates="collections")

    records = db.relationship(
        "Record",
        secondary="record_collection",
        lazy="dynamic",
        back_populates="collections",
    )

    tags = db.relationship(
        "Tag", secondary="collection_tag", lazy="dynamic", back_populates="collections"
    )

    @classmethod
    def create(
        cls,
        *,
        creator,
        identifier,
        title,
        description="",
        plain_description="",
        state="active",
        visibility="private",
    ):
        """Create a new collection and add it to the database session.

        :param creator: The user that created the collection.
        :param identifier: The unique identifier of the collection.
        :param title: The title of the collection.
        :param description: (optional) The description of the collection.
        :param plain_description: (optional) The plain description of the collection.
        :param state: (optional) The state of the collection.
        :param visibility: (optional) The default visibility of the collection.
        :return: The new :class:`.Collection` object.
        """
        collection = cls(
            creator=creator,
            identifier=identifier,
            title=title,
            description=description,
            plain_description=plain_description,
            state=state,
            visibility=visibility,
        )

        db.session.add(collection)
        return collection


# Auxiliary table for collection tags.
db.Table(
    "collection_tag",
    db.Column(
        "collection_id", db.Integer, db.ForeignKey("collection.id"), primary_key=True
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)
