import logging

from requests import HTTPError

from overhave.entities import OverhaveFileSettings, PublisherContext
from overhave.publication.git_publisher import BaseGitVersionPublisherError, GitVersionPublisher
from overhave.publication.stash.settings import OverhaveStashPublisherSettings
from overhave.scenario import FileManager
from overhave.storage import IDraftStorage, IFeatureStorage, IScenarioStorage, ITestRunStorage
from overhave.test_execution import OverhaveProjectSettings
from overhave.transport import (
    PublicationTask,
    StashBranch,
    StashErrorResponse,
    StashHttpClient,
    StashHttpClientConflictError,
    StashPrCreationResponse,
    StashPrRequest,
)

logger = logging.getLogger(__name__)


class BaseStashVersionPublisherException(BaseGitVersionPublisherError):
    """ Base exception for :class:`StashVersionPublisher`. """


class NullablePullRequestUrlError(BaseStashVersionPublisherException):
    """ Exception for nullable pull-request in selected Draft. """


class StashVersionPublisher(GitVersionPublisher):
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
        stash_publisher_settings: OverhaveStashPublisherSettings,
        client: StashHttpClient,
    ):
        super().__init__(
            file_settings=file_settings,
            project_settings=project_settings,
            feature_storage=feature_storage,
            scenario_storage=scenario_storage,
            test_run_storage=test_run_storage,
            draft_storage=draft_storage,
            file_manager=file_manager,
        )
        self._stash_publisher_settings = stash_publisher_settings
        self._client = client

    def _save_as_duplicate(self, context: PublisherContext) -> None:
        previous_draft = self._draft_storage.get_previous_feature_draft(context.feature.id)
        if previous_draft.pr_url is None:
            raise NullablePullRequestUrlError(
                "Previous draft with id=%s has not got pull-request URL!", previous_draft.id
            )
        if previous_draft.published_at is None:
            raise RuntimeError
        self._draft_storage.save_response(
            draft_id=context.draft.id,
            pr_url=previous_draft.pr_url,
            published_at=previous_draft.published_at,
            opened=True,
        )

    def publish_version(self, task: PublicationTask) -> None:
        draft_id = task.data.draft_id
        context = self._push_version(draft_id)
        if not isinstance(context, PublisherContext):
            return
        pull_request = StashPrRequest(
            title=context.feature.name,
            description=self._compile_publication_description(context),
            open=True,
            fromRef=StashBranch(id=context.target_branch, repository=self._stash_publisher_settings.repository),
            toRef=self._stash_publisher_settings.target_branch,
            reviewers=self._stash_publisher_settings.get_reviewers(feature_type=context.feature.feature_type.name),
        )
        logger.info("Prepared pull-request: %s", pull_request.json(by_alias=True))
        try:
            response = self._client.send_pull_request(pull_request)
            if isinstance(response, StashPrCreationResponse):
                self._draft_storage.save_response(
                    draft_id=draft_id,
                    pr_url=response.get_pr_url(),
                    published_at=response.created_date,
                    opened=response.open,
                )
                return
            if isinstance(response, StashErrorResponse) and response.duplicate:
                self._save_as_duplicate(context)
                return
            logger.error("Gotten error response from Stash: %s", response)
        except StashHttpClientConflictError:
            logger.exception("Gotten conflict. Try to return last pull-request for Draft with id=%s...", draft_id)
            self._save_as_duplicate(context)
        except HTTPError:
            logger.exception("Got HTTP error while trying to sent pull-request!")
