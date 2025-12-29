from langgraph.config import get_stream_writer

from ai_core.orchestration.services import Services
from ai_core.orchestration.services.llm_service import ChatMessage, TokenDelta
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

    # Get stream writer (requires stream_mode="custom")
    writer = get_stream_writer()

    # Stream the response
    accumulated_text = ""
    stream = services.llm_main.stream(chat_messages)

    async for event in stream:
        if isinstance(event, TokenDelta):
            writer({"type": "token_delta", "content": event.text})
            accumulated_text += event.text

    # Return accumulated text in state
    return {"messages": [accumulated_text]}
