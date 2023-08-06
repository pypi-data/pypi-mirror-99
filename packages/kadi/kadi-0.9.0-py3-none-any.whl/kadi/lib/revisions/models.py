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
from kadi.lib.db import UTCDateTime
from kadi.lib.utils import SimpleReprMixin
from kadi.lib.utils import utcnow


class Revision(SimpleReprMixin, db.Model):
    """Model to represent general revision metadata.

    The actual revision models are created dynamically instead and linked to this model.
    See :func:`kadi.lib.revisions.core.setup_revisions`.
    """

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "timestamp", "user_id"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "revision"

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the revision, auto incremented."""

    timestamp = db.Column(UTCDateTime, default=utcnow, nullable=False)
    """The timestamp of the revision."""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    """The ID of the user that triggered the revision."""

    user = db.relationship("User", back_populates="revisions")

    @classmethod
    def create(cls, *, user):
        """Create a new revision and add it to the database session.

        :param user: The user that triggered the revision.
        :return: The new :class:`.Revision` object.
        """
        revision = cls(user=user)
        db.session.add(revision)
        return revision
