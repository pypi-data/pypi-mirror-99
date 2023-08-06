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
from flask import render_template
from flask_babel import gettext as _
from flask_login import current_user

from .blueprint import bp
from kadi.modules.collections.models import Collection
from kadi.modules.collections.schemas import CollectionSchema
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.records.models import Record
from kadi.modules.records.schemas import RecordSchema
from kadi.version import __version__


@bp.route("/")
def index():
    """The index/home page.

    Will change depending on whether the current user is authenticated or not.
    """
    if not current_user.is_authenticated:
        return render_template("main/index.html", version=__version__)

    records = (
        get_permitted_objects(current_user, "read", "record")
        .active()
        .order_by(Record.last_modified.desc())
        .limit(6)
    )

    collections = (
        get_permitted_objects(current_user, "read", "collection")
        .active()
        .order_by(Collection.last_modified.desc())
        .limit(6)
    )

    return render_template(
        "main/home.html",
        title=_("Home"),
        js_resources={
            "records": RecordSchema(many=True, _internal=True).dump(records),
            "collections": CollectionSchema(many=True, _internal=True).dump(
                collections
            ),
        },
    )


@bp.route("/about")
def about():
    """The about page."""
    return render_template("main/about.html", title=_("About"), version=__version__)


@bp.route("/help")
def help():
    """The help page."""
    return render_template("main/help.html", title=_("Help"))
