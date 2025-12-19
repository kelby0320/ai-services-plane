from typing import Optional
from uuid import UUID

from sqlalchemy import select
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

    def get_all(self) -> list[GraphProfile]:
        """Retrieve all graph profiles."""
        stmt = select(GraphProfileOrm)
        orms = self._session.scalars(stmt).all()
        return [orm.to_domain() for orm in orms]


class SqlAlchemyModelProfileRepository(ModelProfileRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: UUID) -> Optional[ModelProfile]:
        orm = self._session.get(ModelProfileOrm, id)
        if orm:
            return orm.to_domain()
        return None

    def get_all(self) -> list[ModelProfile]:
        """Retrieve all model profiles."""
        stmt = select(ModelProfileOrm)
        orms = self._session.scalars(stmt).all()
        return [orm.to_domain() for orm in orms]
