import abc
import logging
import tempfile
from pathlib import Path

from overhave.db import TestRunStatus
from overhave.entities import OverhaveFileSettings, ReportManager, TestExecutorContext
from overhave.scenario import FileManager
from overhave.storage import IFeatureStorage, IScenarioStorage, ITestRunStorage
from overhave.test_execution.test_runner import PytestRunner
from overhave.transport import TestRunTask

logger = logging.getLogger(__name__)


class ITestExecutionManager(abc.ABC):
    """ Abstract class for test execution management. """

    @abc.abstractmethod
    def execute_test(self, task: TestRunTask) -> None:
        pass


class BaseTestExecutionManagerException(Exception):
    """ Base exception for :class:`TestExecutionManager`. """


class TestRunNotExistsError(BaseTestExecutionManagerException):
    """ Exception for situation with not existing TestRun. """


class ScenarioNotExistsError(BaseTestExecutionManagerException):
    """ Exception for situation with not existing Scenario. """


class TestExecutionManager(ITestExecutionManager):
    """ Class for test execution management. """

    def __init__(
        self,
        file_settings: OverhaveFileSettings,
        feature_storage: IFeatureStorage,
        scenario_storage: IScenarioStorage,
        test_run_storage: ITestRunStorage,
        file_manager: FileManager,
        test_runner: PytestRunner,
        report_manager: ReportManager,
    ):
        self._file_settings = file_settings
        self._feature_storage = feature_storage
        self._scenario_storage = scenario_storage
        self._test_run_storage = test_run_storage
        self._file_manager = file_manager
        self._test_runner = test_runner
        self._report_manager = report_manager

    def _run_test(self, context: TestExecutorContext, alluredir: Path) -> int:
        with self._file_manager.tmp_feature_file(context=context) as feature_file:
            with self._file_manager.tmp_fixture_file(context=context, feature_file=feature_file) as fixture_file:
                return self._test_runner.run(fixture_file=fixture_file.name, alluredir=alluredir.as_posix())

    def _compile_context(self, test_run_id: int) -> TestExecutorContext:
        test_run = self._test_run_storage.get_test_run(test_run_id)
        if test_run is None:
            raise TestRunNotExistsError(f"TestRun with id={test_run_id} does not exist!")
        scenario = self._scenario_storage.get_scenario(test_run.scenario_id)
        if scenario is None:
            raise ScenarioNotExistsError(f"Scenario with id={test_run.scenario_id} does not exist!")
        feature = self._feature_storage.get_feature(scenario.feature_id)
        return TestExecutorContext(feature=feature, scenario=scenario, test_run=test_run,)

    def execute_test(self, task: TestRunTask) -> None:
        test_run_id = task.data.test_run_id
        self._test_run_storage.set_run_status(run_id=test_run_id, status=TestRunStatus.RUNNING)
        ctx = self._compile_context(test_run_id)

        results_dir = Path(tempfile.mkdtemp())
        logger.debug("Allure results directory path: %s", results_dir.as_posix())
        try:
            test_return_code = self._run_test(context=ctx, alluredir=results_dir)
        except Exception as e:
            logger.exception("Error!")
            self._test_run_storage.set_run_status(
                run_id=test_run_id, status=TestRunStatus.INTERNAL_ERROR, traceback=str(e)
            )
            return

        logger.debug("Test returncode: %s", test_return_code)
        if test_return_code == 0:
            self._test_run_storage.set_run_status(run_id=test_run_id, status=TestRunStatus.SUCCESS)
        else:
            self._test_run_storage.set_run_status(
                run_id=test_run_id, status=TestRunStatus.FAILED, traceback="Test run failed!"
            )
        self._report_manager.create_allure_report(test_run_id=test_run_id, results_dir=results_dir)
