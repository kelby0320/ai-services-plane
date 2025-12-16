"""Types, configs, and events for LLM client operations."""

from dataclasses import dataclass, field
from typing import Any, Literal

Role = Literal["system", "developer", "user", "assistant", "tool"]


@dataclass
class LLMClientConfig:
    """Configuration for LLMClient."""

    base_url: str
    api_key: str | None = None
    timeout_s: float = 60.0
    default_headers: dict[str, str] = field(default_factory=dict)
    verify_tls: bool = True


@dataclass
class ChatMessage:
    """A single chat message."""

    role: Role
    content: str
    name: str | None = None


@dataclass
class ChatRequest:
    """Request for chat completion."""

    model: str
    messages: list[ChatMessage]
    stream: bool = False
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    stop: list[str] | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Usage:
    """Token usage information."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


@dataclass
class ChatResponse:
    """Response from chat completion."""

    text: str
    finish_reason: str | None = None
    usage: Usage | None = None
    raw: dict[str, Any] | None = None


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


def messages_to_json(messages: list[ChatMessage]) -> list[dict[str, Any]]:
    """Convert ChatMessage list to provider JSON format."""
    result = []
    for msg in messages:
        json_msg: dict[str, Any] = {
            "role": msg.role,
            "content": msg.content,
        }
        if msg.name is not None:
            json_msg["name"] = msg.name
        result.append(json_msg)
    return result


def parse_usage(data: dict[str, Any]) -> Usage | None:
    """Parse usage dictionary defensively."""
    if not isinstance(data, dict):
        return None

    usage_data = data.get("usage", data)
    if not isinstance(usage_data, dict):
        return None

    return Usage(
        prompt_tokens=usage_data.get("prompt_tokens"),
        completion_tokens=usage_data.get("completion_tokens"),
        total_tokens=usage_data.get("total_tokens"),
    )
