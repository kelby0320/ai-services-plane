from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ai_core.models import GraphProfile, ModelProfile
from ai_core.orchestration.services.llm_service import LLMClient
from ai_core.repositories import GraphProfileRepository, ModelProfileRepository
from ai_infra.llms.client import OpenAiLLMClient, OpenAiLLMClientConfig
from ai_infra.settings import Settings
from ai_infra.sql_alchemy.repositories import (
    SqlAlchemyGraphProfileRepository,
    SqlAlchemyModelProfileRepository,
)


class AppContext:
    """Application context that manages Settings, repositories, and LLMClient."""

    def __init__(self):
        """Initialize AppContext with Settings, repositories, profile maps, and LLMClient."""
        # Load Settings
        self._settings = Settings()

        # Create SQLAlchemy engine and session factory
        engine = create_engine(str(self._settings.pg_dsn))
        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

        # Create a session for initialization
        session: Session = self._session_factory()

        # Create repositories
        self.graph_profile_repository: GraphProfileRepository = (
            SqlAlchemyGraphProfileRepository(session)
        )
        self.model_profile_repository: ModelProfileRepository = (
            SqlAlchemyModelProfileRepository(session)
        )

        # Build profile maps by querying all profiles
        graph_profiles_list = self.graph_profile_repository.get_all()
        self._graph_profiles: dict[UUID, GraphProfile] = {
            profile.id: profile for profile in graph_profiles_list
        }

        model_profiles_list = self.model_profile_repository.get_all()
        self._model_profiles: dict[UUID, ModelProfile] = {
            profile.id: profile for profile in model_profiles_list
        }

        # Create LLMClient
        client_config = OpenAiLLMClientConfig(
            base_url=self._settings.ai_base_url,
            api_key=self._settings.ai_api_key,
        )
        self._llm_client = OpenAiLLMClient(client_config)

        # Close the initialization session
        session.close()

    def get_settings(self) -> Settings:
        """Get the Settings instance."""
        return self._settings

    def get_model_profile(self, id: UUID) -> ModelProfile | None:
        """Get a ModelProfile by ID."""
        return self._model_profiles.get(id)

    def get_graph_profile(self, id: UUID) -> GraphProfile | None:
        """Get a GraphProfile by ID."""
        return self._graph_profiles.get(id)

    def get_llm_client(self) -> LLMClient:
        """Get the LLMClient instance."""
        return self._llm_client
