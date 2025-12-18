import grpc.aio
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2_grpc
from ai_orchestrator.grpc.servicers.chat_orchestrator import ChatOrchestratorService


async def serve(port: int) -> grpc.aio.Server:
    server = grpc.aio.server()
    chat_orchestrator_pb2_grpc.add_ChatOrchestratorServicer_to_server(
        ChatOrchestratorService(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    return server
