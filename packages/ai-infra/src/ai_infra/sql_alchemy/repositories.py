from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ai_core.models import GraphProfile, ModelProfile
from ai_core.repositories import GraphProfileRepository, ModelProfileRepository
from .orm import GraphProfileOrm, ModelProfileOrm


class SqlAlchemyGraphProfileRepository(GraphProfileRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: UUID) -> Optional[GraphProfile]:
        orm = self._session.get(GraphProfileOrm, id)
        if orm:
            return orm.to_domain()
        return None


class SqlAlchemyModelProfileRepository(ModelProfileRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: UUID) -> Optional[ModelProfile]:
        orm = self._session.get(ModelProfileOrm, id)
        if orm:
            return orm.to_domain()
        return None
