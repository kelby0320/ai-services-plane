from collections.abc import AsyncIterator
from typing import Any

from langgraph.graph.state import CompiledStateGraph


class OrchestratorGraph:
    """
    Wrapper around LangGraph's CompiledStateGraph to abstract LangGraph dependencies.

    This allows ai-core to depend on LangGraph while exposing a clean interface
    that other packages can use without directly depending on LangGraph.
    """

    def __init__(self, compiled_graph: CompiledStateGraph):
        """
        Initialize the OrchestratorGraph wrapper.

        Args:
            compiled_graph: The compiled LangGraph instance to wrap.
        """
        self._graph = compiled_graph

    async def astream(
        self,
        initial_state: dict,
        stream_mode: Any = "custom",
    ) -> AsyncIterator[dict]:
        """
        Stream state updates from the graph execution.

        Args:
            initial_state: Dictionary containing the initial state for graph execution.
            stream_mode: The stream mode to use (default: "custom").

        Yields:
            dict: State updates from the graph execution.
        """
        async for state_update in self._graph.astream(
            initial_state, stream_mode=stream_mode
        ):
            yield state_update
