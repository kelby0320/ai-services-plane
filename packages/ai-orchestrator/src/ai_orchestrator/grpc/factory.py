from ai_core.orchestration.orchestrator import ChatOrchestrator
from ai_core.orchestration.services import LLMService, Services
from ai_orchestrator.context import AppContext
from ai_orchestrator.grpc.plan import ChatTurnPlan


class ChatOrchestratorFactory:
    """Factory for creating ChatOrchestrator instances from ChatTurnPlan."""

    def __init__(self, app_context: AppContext) -> None:
        """
        Initialize ChatOrchestratorFactory.

        Args:
            app_context: Application context with Settings, repositories, and LLMClient.
        """
        self._app_context = app_context

    def create(self, plan: ChatTurnPlan) -> ChatOrchestrator:
        """
        Create a ChatOrchestrator instance from a ChatTurnPlan.

        Args:
            plan: The ChatTurnPlan containing all parsed and validated information.

        Returns:
            ChatOrchestrator: A configured ChatOrchestrator instance ready to execute.
        """
        # Get LLM client from AppContext
        client = self._app_context.get_llm_client()

        # Create LLM service
        main_llm_service = LLMService(client, plan.main_model_profile)

        # Create Services container
        services = Services(llm_main=main_llm_service)

        # Build graph
        graph = plan.graph_builder(services)

        # Create orchestrator
        orchestrator = ChatOrchestrator(graph)

        return orchestrator
