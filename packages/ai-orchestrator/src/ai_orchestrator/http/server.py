from fastapi import FastAPI
from ai_orchestrator.http.routers import health

app = FastAPI(
    title="AI Orchestrator",
    version="0.1.0",
)

app.include_router(health.router, prefix="/api/v1")
