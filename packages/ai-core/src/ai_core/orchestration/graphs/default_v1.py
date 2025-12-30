from langgraph.graph import END, StateGraph

from ai_core.orchestration.graphs.graph import OrchestratorGraph
from ai_core.orchestration.nodes.generate import llm_generate
from ai_core.orchestration.services import Services
from ai_core.orchestration.state import OrchestratorState


def build_graph(services: Services) -> OrchestratorGraph:
    """
    Builds the default v1 graph.

    Args:
        services: Services container with LLM and other services.

    Returns:
        OrchestratorGraph: The compiled state graph wrapped in an OrchestratorGraph instance.
    """
    workflow = StateGraph(OrchestratorState)

    # Add nodes - use a closure to capture services
    async def node_func(state: OrchestratorState) -> dict:
        return await llm_generate(state, services)

    workflow.add_node("llm_generate", node_func)

    # Set entry point
    workflow.set_entry_point("llm_generate")

    # Add edges
    workflow.add_edge("llm_generate", END)

    return OrchestratorGraph(workflow.compile())
