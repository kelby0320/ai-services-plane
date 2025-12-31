from typing import Callable
from ai_core.orchestration.services import Services
from ai_core.orchestration.state import OrchestratorState


def node_func(
    services: Services,
    func: Callable[[OrchestratorState, Services], dict],
) -> Callable[[OrchestratorState], dict]:
    """
    Converts a node function that takes a state and services into a function that takes only a state.

    Args:
        services: Services container with LLM and other services.
        func: The node function to wrap.

    Returns:
        A function that takes only a state and returns a dict.
    """

    async def inner_func(state: OrchestratorState) -> dict:
        return await func(state, services)

    return inner_func
