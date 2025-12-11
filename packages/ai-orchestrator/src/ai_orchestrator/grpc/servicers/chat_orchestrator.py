from typing import AsyncIterator, Any

from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2_grpc


class ChatOrchestratorService(chat_orchestrator_pb2_grpc.ChatOrchestratorServicer):
    async def ChatTurn(
        self,
        request: chat_orchestrator_pb2.ChatTurnRequest,
        context: Any,
    ) -> AsyncIterator[chat_orchestrator_pb2.ChatEvent]:
        # Dummy implementation
        yield chat_orchestrator_pb2.ChatEvent(
            token=chat_orchestrator_pb2.TokenChunkEvent(
                content="Hello from gRPC!",
                is_first=True,
                is_last=False,
            )
        )
        yield chat_orchestrator_pb2.ChatEvent(done=chat_orchestrator_pb2.DoneEvent())
