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
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask_babel import gettext as _
from flask_login import login_required

from .blueprint import bp
from .core import create_template
from .core import delete_template as _delete_template
from .core import update_template
from .forms import AddPermissionsForm
from .forms import EditExtrasTemplateForm
from .forms import EditRecordTemplateForm
from .forms import NewExtrasTemplateForm
from .forms import NewRecordTemplateForm
from .models import Template
from kadi.ext.db import db
from kadi.lib.forms import field_to_dict
from kadi.lib.resources.views import add_roles
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import permission_required
from kadi.modules.records.models import Record


@bp.route("")
@login_required
def templates():
    """Template overview page.

    Allows users to filter for templates or create new ones.
    """
    return render_template("templates/templates.html", title=_("Templates"))


@bp.route("/new/<type>", methods=["GET", "POST"])
@qparam("template", None, type=int)
@qparam("record", None, type=int)
@permission_required("create", "template", None)
def new_template(type, qparams):
    """Page to create a new template."""
    template = None
    record = None

    if request.method == "GET":
        # Copy a template's metadata.
        if qparams["template"] is not None:
            template = Template.query.get(qparams["template"])

        # Copy a record's extra metadata to an "extras" template (without values).
        if qparams["record"] is not None:
            record = Record.query.get(qparams["record"])

    if type == "record":
        return _new_record_template(template)
    if type == "extras":
        return _new_extras_template(template, record)

    abort(404)


def _new_record_template(template):
    form = NewRecordTemplateForm(template=template)

    if request.method == "POST":
        if form.validate():
            data = {
                "title": form.record_title.data,
                "identifier": form.record_identifier.data,
                "type": form.record_type.data,
                "description": form.record_description.data,
                "license": form.record_license.data,
                "tags": form.record_tags.data,
                "extras": form.record_extras.data,
            }

            template = create_template(
                identifier=form.identifier.data,
                title=form.title.data,
                data=data,
                type="record",
            )

            if template:
                db.session.commit()

                flash(_("Template created successfully."), "success")
                return redirect(url_for("templates.view_template", id=template.id))

        flash(_("Error creating template."), "danger")

    return render_template(
        "templates/new_template.html",
        title=_("New record template"),
        type="record",
        form=form,
        js_resources={
            "title_field": field_to_dict(form.title),
            "extras_field": field_to_dict(form.record_extras),
        },
    )


def _new_extras_template(template, record):
    form = NewExtrasTemplateForm(template=template, record=record)

    if request.method == "POST":
        if form.validate():
            template = create_template(
                identifier=form.identifier.data,
                title=form.title.data,
                data=form.extras.data,
                type="extras",
            )

            if template:
                db.session.commit()

                flash(_("Template created successfully."), "success")
                return redirect(url_for("templates.view_template", id=template.id))

        flash(_("Error creating template."), "danger")

    return render_template(
        "templates/new_template.html",
        title=_("New extras template"),
        type="extras",
        form=form,
        js_resources={
            "title_field": field_to_dict(form.title),
            "extras_field": field_to_dict(form.extras),
        },
    )


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@permission_required("update", "template", "id")
def edit_template(id):
    """Page to edit an existing template."""
    template = Template.query.get_or_404(id)

    if template.type == "record":
        return _edit_record_template(template)
    if template.type == "extras":
        return _edit_extras_template(template)

    abort(404)


def _edit_record_template(template):
    form = EditRecordTemplateForm(template)

    if request.method == "POST":
        if form.validate():
            data = {
                "title": form.record_title.data,
                "identifier": form.record_identifier.data,
                "type": form.record_type.data,
                "description": form.record_description.data,
                "license": form.record_license.data,
                "tags": form.record_tags.data,
                "extras": form.record_extras.data,
            }

            if update_template(
                template,
                identifier=form.identifier.data,
                title=form.title.data,
                data=data,
            ):
                db.session.commit()

                flash(_("Changes saved successfully."), "success")
                return redirect(url_for("templates.view_template", id=template.id))

        flash(_("Error editing template."), "danger")

    return render_template(
        "templates/edit_template.html",
        title=_("Edit"),
        template=template,
        form=form,
        js_resources={
            "title_field": field_to_dict(form.title),
            "extras_field": field_to_dict(form.record_extras),
        },
    )


def _edit_extras_template(template):
    form = EditExtrasTemplateForm(template)

    if request.method == "POST":
        if form.validate():
            if update_template(
                template,
                identifier=form.identifier.data,
                title=form.title.data,
                data=form.extras.data,
            ):
                db.session.commit()

                flash(_("Changes saved successfully."), "success")
                return redirect(url_for("templates.view_template", id=template.id))

        flash(_("Error editing template."), "danger")

    return render_template(
        "templates/edit_template.html",
        title=_("Edit"),
        template=template,
        form=form,
        js_resources={
            "title_field": field_to_dict(form.title),
            "extras_field": field_to_dict(form.extras),
        },
    )


@bp.route("/<int:id>")
@permission_required("read", "template", "id")
def view_template(id):
    """Page to view a template."""
    template = Template.query.get_or_404(id)
    return render_template("templates/view_template.html", template=template)


@bp.route("/<int:id>/permissions", methods=["GET", "POST"])
@permission_required("permissions", "template", "id")
def manage_permissions(id):
    """Page to manage access permissions of a template."""
    template = Template.query.get_or_404(id)

    form = AddPermissionsForm()
    if form.validate_on_submit():
        add_roles(User, form.users.data, template, form.role.data)
        add_roles(Group, form.groups.data, template, form.role.data)
        db.session.commit()
        flash(_("Changes saved successfully."), "success")

    return render_template(
        "templates/manage_permissions.html",
        title=_("Permissions"),
        template=template,
        form=form,
    )


@bp.route("/<int:id>/delete", methods=["POST"])
@permission_required("delete", "template", "id")
def delete_template(id):
    """Endpoint to delete an existing template.

    Does basically the same as the corresponding API endpoint.
    """
    template = Template.query.get_or_404(id)

    _delete_template(template)
    db.session.commit()

    flash(_("Template deleted successfully."), "success")
    return redirect(url_for("templates.templates"))
