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
from sqlalchemy.dialects.postgresql import JSONB

from kadi.ext.db import db
from kadi.lib.db import composite_index
from kadi.lib.db import UTCDateTime
from kadi.lib.utils import SimpleReprMixin
from kadi.lib.utils import utcnow


class Notification(SimpleReprMixin, db.Model):
    """Model to represent user notifications."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "user_id", "name"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "notification"

    __table_args__ = (composite_index("user_id", "name"),)

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the notification, auto incremented."""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    """The ID of the user that should receive the notification."""

    name = db.Column(db.Text, nullable=False)
    """The name/type of the notification."""

    data = db.Column(JSONB, nullable=True)
    """The data of the notification, depending on its type."""

    created_at = db.Column(UTCDateTime, default=utcnow, nullable=False)
    """The date and time the notification was created at."""

    user = db.relationship("User", back_populates="notifications")

    @classmethod
    def create(cls, *, user, name, data=None):
        """Create a new notification and add it to the database session.

        :param user: The user that should receive the notification.
        :param name: The name/type of the notification.
        :param data: (optional) The data of the notification.
        :return: The new :class:`.Notification` object.
        """
        notification = cls(user=user, name=name, data=data)

        db.session.add(notification)
        return notification
