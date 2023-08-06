import json
import logging
import re
from functools import cached_property
from typing import Any, Dict, List, Optional, cast

import flask
import werkzeug
from flask_admin import expose
from flask_admin.model import InlineFormAdmin
from flask_login import current_user
from markupsafe import Markup
from wtforms import Field, TextAreaField, ValidationError
from wtforms.widgets import HiddenInput

from overhave import db
from overhave.admin.views.base import ModelViewConfigured
from overhave.factory import get_proxy_factory

logger = logging.getLogger(__name__)


class ScenarioTextWidget(HiddenInput):
    """ Widget to override scenario view. """

    def __call__(self, field: Field, **kwargs: Any) -> Any:
        widget_name = type(self).__name__
        logger.debug("%s field id: '%s'", widget_name, field.id)
        inputs = super().__call__(field, **kwargs)
        logger.debug("%s inputs: '%s'", widget_name, inputs)
        return inputs + Markup(f'<div class="editor" ref="{field.id}" id="{field.id}-editor"></div>')


class ScenarioTextAreaField(TextAreaField):
    """ Field to override scenario view. """

    widget = ScenarioTextWidget()


class ScenarioInlineModelForm(InlineFormAdmin):
    """ Form to override scenario view. """

    form_overrides = dict(text=ScenarioTextAreaField)
    form_excluded_columns = ("created_at", "test_runs")


class FeatureView(ModelViewConfigured):
    """ View for :class:`Feature` table. """

    can_view_details = False

    inline_models = (ScenarioInlineModelForm(db.Scenario),)

    create_template = "feature_create.html"
    edit_template = "feature_edit.html"

    column_list = (
        "id",
        "name",
        "feature_tags",
        "feature_type",
        "task",
        "author",
        "created_at",
        "last_edited_by",
        "released",
    )
    form_excluded_columns = (
        "created_at",
        "last_edited_by",
        "released",
        "versions",
        "feature_tags.value",
    )

    column_searchable_list = [
        "id",
        "name",
        "task",
        "author",
        "last_edited_by",
        "feature_tags.value",
    ]
    column_filters = ("name", "feature_type", "last_edited_by", "author", "created_at", "feature_tags.value")
    column_sortable_list = ("id", "name", "author", "last_edited_by")
    column_labels = {"feature_tags.value": "Tags"}

    _task_pattern = re.compile(r"\w+[-]\d+")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def _validate_tasks(cls, tasks: List[str]) -> None:
        for task in tasks:
            if cls._task_pattern.match(task):
                continue
            raise ValidationError(
                f"Incorrect format of task specification: '{task}'! "
                "Supported: <PROJECT>-<NUMBER>, for example 'PRJ-1234'."
            )

    def on_model_change(self, form, model, is_created) -> None:  # type: ignore
        self._validate_tasks(model.task)
        if is_created:
            model.author = current_user.login
        model.last_edited_by = current_user.login
        model.released = False

    def on_model_delete(self, model) -> None:  # type: ignore
        if not (current_user.login == model.author or current_user.role == db.Role.admin):
            raise ValidationError("Only feature author or administrator could delete feature!")

    @cached_property
    def get_bdd_steps(self) -> Dict[str, Dict[str, List[str]]]:
        factory = get_proxy_factory()
        return {
            feature_type: factory.injector.get_steps(feature_type)
            for feature_type in factory.feature_extractor.feature_types
        }

    @property
    def browse_url(self) -> Optional[str]:
        browse_url_value = get_proxy_factory().context.project_settings.browse_url
        if browse_url_value is not None:
            return cast(str, browse_url_value.human_repr())
        return None

    @staticmethod
    def _run_test(data: Dict[str, Any], rendered: werkzeug.Response) -> werkzeug.Response:
        prefix = "scenario-0"
        scenario_id = data.get(f"{prefix}-id")
        scenario_text = data.get(f"{prefix}-text")
        if not scenario_id or not scenario_text:
            logger.debug("Not found scenario for execution!")
            return rendered

        return cast(
            werkzeug.Response,
            get_proxy_factory().processor.execute_test(scenario_id=int(scenario_id), executed_by=current_user.login),
        )

    @expose("/edit/", methods=("GET", "POST"))
    def edit_view(self) -> werkzeug.Response:
        data = flask.request.form
        logger.debug("Request data:\n%s", json.dumps(data))

        rendered: werkzeug.Response = super().edit_view()
        logger.debug("EditView rendered")

        run_scenario_action = data.get("run")
        if not run_scenario_action:
            logger.debug("Show rendered EditView")
            return rendered

        logger.debug("Seen feature 'RUN' request")
        tasks = data.get("task").split(",")  # type: ignore
        self._validate_tasks(tasks=tasks)
        return self._run_test(data, rendered)
