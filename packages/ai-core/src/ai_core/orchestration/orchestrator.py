from collections.abc import AsyncIterator

from ai_core.orchestration.graphs.graph import OrchestratorGraph
from ai_core.orchestration.streaming import (
    ChatStreamEvent,
    SourcedEvent,
    StreamDone,
    StreamUsage,
    TokenDelta,
    Usage,
)


class ChatOrchestrator:
    """
    The main orchestration component for executing chat graphs.
    """

    def __init__(self, graph: OrchestratorGraph):
        """
        Initialize the ChatOrchestrator.

        Args:
            graph (OrchestratorGraph): The graph instance to execute.
        """
        self._graph = graph

    async def execute(
        self,
        initial_state: dict,
    ) -> AsyncIterator[SourcedEvent]:
        """
        Executes the graph with the given initial state and streams structured events.

        Args:
            initial_state: Dictionary containing the initial state for graph execution.
                Expected keys: request_id, session_id, user_id, model_bindings, messages.

        Yields:
            SourcedEvent: Structured events from the graph execution.
        """
        current_source: str | None = None

        async for stream_item in self._graph.astream(
            initial_state, stream_mode="custom"
        ):
            if not isinstance(stream_item, dict):
                continue

            # Check if this is a state update (has node name keys, not custom event)
            node_keys = [key for key in stream_item.keys() if not key.startswith("__")]
            if node_keys and "type" not in stream_item:
                # This is a state update - track the current source node
                current_source = node_keys[0]
                # State updates themselves are not yielded as events
                continue

            # Check if this is a custom event from stream writer
            if "type" in stream_item:
                event_type = stream_item.get("type")
                event: ChatStreamEvent | None = None

                if event_type == "token_delta":
                    content = stream_item.get("content", "")
                    event = TokenDelta(text=content)
                elif event_type == "stream_usage":
                    usage_dict = stream_item.get("usage")
                    if usage_dict:
                        usage = Usage(
                            prompt_tokens=usage_dict.get("prompt_tokens"),
                            completion_tokens=usage_dict.get("completion_tokens"),
                            total_tokens=usage_dict.get("total_tokens"),
                        )
                        event = StreamUsage(usage=usage)
                elif event_type == "stream_done":
                    finish_reason = stream_item.get("finish_reason")
                    event = StreamDone(finish_reason=finish_reason)

                if event is not None:
                    yield SourcedEvent(source=current_source, event=event)
