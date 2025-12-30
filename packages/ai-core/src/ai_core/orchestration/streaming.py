"""Streaming event types for orchestration."""

from dataclasses import dataclass


@dataclass
class Usage:
    """Token usage information."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


@dataclass
class TokenDelta:
    """Streaming token delta event."""

    text: str


@dataclass
class StreamUsage:
    """Streaming usage information event."""

    usage: Usage


@dataclass
class StreamDone:
    """Stream completion event."""

    finish_reason: str | None = None


ChatStreamEvent = TokenDelta | StreamUsage | StreamDone


@dataclass(frozen=True)
class SourcedEvent:
    """An event with its source node identifier."""

    source: str | None
    event: ChatStreamEvent
