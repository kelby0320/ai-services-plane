from typing import Any
from uuid import UUID
from collections.abc import AsyncIterator

from ai_core.models import ModelProfile
from ai_core.orchestration.graphs import graph_registry
from ai_core.orchestration.orchestrator import ChatOrchestrator
from ai_core.orchestration.services import LLMService, Services
from ai_orchestrator.context import AppContext
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2_grpc


class ChatOrchestratorService(chat_orchestrator_pb2_grpc.ChatOrchestratorServicer):
    def __init__(self, app_context: AppContext):
        """
        Initialize ChatOrchestratorService.

        Args:
            app_context: Application context with Settings, repositories, and LLMClient.
        """
        self._app_context = app_context

    async def ChatTurn(
        self,
        request: chat_orchestrator_pb2.ChatTurnRequest,
        context: Any,
    ) -> AsyncIterator[chat_orchestrator_pb2.ChatEvent]:
        # Extract IDs from request
        request_id = UUID(request.request_id)
        session_id = UUID(request.session_id)
        user_id = UUID(request.user_id)

        try:
            # Get graph profile
            graph_profile_id = UUID(request.assistant.graph_profile_id)
            graph_profile = self._app_context.get_graph_profile(graph_profile_id)
            if graph_profile is None:
                yield chat_orchestrator_pb2.ChatEvent(
                    error=chat_orchestrator_pb2.ErrorEvent(
                        code="GRAPH_PROFILE_NOT_FOUND",
                        message=f"Graph profile {graph_profile_id} not found",
                    )
                )
                return

            # Get graph builder function
            try:
                graph_builder = graph_registry[graph_profile.graph_name]
            except KeyError:
                yield chat_orchestrator_pb2.ChatEvent(
                    error=chat_orchestrator_pb2.ErrorEvent(
                        code="GRAPH_BUILDER_NOT_FOUND",
                        message=f"Graph builder for '{graph_profile.graph_name}' not found",
                    )
                )
                return

            # Build model bindings dict from request using AppContext
            model_bindings: dict[str, ModelProfile] = {}
            for binding in request.assistant.model_bindings:
                model_profile_id = UUID(binding.model_profile_id)
                model_profile = self._app_context.get_model_profile(model_profile_id)
                if model_profile is None:
                    yield chat_orchestrator_pb2.ChatEvent(
                        error=chat_orchestrator_pb2.ErrorEvent(
                            code="MODEL_PROFILE_NOT_FOUND",
                            message=f"Model profile {model_profile_id} not found",
                        )
                    )
                    return
                model_bindings[binding.slot_name] = model_profile

            # Get model profile for main LLM service
            try:
                main_profile = model_bindings["main"]
            except KeyError:
                yield chat_orchestrator_pb2.ChatEvent(
                    error=chat_orchestrator_pb2.ErrorEvent(
                        code="NO_MODEL_PROFILE",
                        message="No model profile available for LLM service",
                    )
                )
                return

            # Get LLM client from AppContext
            client = self._app_context.get_llm_client()

            # Create LLM service
            main_llm_service = LLMService(client, main_profile)

            # Create Services container
            services = Services(llm_main=main_llm_service)

            # Build graph
            graph = graph_builder(services)

            # Create orchestrator
            orchestrator = ChatOrchestrator(graph)

            # Prepare initial state
            user_message = request.input.message
            initial_state = {
                "request_id": request_id,
                "session_id": session_id,
                "user_id": user_id,
                "model_bindings": model_bindings,
                "messages": [user_message],
            }

            # Stream responses from orchestrator
            is_first = True
            last_message = ""
            async for state_update in orchestrator.execute(initial_state):
                # Extract llm_generate node output from state update
                try:
                    llm_generate = state_update["llm_generate"]
                except KeyError:
                    continue

                # Extract messages from llm_generate node output
                messages = llm_generate.get("messages", [])
                if messages:
                    # Get the latest message
                    current_message = messages[-1] if isinstance(messages, list) else ""
                    # Calculate the delta (new content)
                    if current_message and current_message != last_message:
                        delta = current_message[len(last_message) :]
                        if delta:
                            yield chat_orchestrator_pb2.ChatEvent(
                                token=chat_orchestrator_pb2.TokenChunkEvent(
                                    content=delta,
                                    is_first=is_first,
                                    is_last=False,
                                )
                            )
                            is_first = False
                            last_message = current_message

            # Send final token chunk if there's remaining content
            if last_message:
                yield chat_orchestrator_pb2.ChatEvent(
                    token=chat_orchestrator_pb2.TokenChunkEvent(
                        content="",
                        is_first=False,
                        is_last=True,
                    )
                )

            # End with DoneEvent
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
