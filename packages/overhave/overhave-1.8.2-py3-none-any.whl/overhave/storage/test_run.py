import abc
from typing import Optional, cast

from overhave import db
from overhave.entities import TestRunModel
from overhave.utils.time import get_current_time


class ITestRunStorage(abc.ABC):
    """ Abstract class for test runs storage. """

    @abc.abstractmethod
    def create_test_run(self, scenario_id: int, executed_by: str) -> int:
        pass

    @abc.abstractmethod
    def set_run_status(self, run_id: int, status: db.TestRunStatus, traceback: Optional[str] = None) -> None:
        pass

    @abc.abstractmethod
    def set_report(self, run_id: int, status: db.TestReportStatus, report: Optional[str] = None) -> None:
        pass

    @abc.abstractmethod
    def get_test_run(self, run_id: int) -> Optional[TestRunModel]:
        pass


class TestRunStorage(ITestRunStorage):
    """ Class for test runs storage. """

    def create_test_run(self, scenario_id: int, executed_by: str) -> int:
        with db.create_session() as session:
            scenario: db.Scenario = session.query(db.Scenario).filter(db.Scenario.id == scenario_id).one()
            feature: db.Feature = session.query(db.Feature).filter(db.Feature.id == scenario.feature_id).one()
            run = db.TestRun(  # type: ignore
                scenario_id=scenario_id,
                name=feature.name,
                start=get_current_time(),
                status=db.TestRunStatus.STARTED,
                report_status=db.TestReportStatus.EMPTY,
                executed_by=executed_by,
            )
            session.add(run)
            session.flush()
            return cast(int, run.id)

    def set_run_status(self, run_id: int, status: db.TestRunStatus, traceback: Optional[str] = None) -> None:
        with db.create_session() as session:
            run: db.TestRun = session.query(db.TestRun).filter(db.TestRun.id == run_id).one()
            run.status = status
            if status.finished:
                run.end = get_current_time()
            if isinstance(traceback, str):
                run.traceback = traceback

    def set_report(self, run_id: int, status: db.TestReportStatus, report: Optional[str] = None) -> None:
        with db.create_session() as session:
            run: db.TestRun = session.query(db.TestRun).filter(db.TestRun.id == run_id).one()
            run.report_status = status
            if isinstance(report, str):
                run.report = report

    def get_test_run(self, run_id: int) -> Optional[TestRunModel]:
        with db.create_session() as session:
            run: db.TestRun = session.query(db.TestRun).filter(db.TestRun.id == run_id).one_or_none()
            if run is not None:
                return cast(TestRunModel, TestRunModel.from_orm(run))
            return None
