import anyio
import uvicorn
from ai_orchestrator.http.server import app as fastapi_app
from ai_orchestrator.grpc.server import serve as serve_grpc
from ai_orchestrator.context import AppContext
from ai_orchestrator.telemetry import configure_logging, configure_tracing


async def run_grpc(server, port: int):
    await server.start()
    print(f"gRPC server started on port {port}")
    await server.wait_for_termination()


async def start():
    app_context = AppContext()
    settings = app_context.get_settings()

    if settings.enable_tracing:
        configure_tracing(settings)

    configure_logging(settings)

    config = uvicorn.Config(
        fastapi_app, host="0.0.0.0", port=settings.http_port, log_level="info"
    )
    http_server = uvicorn.Server(config)

    grpc_server = await serve_grpc(app_context)

    print("Starting AI Orchestrator services...")
    async with anyio.create_task_group() as tg:
        tg.start_soon(http_server.serve)
        tg.start_soon(run_grpc, grpc_server, settings.grpc_port)
