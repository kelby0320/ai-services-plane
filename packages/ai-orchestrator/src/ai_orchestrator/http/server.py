from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from ai_orchestrator.http.middleware import RequestContextMiddleware
from ai_orchestrator.http.routers import graph_profile, health, model_profile

app = FastAPI(
    title="AI Orchestrator",
    version="0.1.0",
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(graph_profile.router, prefix="/api/v1")
app.include_router(model_profile.router, prefix="/api/v1")

FastAPIInstrumentor.instrument_app(app)

app.add_middleware(RequestContextMiddleware)
