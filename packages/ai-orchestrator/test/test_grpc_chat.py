import pytest
import grpc.aio


from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2_grpc
from ai_orchestrator.grpc.servicers.chat_orchestrator import ChatOrchestratorService


@pytest.mark.asyncio
async def test_chat_orchestrator_grpc_turn():
    # Start server
    server = grpc.aio.server()
    chat_orchestrator_pb2_grpc.add_ChatOrchestratorServicer_to_server(
        ChatOrchestratorService(), server
    )
    # Bind to port 0 (random ephemeral port) to avoid conflicts
    port = server.add_insecure_port("[::]:0")
    await server.start()

    try:
        async with grpc.aio.insecure_channel(f"localhost:{port}") as channel:
            stub = chat_orchestrator_pb2_grpc.ChatOrchestratorStub(channel)

            request = chat_orchestrator_pb2.ChatTurnRequest(
                request_id="test-req",
                session_id="test-sess",
                user_id="test-user",
                input=chat_orchestrator_pb2.UserInput(message="Hello"),
            )

            responses = []
            async for response in stub.ChatTurn(request):
                responses.append(response)

            # Verify responses
            assert len(responses) == 2

            # First event: TokenChunk
            assert responses[0].token.content == "Hello from gRPC!"
            assert responses[0].token.is_first is True

            # Second event: Done
            assert responses[1].HasField("done")

    finally:
        await server.stop(grace=None)
