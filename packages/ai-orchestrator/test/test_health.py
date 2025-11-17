import pytest
from httpx import ASGITransport, AsyncClient
from ai_orchestrator import app


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        yield client


@pytest.mark.anyio
async def test_healthz(client):
    response = await client.get("/api/v1/healthz")
    assert response.status_code == 200
