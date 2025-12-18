from datetime import datetime
from typing import Any
from uuid import UUID
from collections.abc import AsyncIterator

from ai_core.models import ModelProfile
from ai_core.orchestration.graphs.default_v1 import build_graph
from ai_core.orchestration.orchestrator import ChatOrchestrator
from ai_core.orchestration.services import LLMService, Services
from ai_infra.llms.client import OpenAiLLMClient, OpenAiLLMClientConfig
from ai_infra.settings import Settings
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2_grpc


class ChatOrchestratorService(chat_orchestrator_pb2_grpc.ChatOrchestratorServicer):
    async def ChatTurn(
        self,
        request: chat_orchestrator_pb2.ChatTurnRequest,
        context: Any,
    ) -> AsyncIterator[chat_orchestrator_pb2.ChatEvent]:
        # Extract IDs from request
        request_id = UUID(request.request_id)
        session_id = UUID(request.session_id)
        user_id = UUID(request.user_id)

        # Build model bindings dict from request
        # TODO: Fetch actual ModelProfile objects from repository using model_profile_id
        # For now, create placeholder ModelProfile objects
        model_bindings: dict[str, ModelProfile] = {}
        for binding in request.assistant.model_bindings:
            model_profile_id = UUID(binding.model_profile_id)
            # Create placeholder ModelProfile - should be fetched from repository
            model_profile = ModelProfile(
                id=model_profile_id,
                name="GPT-OSS-120B",
                description="",
                model="gpt-oss-120b",  # Default model, should come from repository
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True,
            )
            model_bindings[binding.slot_name] = model_profile

        # Get model profile for main LLM service (use "main" slot or first available)
        main_profile = model_bindings.get("main") or (
            list(model_bindings.values())[0] if model_bindings else None
        )
        if not main_profile:
            # Error case - no model profile available
            yield chat_orchestrator_pb2.ChatEvent(
                error=chat_orchestrator_pb2.ErrorEvent(
                    code="NO_MODEL_PROFILE",
                    message="No model profile available for LLM service",
                )
            )
            return

        settings = Settings()
        client_config = OpenAiLLMClientConfig(
            base_url=settings.ai_base_url,
            api_key=settings.ai_api_key,
        )
        client = OpenAiLLMClient(client_config)

        # Create LLM service
        llm_service = LLMService(client, main_profile)

        # Create Services container
        services = Services(llm_main=llm_service)

        # Build graph
        graph = build_graph(services)

        # Create orchestrator
        orchestrator = ChatOrchestrator(graph)

        # Execute graph
        user_message = request.input.message
        try:
            response = await orchestrator.execute(
                message=user_message,
                request_id=request_id,
                session_id=session_id,
                user_id=user_id,
                model_bindings=model_bindings,
            )

            # Stream response as gRPC events
            # For now, send as a single token chunk
            yield chat_orchestrator_pb2.ChatEvent(
                token=chat_orchestrator_pb2.TokenChunkEvent(
                    content=response,
                    is_first=True,
                    is_last=True,
                )
            )
            yield chat_orchestrator_pb2.ChatEvent(
                done=chat_orchestrator_pb2.DoneEvent()
            )
        except Exception as e:
            yield chat_orchestrator_pb2.ChatEvent(
                error=chat_orchestrator_pb2.ErrorEvent(
                    code="EXECUTION_ERROR",
                    message=str(e),
                )
            )
        finally:
            # Clean up client
            await client.aclose()
