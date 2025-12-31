from dataclasses import dataclass
from typing import Callable
from uuid import UUID

from ai_core.models import GraphProfile, ModelProfile
from ai_core.orchestration.graphs import graph_registry
from ai_core.orchestration.graphs.graph import OrchestratorGraph
from ai_core.orchestration.services import Services
from ai_orchestrator.context import AppContext
from ai_orchestrator.exceptions import ChatTurnPlanError
from ai_orchestrator.grpc.generated.aisp.v1 import chat_orchestrator_pb2


@dataclass
class ChatTurnPlan:
    """
    Plan containing parsed and validated information from a ChatTurnRequest.

    This plan can be used later to construct a ChatOrchestrator instance.
    """

    request_id: UUID
    session_id: UUID
    user_id: UUID
    graph_profile_id: UUID
    graph_profile: GraphProfile
    graph_builder: Callable[[Services], OrchestratorGraph]
    model_bindings: dict[str, ModelProfile]
    main_model_profile: ModelProfile

    @classmethod
    def build(
        cls,
        request: chat_orchestrator_pb2.ChatTurnRequest,
        app_context: AppContext,
    ) -> "ChatTurnPlan":
        """
        Build a ChatTurnPlan from a ChatTurnRequest and AppContext.

        Args:
            request: The ChatTurnRequest to parse.
            app_context: Application context with Settings, repositories, and LLMClient.

        Returns:
            ChatTurnPlan: A plan containing all parsed and validated information.

        Raises:
            ChatTurnPlanError: If any validation fails or required data is missing.
        """
        # Extract IDs from request
        try:
            request_id = UUID(request.request_id)
        except ValueError as e:
            raise ChatTurnPlanError(
                code="INVALID_REQUEST_ID",
                message=f"Invalid request_id format: {request.request_id}",
            ) from e

        try:
            session_id = UUID(request.session_id)
        except ValueError as e:
            raise ChatTurnPlanError(
                code="INVALID_SESSION_ID",
                message=f"Invalid session_id format: {request.session_id}",
            ) from e

        try:
            user_id = UUID(request.user_id)
        except ValueError as e:
            raise ChatTurnPlanError(
                code="INVALID_USER_ID",
                message=f"Invalid user_id format: {request.user_id}",
            ) from e

        # Get graph profile
        try:
            graph_profile_id = UUID(request.assistant.graph_profile_id)
        except ValueError as e:
            raise ChatTurnPlanError(
                code="INVALID_GRAPH_PROFILE_ID",
                message=f"Invalid graph_profile_id format: {request.assistant.graph_profile_id}",
            ) from e

        graph_profile = app_context.get_graph_profile(graph_profile_id)
        if graph_profile is None:
            raise ChatTurnPlanError(
                code="GRAPH_PROFILE_NOT_FOUND",
                message=f"Graph profile {graph_profile_id} not found",
            )

        # Get graph builder function
        try:
            graph_builder = graph_registry[graph_profile.graph_name]
        except KeyError:
            raise ChatTurnPlanError(
                code="GRAPH_BUILDER_NOT_FOUND",
                message=f"Graph builder for '{graph_profile.graph_name}' not found",
            )

        # Build model bindings dict from request using AppContext
        model_bindings: dict[str, ModelProfile] = {}
        for binding in request.assistant.model_bindings:
            try:
                model_profile_id = UUID(binding.model_profile_id)
            except ValueError as e:
                raise ChatTurnPlanError(
                    code="INVALID_MODEL_PROFILE_ID",
                    message=f"Invalid model_profile_id format: {binding.model_profile_id}",
                ) from e

            model_profile = app_context.get_model_profile(model_profile_id)
            if model_profile is None:
                raise ChatTurnPlanError(
                    code="MODEL_PROFILE_NOT_FOUND",
                    message=f"Model profile {model_profile_id} not found",
                )
            model_bindings[binding.slot_name] = model_profile

        # Get model profile for main LLM service
        try:
            main_model_profile = model_bindings["main"]
        except KeyError:
            raise ChatTurnPlanError(
                code="NO_MODEL_PROFILE",
                message="No model profile available for LLM service",
            )

        return cls(
            request_id=request_id,
            session_id=session_id,
            user_id=user_id,
            graph_profile_id=graph_profile_id,
            graph_profile=graph_profile,
            graph_builder=graph_builder,
            model_bindings=model_bindings,
            main_model_profile=main_model_profile,
        )
