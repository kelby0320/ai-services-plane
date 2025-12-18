import anyio
import uvicorn
from ai_infra.settings import Settings
from ai_orchestrator.http.server import app as fastapi_app
from ai_orchestrator.grpc.server import serve as serve_grpc


async def run_grpc(server, port: int):
    await server.start()
    print(f"gRPC server started on port {port}")
    await server.wait_for_termination()


async def start():
    settings = Settings()

    config = uvicorn.Config(
        fastapi_app, host="0.0.0.0", port=settings.http_port, log_level="info"
    )
    http_server = uvicorn.Server(config)

    grpc_server = await serve_grpc(settings.grpc_port)

    print("Starting AI Orchestrator services...")
    async with anyio.create_task_group() as tg:
        tg.start_soon(http_server.serve)
        tg.start_soon(run_grpc, grpc_server, settings.grpc_port)
