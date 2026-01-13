from unittest.mock import Mock, patch

import pytest
from ai_orchestrator.http.server import app as fastapi_app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(fastapi_app)


@pytest.fixture
def mock_app_context():
    with patch("ai_orchestrator.app.AppContext") as _:
        mock_context = Mock()

        # Setup repositories
        mock_graph_repo = Mock()
        mock_model_repo = Mock()

        mock_context.get_graph_profile_repository.return_value = mock_graph_repo
        mock_context.get_model_profile_repository.return_value = mock_model_repo

        # Inject into app state
        fastapi_app.state.context = mock_context

        yield mock_context
