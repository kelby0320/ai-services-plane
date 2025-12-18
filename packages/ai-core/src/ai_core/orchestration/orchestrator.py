from uuid import UUID

from langgraph.graph.state import CompiledStateGraph

from ai_core.models import ModelProfile


class ChatOrchestrator:
    """
    The main orchestration component for executing chat graphs.
    """

    def __init__(self, graph: CompiledStateGraph):
        """
        Initialize the ChatOrchestrator.

        Args:
            graph (CompiledStateGraph): The compiled LangGraph instance to execute.
        """
        self._graph = graph

    async def execute(
        self,
        message: str,
        request_id: UUID,
        session_id: UUID,
        user_id: UUID,
        model_bindings: dict[str, ModelProfile],
    ) -> str:
        """
        Executes the graph with the given message and state.

        Args:
            message: The input message to execute the graph with.
            request_id: Unique identifier for the request.
            session_id: Unique identifier for the session.
            user_id: Unique identifier for the user.
            model_bindings: Dictionary mapping slot names to model profiles.

        Returns:
            str: The response from the graph execution.
        """
        initial_state = {
            "request_id": request_id,
            "session_id": session_id,
            "user_id": user_id,
            "model_bindings": model_bindings,
            "messages": [message],
        }
        result = await self._graph.ainvoke(initial_state)

        # extracted from state
        messages = result.get("messages", [])
        if messages:
            return messages[-1]
        return ""
