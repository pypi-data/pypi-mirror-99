import abc

from overhave.entities import OverhaveFileSettings, PublisherContext
from overhave.publication.abstract_publisher import IVersionPublisher
from overhave.scenario import FileManager, generate_task_info
from overhave.storage import IDraftStorage, IFeatureStorage, IScenarioStorage, ITestRunStorage
from overhave.test_execution import OverhaveProjectSettings


class BaseVersionPublisherException(Exception):
    """ Base exception for :class:`BaseVersionPublisher`. """


class DraftNotExistsError(BaseVersionPublisherException):
    """ Exception for situation with not existing Draft. """


class TestRunNotExistsError(BaseVersionPublisherException):
    """ Exception for situation with not existing TestRun. """


class ScenarioNotExistsError(BaseVersionPublisherException):
    """ Exception for situation with not existing Scenario. """


class BaseVersionPublisher(IVersionPublisher, abc.ABC):
    """ Class for feature version's pull requests management relative to Atlassian Stash API. """

    def __init__(
        self,
        file_settings: OverhaveFileSettings,
        project_settings: OverhaveProjectSettings,
        feature_storage: IFeatureStorage,
        scenario_storage: IScenarioStorage,
        test_run_storage: ITestRunStorage,
        draft_storage: IDraftStorage,
        file_manager: FileManager,
    ) -> None:
        self._file_settings = file_settings
        self._project_settings = project_settings
        self._feature_storage = feature_storage
        self._scenario_storage = scenario_storage
        self._test_run_storage = test_run_storage
        self._draft_storage = draft_storage
        self._file_manager = file_manager

    def _compile_context(self, draft_id: int) -> PublisherContext:
        draft = self._draft_storage.get_draft(draft_id)
        if not draft:
            raise DraftNotExistsError(f"Draft with id={draft_id} does not exist!")
        test_run = self._test_run_storage.get_test_run(draft.test_run_id)
        if not test_run:
            raise TestRunNotExistsError(f"TestRun with id={draft.test_run_id} does not exist!")
        feature = self._feature_storage.get_feature(draft.feature_id)
        scenario = self._scenario_storage.get_scenario(test_run.scenario_id)
        if not scenario:
            raise ScenarioNotExistsError(f"Scenario with id={test_run.scenario_id} does not exist!")
        return PublisherContext(
            feature=feature,
            scenario=scenario,
            test_run=test_run,
            draft=draft,
            target_branch=f"bdd-feature-{feature.id}",
        )

    def _compile_publication_description(self, context: PublisherContext) -> str:
        return "\n".join(
            (
                f"Feature ID: {context.feature.id}. Type: '{context.feature.feature_type.name}'.",
                f"Created by: @{context.feature.author} at {context.feature.created_at.strftime('%d-%m-%Y %H:%M:%S')}.",
                f"Last edited by: @{context.feature.last_edited_by}.",
                f"PR from Test Run ID: {context.test_run.id}. Executed by: @{context.test_run.executed_by}",
                f"Published by: @{context.draft.published_by}.",
                generate_task_info(tasks=context.feature.task, header=self._project_settings.links_keyword),
            )
        )
