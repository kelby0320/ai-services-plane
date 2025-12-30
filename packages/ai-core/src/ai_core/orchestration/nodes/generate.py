from langgraph.config import get_stream_writer

from ai_core.orchestration.services import Services
from ai_core.orchestration.services.llm_service import ChatMessage
from ai_core.orchestration.state import OrchestratorState
from ai_core.orchestration.streaming import StreamDone, StreamUsage, TokenDelta


async def llm_generate(state: OrchestratorState, services: Services) -> dict:
    """
    Generates a response using the LLM service.

    Args:
        state (OrchestratorState): The current state of the graph.
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
        elif isinstance(event, StreamUsage):
            # Convert Usage dataclass to dict for serialization
            usage_dict = {
                "prompt_tokens": event.usage.prompt_tokens,
                "completion_tokens": event.usage.completion_tokens,
                "total_tokens": event.usage.total_tokens,
            }
            writer({"type": "stream_usage", "usage": usage_dict})
        elif isinstance(event, StreamDone):
            writer({"type": "stream_done", "finish_reason": event.finish_reason})

    # Return accumulated text in state
    return {"messages": [accumulated_text]}
