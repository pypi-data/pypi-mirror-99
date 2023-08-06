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
from .core import AuthProviderBase
from kadi.lib.ldap import bind
from kadi.lib.ldap import make_connection
from kadi.lib.ldap import make_server
from kadi.lib.ldap import modify_password
from kadi.lib.ldap import search
from kadi.lib.ldap import unbind
from kadi.lib.utils import named_tuple
from kadi.modules.accounts.models import LDAPIdentity


class LDAPProvider(AuthProviderBase):
    """LDAP authentication provider."""

    class Meta:
        """Container to store meta class attributes."""

        provider_type = {"type": "ldap", "name": "LDAP"}
        """The type and full name of the provider."""

        defaults = {
            "title": "Login with LDAP",
            "default_system_role": "member",
            "host": "",
            "port": 389,
            "encryption": None,
            "validate_cert": True,
            "users_dn": "",
            "bind_user": None,
            "bind_pw": None,
            "username_attr": "uid",
            "email_attr": "mail",
            "displayname_attr": "displayName",
            "firstname_attr": "givenName",
            "lastname_attr": "sn",
            "allow_password_change": False,
            "supports_std_exop": True,
            "send_old_password": False,
        }
        """The default configuration values of the provider."""

    @classmethod
    def _make_connection(cls, user_dn=None, username=None, password=None):
        config = cls.get_config()
        encryption = config["encryption"]

        use_ssl = encryption.lower() == "ldaps" if encryption is not None else False
        server = make_server(
            config["host"],
            port=config["port"],
            use_ssl=use_ssl,
            validate_cert="REQUIRED" if config["validate_cert"] else "NONE",
        )

        user = None
        if user_dn is not None:
            user = user_dn
        elif username is not None:
            user = f"{config['username_attr']}={username},{config['users_dn']}"

        use_starttls = (
            encryption.lower() == "starttls" if encryption is not None else False
        )

        return make_connection(
            server, user=user, password=password, use_starttls=use_starttls
        )

    @classmethod
    def allow_password_change(cls):
        if not cls.is_registered():
            return False

        return cls.get_config()["allow_password_change"]

    @classmethod
    def register(cls, *, username, email, displayname, system_role=None, **kwargs):
        """Register a new LDAP user.

        If an identity with the given ``username`` already exists, that identity will be
        updated with the given ``email``.

        :param username: The user's unique name.
        :param email: The user's email address.
        :param displayname: The users's display name.
        :param system_role: (optional) The user's system role. Defaults to ``"member"``.
        :return: A new :class:`.LDAPIdentity` object linked with a new user or an
            existing, updated :class:`.LDAPIdentity`. Returns ``None`` if this provider
            is not registered in the application.
        """
        # pylint: disable=arguments-differ
        if not cls.is_registered():
            return None

        config = cls.get_config()
        identity = LDAPIdentity.query.filter_by(username=username).first()

        if identity:
            identity.email = email
            return identity

        system_role = (
            system_role if system_role is not None else config["default_system_role"]
        )
        return cls._create_identity(
            system_role=system_role,
            identity_model=LDAPIdentity,
            username=username,
            email=email,
            displayname=displayname,
        )

    @classmethod
    def authenticate(cls, *, username, password, **kwargs):
        """Authenticate an LDAP user.

        :param username: The user's unique name to use for binding to the LDAP server
            and for searching their entry in the database.
        :param password: The user's password to use for binding to the LDAP server.
        :return: An instance of :class:`.UserInfo` or ``None`` if this provider is not
            registered in the application. In case the authentication is successful, the
            contained data is an object containing the username, email and display name
            of the user as attributes ``username``, ``email`` and ``displayname``
            respectively.
        """
        # pylint: disable=arguments-differ
        if not cls.is_registered():
            return None

        config = cls.get_config()

        # Try authenticating as the user.
        connection = cls._make_connection(username=username, password=password)
        if not bind(connection):
            return cls.UserInfo(False)

        # Then check if another user was configured to use for the LDAP operations.
        bind_user = config["bind_user"]
        if bind_user is not None:
            unbind(connection)
            connection = cls._make_connection(
                user_dn=bind_user, password=config["bind_pw"]
            )

            if not bind(connection):
                return cls.UserInfo(False)

        search_filter = f"({config['username_attr']}={username})"
        attribute_map = {
            "username": config["username_attr"],
            "email": config["email_attr"],
            "displayname": config["displayname_attr"],
            "firstname": config["firstname_attr"],
            "lastname": config["lastname_attr"],
        }

        results = search(connection, config["users_dn"], search_filter, attribute_map)
        unbind(connection)

        if results is None:
            return cls.UserInfo(False)

        username = results["username"]
        email = results["email"]
        if username is None or email is None:
            return cls.UserInfo(False)

        displayname = results["displayname"]
        if displayname is None:
            firstname = results["firstname"]
            lastname = results["lastname"]

            if firstname is not None and lastname is not None:
                displayname = f"{firstname} {lastname}"

        if displayname is None:
            displayname = username

        ldap_info = named_tuple(
            "LDAPInfo", username=username, email=email, displayname=displayname
        )
        return cls.UserInfo(True, ldap_info)

    @classmethod
    def change_password(cls, username, old_password, new_password):
        if not cls.is_registered():
            return False

        config = cls.get_config()

        # Try authenticating as the user.
        connection = cls._make_connection(username=username, password=old_password)
        if not bind(connection):
            return False

        # Then check if another user was configured to use for the LDAP operations.
        bind_user = config["bind_user"]
        if bind_user is not None:
            unbind(connection)
            connection = cls._make_connection(
                user_dn=bind_user, password=config["bind_pw"]
            )

            if not bind(connection):
                return False

        kwargs = {}
        if config["send_old_password"]:
            kwargs["old_password"] = old_password

        result = modify_password(
            connection,
            f"{config['username_attr']}={username},{config['users_dn']}",
            new_password,
            standard_exop=config["supports_std_exop"],
            **kwargs,
        )
        unbind(connection)

        return result
