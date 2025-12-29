from collections.abc import AsyncIterator

from langgraph.graph.state import CompiledStateGraph


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
        initial_state: dict,
    ) -> AsyncIterator[dict]:
        """
        Executes the graph with the given initial state and streams state updates.

        Args:
            initial_state: Dictionary containing the initial state for graph execution.
                Expected keys: request_id, session_id, user_id, model_bindings, messages.

        Yields:
            dict: State updates from the graph execution.
        """
        async for state_update in self._graph.astream(
            initial_state, stream_mode="custom"
        ):
            yield state_update
