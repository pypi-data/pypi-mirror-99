import logging
import typing
from http import HTTPStatus
from pathlib import Path

import flask
import werkzeug

from overhave import db
from overhave.admin.flask import get_flask_admin, get_flask_app
from overhave.admin.flask.login_manager import get_flask_login_manager
from overhave.factory import IOverhaveFactory, ProxyFactory

logger = logging.getLogger(__name__)

OverhaveAppType = typing.NewType("OverhaveAppType", flask.Flask)


def _prepare_factory(factory: ProxyFactory) -> None:
    """ Resolve necessary settings and prepare instance of :class:`ProxyFactory` for usage. """
    factory.context.logging_settings.setup_logging()
    factory.patch_pytest()
    factory.supply_injector_for_collection()
    factory.injector.collect_configs()


def _resolved_app(factory: IOverhaveFactory, template_dir: Path) -> flask.Flask:
    """ Resolve Flask application with :class:`IOverhaveFactory` and templates directory `template_dir`. """
    from overhave.admin.views import (
        DraftView,
        EmulationRunView,
        EmulationView,
        FeatureView,
        GroupView,
        OverhaveIndexView,
        TagsView,
        TestRunView,
        TestUserView,
        UserView,
    )

    index_view = OverhaveIndexView(name="Info", url="/", context=factory.context, auth_manager=factory.auth_manager)
    flask_admin = get_flask_admin(index_view=index_view)
    flask_admin.add_views(
        FeatureView(db.Feature, db.current_session, category="Scenarios", name="Features"),
        TestRunView(db.TestRun, db.current_session, category="Scenarios", name="Test runs"),
        DraftView(db.Draft, db.current_session, category="Scenarios", name="Versions"),
        TagsView(db.Tags, db.current_session, category="Scenarios", name="Tags"),
        EmulationView(db.Emulation, db.current_session, category="Emulation", name="Templates"),
        TestUserView(db.TestUser, db.current_session, category="Emulation", name="Test users"),
        EmulationRunView(db.EmulationRun, db.current_session, category="Emulation", name="Emulation runs"),
        UserView(db.UserRole, db.current_session, category="Access", name="Users"),
        GroupView(db.GroupRole, db.current_session, category="Access", name="Groups"),
    )
    flask_app = get_flask_app(template_folder=template_dir.as_posix())
    flask_admin.init_app(app=flask_app)
    login_manager = get_flask_login_manager()
    login_manager.init_app(flask_app)
    db.ensure_feature_types_exist(factory.feature_extractor.feature_types)  # type: ignore
    return flask_app


def overhave_app(factory: ProxyFactory) -> OverhaveAppType:  # noqa: C901
    """ Overhave application, based on Flask. """
    current_dir = Path(__file__).parent
    template_dir = current_dir / "templates"
    files_dir = current_dir / "files"

    _prepare_factory(factory)
    flask_app = _resolved_app(factory=factory, template_dir=template_dir)
    flask_app.config["FILES_DIR"] = files_dir

    @flask_app.teardown_request
    def remove_session(exception: typing.Optional[Exception]) -> None:
        db.current_session.remove()

    @flask_app.route("/reports/<path:request>", methods=["GET", "POST"])
    def get_report(request: str) -> flask.Response:
        if flask.request.method == "POST":
            test_run_id = flask.request.form.get("run_id")
            if test_run_id is None or not factory.report_manager.ensure_allure_report_exists(
                report=request, run_id=int(test_run_id)
            ):
                return flask.abort(status=HTTPStatus.NOT_FOUND)
        return typing.cast(
            flask.Response, flask.send_from_directory(factory.context.file_settings.tmp_reports_dir, request)
        )

    @flask_app.route("/emulations/<path:url>")
    def go_to_emulation(url: str) -> werkzeug.Response:
        return flask.redirect(factory.context.emulation_settings.get_emulation_url(url))

    @flask_app.route("/pull_request/<int:run_id>")
    def create_pr(run_id: int) -> werkzeug.Response:
        published_by = flask.request.args.get("published_by")
        if not isinstance(published_by, str):
            flask.flash("Parameter 'published_by' should be specified for version's creation!", category="error")
            return flask.redirect(
                flask.url_for("testrun.details_view", id=run_id), code=HTTPStatus.UNPROCESSABLE_ENTITY
            )
        return factory.processor.create_version(test_run_id=run_id, published_by=published_by)

    @flask_app.route("/files/<path:file>")
    def get_files(file: str) -> flask.Response:
        return typing.cast(flask.Response, flask.send_from_directory(files_dir, file))

    @flask_app.route("/favicon.ico")
    def favicon() -> flask.Response:
        return typing.cast(
            flask.Response, flask.send_from_directory(files_dir, "favicon.ico", mimetype="image/vnd.microsoft.icon")
        )

    return OverhaveAppType(flask_app)
