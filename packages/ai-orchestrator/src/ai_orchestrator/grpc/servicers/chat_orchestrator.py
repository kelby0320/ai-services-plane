from typing import Any
from collections.abc import AsyncIterator

from ai_core.orchestration.streaming import StreamDone, TokenDelta
from ai_orchestrator.context import AppContext
from ai_orchestrator.exceptions import ChatTurnPlanError
from ai_orchestrator.grpc.factory import ChatOrchestratorFactory
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2_grpc
from ai_orchestrator.grpc.plan import ChatTurnPlan


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
        try:
            # Build plan from request
            try:
                plan = ChatTurnPlan.build(request, self._app_context)
            except ChatTurnPlanError as e:
                yield chat_orchestrator_pb2.ChatEvent(
                    error=chat_orchestrator_pb2.ErrorEvent(
                        code=e.code,
                        message=e.message,
                    )
                )
                return

            # Create orchestrator from plan
            factory = ChatOrchestratorFactory(self._app_context)
            orchestrator = factory.create(plan)

            # Prepare initial state
            initial_state = {
                "request_id": plan.request_id,
                "session_id": plan.session_id,
                "user_id": plan.user_id,
                "model_bindings": plan.model_bindings,
                "messages": [request.input.message],
            }

            # Stream events from orchestrator
            is_first = True
            async for sourced_event in orchestrator.execute(initial_state):
                event = sourced_event.event

                if isinstance(event, TokenDelta):
                    yield chat_orchestrator_pb2.ChatEvent(
                        token=chat_orchestrator_pb2.TokenChunkEvent(
                            content=event.text,
                            is_first=is_first,
                            is_last=False,
                        )
                    )
                    is_first = False
                elif isinstance(event, StreamDone):
                    # Send final token chunk to mark end of stream
                    if not is_first:
                        yield chat_orchestrator_pb2.ChatEvent(
                            token=chat_orchestrator_pb2.TokenChunkEvent(
                                content="",
                                is_first=False,
                                is_last=True,
                            )
                        )
                    # Send DoneEvent
                    yield chat_orchestrator_pb2.ChatEvent(
                        done=chat_orchestrator_pb2.DoneEvent()
                    )
                    break
                # StreamUsage events are currently not converted to protobuf

        except Exception as e:
            yield chat_orchestrator_pb2.ChatEvent(
                error=chat_orchestrator_pb2.ErrorEvent(
                    code="EXECUTION_ERROR",
                    message=str(e),
                )
            )
