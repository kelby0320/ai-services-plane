"""LLM service for model-bound orchestration."""

from dataclasses import dataclass
from collections.abc import AsyncIterator
from typing import Any, Literal, Protocol

from ai_core.models import ModelProfile

# Type definitions
Role = Literal["system", "developer", "user", "assistant", "tool"]


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


class LLMClient(Protocol):
    """Protocol for LLM client implementations."""

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Send a non-streaming chat request.

        Args:
            request: Chat request parameters.

        Returns:
            Chat response with text and metadata.
        """
        ...

    def stream_chat(self, request: ChatRequest) -> AsyncIterator[ChatStreamEvent]:
        """
        Send a streaming chat request.

        Args:
            request: Chat request parameters (stream will be forced to True).

        Yields:
            ChatStreamEvent objects (TokenDelta, StreamUsage, StreamDone).
        """
        ...

    async def aclose(self) -> None:
        """Close the client."""
        ...


class LLMService:
    """Service for LLM operations with model-specific defaults."""

    def __init__(self, client: LLMClient, profile: ModelProfile) -> None:
        """
        Initialize the LLM service.

        Args:
            client: LLM client instance.
            profile: Model profile with defaults.
        """
        self._client: LLMClient = client
        self._profile: ModelProfile = profile

    def stream(
        self, messages: list[ChatMessage], **overrides: Any
    ) -> AsyncIterator[ChatStreamEvent]:
        """
        Stream chat completion with merged parameters.

        Args:
            messages: List of chat messages.
            **overrides: Parameter overrides (temperature, top_p, max_tokens, etc.).

        Returns:
            AsyncIterator of ChatStreamEvent objects.
        """
        request = ChatRequest(model=self._profile.model, messages=messages, stream=True)
        return self._client.stream_chat(request)

    async def chat(self, messages: list[ChatMessage], **overrides: Any) -> ChatResponse:
        """
        Send chat completion with merged parameters.

        Args:
            messages: List of chat messages.
            **overrides: Parameter overrides (temperature, top_p, max_tokens, etc.).

        Returns:
            Chat response.
        """
        request = ChatRequest(
            model=self._profile.model, messages=messages, stream=False
        )
        return await self._client.chat(request)
