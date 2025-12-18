from ai_core.orchestration.services import Services
from ai_core.orchestration.services.llm_service import ChatMessage
from ai_core.orchestration.state import GraphState


async def llm_generate(state: GraphState, services: Services) -> dict:
    """
    Generates a response using the LLM service.

    Args:
        state (GraphState): The current state of the graph.
        services (Services): Services container with LLM service.

    Returns:
        dict: The updated state with the generated message.
    """
    # Convert state messages to ChatMessage format
    # Assuming all messages are user messages for now
    chat_messages = [ChatMessage(role="user", content=msg) for msg in state["messages"]]

    # Call LLM service
    response = await services.llm_main.chat(chat_messages)

    # Update state with the response
    return {"messages": [response.text]}
