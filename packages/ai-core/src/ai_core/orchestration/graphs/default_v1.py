from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from ai_core.orchestration.nodes.generate import llm_generate
from ai_core.orchestration.state import GraphState


def build_graph() -> CompiledStateGraph:
    """
    Builds the default v1 graph.

    Returns:
        CompiledStateGraph: The compiled state graph.
    """
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("llm_generate", llm_generate)

    # Set entry point
    workflow.set_entry_point("llm_generate")

    # Add edges
    workflow.add_edge("llm_generate", END)

    return workflow.compile()
