import anyio
import uvicorn
from ai_orchestrator.http.server import app as fastapi_app
from ai_orchestrator.grpc.server import serve as serve_grpc


async def run_grpc(server):
    await server.start()
    print("gRPC server started on port 50051")
    await server.wait_for_termination()


async def start():
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8000, log_level="info")
    http_server = uvicorn.Server(config)

    grpc_server = await serve_grpc()

    print("Starting AI Orchestrator services...")
    async with anyio.create_task_group() as tg:
        tg.start_soon(http_server.serve)
        tg.start_soon(run_grpc, grpc_server)
