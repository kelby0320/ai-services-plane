from ai_core.orchestration.state import GraphState


def llm_generate(state: GraphState) -> dict:
    """
    Simulates an LLM generation step.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        dict: The updated state with the generated message.
    """
    return {"messages": ["This is a dummy response from the LLM generation node."]}
