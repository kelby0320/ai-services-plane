from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from ai_core.orchestration.nodes.generate import llm_generate
from ai_core.orchestration.services import Services
from ai_core.orchestration.state import GraphState


def build_graph(services: Services) -> CompiledStateGraph:
    """
    Builds the default v1 graph.

    Args:
        services: Services container with LLM and other services.

    Returns:
        CompiledStateGraph: The compiled state graph.
    """
    workflow = StateGraph(GraphState)

    # # Add nodes - use a closure to capture services
    # async def node_func(state: GraphState) -> dict:
    #     return await llm_generate(state, services)

    workflow.add_node("llm_generate", lambda s: llm_generate(s, services))

    # Set entry point
    workflow.set_entry_point("llm_generate")

    # Add edges
    workflow.add_edge("llm_generate", END)

    return workflow.compile()
