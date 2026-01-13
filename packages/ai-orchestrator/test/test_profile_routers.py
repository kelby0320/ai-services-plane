from uuid import uuid4

from ai_core.models import GraphProfile, ModelProfile


def test_get_graph_profile_success(client, mock_app_context):
    graph_id = uuid4()
    profile = GraphProfile(
        id=graph_id,
        name="Test Graph",
        version_major=1,
        version_minor=0,
        graph_name="test_graph",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        is_active=True,
    )

    mock_app_context.get_graph_profile_repository().get_by_id.return_value = profile

    response = client.get(f"/api/v1/graph_profile/{graph_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(graph_id)
    assert response.json()["name"] == "Test Graph"


def test_get_graph_profile_not_found(client, mock_app_context):
    graph_id = uuid4()
    mock_app_context.get_graph_profile_repository().get_by_id.return_value = None

    response = client.get(f"/api/v1/graph_profile/{graph_id}")

    assert response.status_code == 404


def test_get_model_profile_success(client, mock_app_context):
    model_id = uuid4()
    profile = ModelProfile(
        id=model_id,
        name="Test Model",
        description="A test model",
        model="gpt-4",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        is_active=True,
        temperature=0.5,
        top_p=0.9,
        max_tokens=1000,
    )

    mock_app_context.get_model_profile_repository().get_by_id.return_value = profile

    response = client.get(f"/api/v1/model_profile/{model_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(model_id)
    assert response.json()["name"] == "Test Model"
    assert response.json()["temperature"] == 0.5


def test_get_model_profile_not_found(client, mock_app_context):
    model_id = uuid4()
    mock_app_context.get_model_profile_repository().get_by_id.return_value = None

    response = client.get(f"/api/v1/model_profile/{model_id}")

    assert response.status_code == 404
