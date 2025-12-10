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

    def execute(self, message: str) -> str:
        """
        Executes the graph with the given message.

        Args:
            message (str): The input message to execute the graph with.

        Returns:
            str: The response from the graph execution.
        """
        initial_state = {"messages": [message]}
        result = self._graph.invoke(initial_state)

        # extracted from state
        messages = result.get("messages", [])
        if messages:
            return messages[-1]
        return ""
