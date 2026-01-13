from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

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

    def get_model_profile_repository(self) -> ModelProfileRepository:
        """Get the ModelProfileRepository."""
        return self.model_profile_repository

    def get_graph_profile_repository(self) -> GraphProfileRepository:
        """Get the GraphProfileRepository."""
        return self.graph_profile_repository

    def get_llm_client(self) -> LLMClient:
        """Get the LLMClient instance."""
        return self._llm_client
