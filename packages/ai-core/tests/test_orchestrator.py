import pytest
from uuid import uuid4

from ai_core.orchestration.graphs import graph_registry
from ai_core.orchestration.orchestrator import ChatOrchestrator
from ai_core.orchestration.services import Services
from ai_core.orchestration.streaming import TokenDelta


@pytest.mark.asyncio
async def test_chat_orchestrator_execution():
    """
    Verifies that the ChatOrchestrator can successfully execute the dummy graph
    and return the expected dummy response.
    """
    # Arrange
    build_graph = graph_registry.get("dummy_v1")
    assert build_graph is not None, "dummy_v1 should be registered"

    services = Services(llm_main=None)

    graph = build_graph(services)
    orchestrator = ChatOrchestrator(graph)
    input_message = "Test message"
    expected_response = "This is a dummy response from the LLM generation node."

    # Act
    initial_state = {
        "request_id": uuid4(),
        "session_id": uuid4(),
        "user_id": uuid4(),
        "model_bindings": {},
        "messages": [input_message],
    }

    sourced_events = []
    async for sourced_event in orchestrator.execute(initial_state):
        sourced_events.append(sourced_event)

    # Build response from TokenDelta events
    response = ""
    for sourced_event in sourced_events:
        if isinstance(sourced_event.event, TokenDelta):
            response += sourced_event.event.text

    # Remove trailing space from accumulated response
    response = response.rstrip()

    assert response == expected_response
