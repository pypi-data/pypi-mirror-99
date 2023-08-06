from typing import List, cast

from overhave import db
from overhave.entities import DraftModel
from overhave.transport import StashPrCreationResponse


class BaseDraftStorageException(Exception):
    """ Base exception for :class:`DraftStorage`. """


class UniqueDraftCreationError(BaseDraftStorageException):
    """ Exception for draft creation error with `as_unique`. """


class NullableDraftsError(BaseDraftStorageException):
    """ Exception for situation with not existing drafts. """


def save_draft(test_run_id: int, published_by: str) -> int:
    with db.create_session() as session:
        try:
            draft = session.query(db.Draft).as_unique(test_run_id=test_run_id, published_by=published_by)
        except RuntimeError as e:
            raise UniqueDraftCreationError("Could not get unique draft!") from e
        session.add(draft)
        session.flush()
        return cast(int, draft.id)


def add_pr_url(draft_id: int, response: StashPrCreationResponse) -> None:
    with db.create_session() as session:
        draft: db.Draft = session.query(db.Draft).filter(db.Draft.id == draft_id).one()
        draft.pr_url = response.get_pr_url()
        draft.created_at = response.created_date
        feature: db.Feature = session.query(db.Feature).filter(db.Feature.id == draft.feature.id).one()
        feature.released = response.open


def get_last_draft(feature_id: int) -> DraftModel:
    with db.create_session() as session:
        draft: db.Draft = session.query(db.Draft).filter(db.Draft.feature_id == feature_id).order_by(
            db.Draft.id.desc()
        ).first()
        return cast(DraftModel, DraftModel.from_orm(draft))


def get_previous_draft(feature_id: int) -> DraftModel:
    with db.create_session() as session:
        selection_num = 2
        drafts: List[db.Draft] = session.query(db.Draft).filter(db.Draft.feature_id == feature_id).order_by(
            db.Draft.id.asc()
        ).limit(selection_num).all()
        if not drafts or len(drafts) != selection_num:
            raise NullableDraftsError(f"Haven't got Drafts amount={selection_num} for feature_id={feature_id}!")
        return cast(DraftModel, DraftModel.from_orm(drafts[0]))
