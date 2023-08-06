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
from flask import abort
from flask import current_app
from flask_sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from kadi.lib.exceptions import KadiDecryptionKeyError


naming_convention = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
}


class KadiBaseQuery(BaseQuery):
    """Custom SQLAlchemy query class."""

    def get_active_or_404(self, ident, attr="state", value="active"):
        """Convenience method to get an active item or abort with 404.

        In this context active means having some state attribute set to a specific
        value.

        :param ident: The primary key value of the item.
        :param attr: (optional) The name of the state attribute.
        :param value: (optional) The value the state attribute needs for the item to be
            considered active.
        :return: The item or an error reponse with status code 404 if the item was not
            found or is inactive.
        """
        item = self.get(ident)

        if item is not None:
            state = getattr(item, attr, None)

            if state is not None and state == value:
                return item

        abort(404)

    def active(self, attr="state", value="active"):
        """Shortcut to filter active rows for simple queries.

        In this context active means having some state attribute set to a specific
        value.

        :param attr: (optional) The name of the state attribute.
        :param value: (optional) The value the state attribute needs for the rows to be
            considered active.
        :return: The filtered query.
        """
        return self.filter_by(**{attr: value})


class KadiAesEngine(AesEngine):
    """Custom AES engine for decrypting database values."""

    def decrypt(self, value):
        """Try to decrypt the given value.

        :param value: The value to decrypt.
        :return: The decrypted value.
        :raises KadiDecryptionKeyError: If the key used for decrypting the value is
            invalid.
        """
        try:
            return super().decrypt(value)
        except ValueError as e:
            raise KadiDecryptionKeyError from e


def get_secret_key():
    """Get the secret key to use for encrypted fields.

    Note that this secret key is the same ``SECRET_KEY`` Flask uses as well, as
    specified in the application's configuration. If it ever changes, all fields
    encrypted with this key will become unreadable.

    :return: The secret key.
    """
    return current_app.config["SECRET_KEY"]


metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata, query_class=KadiBaseQuery)
