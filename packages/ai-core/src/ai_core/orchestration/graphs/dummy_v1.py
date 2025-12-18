from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from ai_core.orchestration.services import Services
from ai_core.orchestration.state import GraphState


async def dummy_llm_generate(state: GraphState) -> dict:
    """
    Dummy LLM generate node that returns a fixed response for testing.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        dict: The updated state with the dummy response message.
    """
    return {"messages": ["This is a dummy response from the LLM generation node."]}


def build_graph(services: Services) -> CompiledStateGraph:
    """
    Builds the dummy v1 graph for testing.

    Returns:
        CompiledStateGraph: The compiled state graph with dummy nodes.
    """
    workflow = StateGraph(GraphState)

    # Add dummy node
    workflow.add_node("dummy_llm_generate", dummy_llm_generate)

    # Set entry point
    workflow.set_entry_point("dummy_llm_generate")

    # Add edges
    workflow.add_edge("dummy_llm_generate", END)

    return workflow.compile()
