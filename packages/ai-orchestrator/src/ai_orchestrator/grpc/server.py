import grpc.aio
from ai_orchestrator.context import AppContext
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2_grpc
from ai_orchestrator.grpc.servicers.chat_orchestrator import ChatOrchestratorService


async def serve(app_context: AppContext) -> grpc.aio.Server:
    settings = app_context.get_settings()
    port = settings.grpc_port

    server = grpc.aio.server()
    chat_orchestrator_pb2_grpc.add_ChatOrchestratorServicer_to_server(
        ChatOrchestratorService(app_context), server
    )
    server.add_insecure_port(f"[::]:{port}")
    return server
