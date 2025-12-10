from ai_core.orchestration.graphs import graph_registry
from ai_core.orchestration.orchestrator import ChatOrchestrator


def test_chat_orchestrator_execution():
    """
    Verifies that the ChatOrchestrator can successfully execute the default graph
    and return the expected dummy response.
    """
    # Arrange
    build_graph = graph_registry.get("default_graph_v1")
    assert build_graph is not None, "default_graph_v1 should be registered"

    graph = build_graph()
    orchestrator = ChatOrchestrator(graph)
    input_message = "Test message"
    expected_response = "This is a dummy response from the LLM generation node."

    # Act
    response = orchestrator.execute(input_message)

    # Assert
    assert response == expected_response
