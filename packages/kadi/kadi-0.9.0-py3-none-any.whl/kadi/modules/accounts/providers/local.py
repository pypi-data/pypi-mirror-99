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
from kadi.modules.accounts.models import LocalIdentity


class LocalProvider(AuthProviderBase):
    """Local authentication provider."""

    class Meta:
        """Container to store meta class attributes."""

        provider_type = {"type": "local", "name": "Local"}
        """The type and full name of the provider."""

        defaults = {
            "title": "Login with credentials",
            "default_system_role": "member",
            "allow_registration": False,
            "email_confirmation_required": False,
        }
        """The default configuration values of the provider."""

    @classmethod
    def registration_allowed(cls):
        """Check if this provider allows registration of new users.

        :return: ``True`` if registration is allowed, ``False`` if not or if this
            provider is not registered in the application.
        """
        if not cls.is_registered():
            return False

        return cls.get_config()["allow_registration"]

    @classmethod
    def email_confirmation_required(cls):
        """Check if this provider requires email confirmation.

        :return: ``True`` if email confirmation is required, ``False`` if not or if this
            provider is not registered in the application.
        """
        if not cls.is_registered():
            return False

        return cls.get_config()["email_confirmation_required"]

    @classmethod
    def allow_password_change(cls):
        if not cls.is_registered():
            return False

        return True

    @classmethod
    def register(
        cls, *, username, email, displayname, password, system_role=None, **kwargs
    ):
        """Register a new local user.

        :param username: The user's unique name.
        :param email: The user's email address.
        :param displayname: The users's display name.
        :param password: The users's password.
        :param system_role: (optional) The user's system role. Defaults to ``"member"``.
        :return: A new :class:`.LocalIdentity` object linked with a new user or ``None``
            if this provider is not registered in the application.
        """
        # pylint: disable=arguments-differ
        if not cls.is_registered():
            return None

        config = cls.get_config()
        system_role = (
            system_role if system_role is not None else config["default_system_role"]
        )

        return cls._create_identity(
            system_role=system_role,
            identity_model=LocalIdentity,
            username=username,
            email=email,
            displayname=displayname,
            password=password,
        )

    @classmethod
    def authenticate(cls, *, username, password, **kwargs):
        """Authenticate a local user.

        :param username: The user's unique name to search in the local database.
        :param password: The user's password to call
            :meth:`.LocalIdentity.check_password` with.
        :return: An instance of :class:`.UserInfo` or ``None`` if this provider is not
            registered in the application. In case the authentication is successful, the
            contained data is the user's existing :class:`.LocalIdentity`.
        """
        # pylint: disable=arguments-differ
        if not cls.is_registered():
            return None

        identity = LocalIdentity.query.filter_by(username=username).first()

        if identity and identity.check_password(password):
            return cls.UserInfo(True, identity)

        return cls.UserInfo(False)

    @classmethod
    def change_password(cls, username, old_password, new_password):
        if not cls.is_registered():
            return False

        identity = LocalIdentity.query.filter_by(username=username).first()

        if identity.check_password(old_password):
            identity.set_password(new_password)
            return True

        return False
