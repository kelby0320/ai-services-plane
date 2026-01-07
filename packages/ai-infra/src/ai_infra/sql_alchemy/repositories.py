import logging
from typing import Optional
from uuid import UUID

from opentelemetry import trace
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_core.models import GraphProfile, ModelProfile
from ai_core.repositories import GraphProfileRepository, ModelProfileRepository
from .orm import GraphProfileOrm, ModelProfileOrm

log = logging.getLogger("sql_alchemy.repositories")
tracer = trace.get_tracer("sql_alchemy.repositories")


class SqlAlchemyGraphProfileRepository(GraphProfileRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: UUID) -> Optional[GraphProfile]:
        with tracer.start_as_current_span("graph_profile_repository.get_by_id"):
            log.debug(
                "graph_profile_repository.get_by_id", extra={"graph_profile_id": id}
            )
            orm = self._session.get(GraphProfileOrm, id)
            if orm:
                return orm.to_domain()
            return None

    def get_all(self) -> list[GraphProfile]:
        """Retrieve all graph profiles."""
        with tracer.start_as_current_span("graph_profile_repository.get_all"):
            stmt = select(GraphProfileOrm)
            orms = self._session.scalars(stmt).all()
            count = len(orms)
            log.debug("graph_profile_repository.get_all", extra={"count": count})
            return [orm.to_domain() for orm in orms]


class SqlAlchemyModelProfileRepository(ModelProfileRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: UUID) -> Optional[ModelProfile]:
        with tracer.start_as_current_span("model_profile_repository.get_by_id"):
            log.debug(
                "model_profile_repository.get_by_id", extra={"graph_profile_id": id}
            )
            orm = self._session.get(ModelProfileOrm, id)
            if orm:
                return orm.to_domain()
            return None

    def get_all(self) -> list[ModelProfile]:
        """Retrieve all model profiles."""
        with tracer.start_as_current_span("model_profile_repository.get_all"):
            stmt = select(ModelProfileOrm)
            orms = self._session.scalars(stmt).all()
            count = len(orms)
            log.debug("model_profile_repository.get_all", extra={"count": count})
            return [orm.to_domain() for orm in orms]
