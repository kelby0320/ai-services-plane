from langgraph.graph import END, StateGraph

from ai_core.orchestration.graphs.graph import OrchestratorGraph
from ai_core.orchestration.nodes.generate import llm_generate
from ai_core.orchestration.services import Services
from ai_core.orchestration.state import OrchestratorState
from ai_core.orchestration.graphs.helpers import node_func


def build_graph(services: Services) -> OrchestratorGraph:
    """
    Builds the default v1 graph.

    Args:
        services: Services container with LLM and other services.

    Returns:
        OrchestratorGraph: The compiled state graph wrapped in an OrchestratorGraph instance.
    """
    workflow = StateGraph(OrchestratorState)

    llm_generate_node = node_func(services, llm_generate)

    workflow.add_node("llm_generate", llm_generate_node)

    # Set entry point
    workflow.set_entry_point("llm_generate")

    # Add edges
    workflow.add_edge("llm_generate", END)

    return OrchestratorGraph(workflow.compile())
