"""LLM service for model-bound orchestration."""

from typing import Any, AsyncIterator

from ai_core.models import ModelProfile
from ai_infra.llms import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ChatStreamEvent,
    LLMClient,
)


class LLMService:
    """Service for LLM operations with model-specific defaults."""

    def __init__(self, client: LLMClient, profile: ModelProfile) -> None:
        """
        Initialize the LLM service.

        Args:
            client: LLM client instance.
            profile: Model profile with defaults.
        """
        self._client = client
        self._profile = profile

    async def stream(
        self, messages: list[ChatMessage], **overrides: Any
    ) -> AsyncIterator[ChatStreamEvent]:
        """
        Stream chat completion with merged parameters.

        Args:
            messages: List of chat messages.
            **overrides: Parameter overrides (temperature, top_p, max_tokens, etc.).

        Yields:
            ChatStreamEvent objects.
        """
        params = self._merge_params(overrides)
        request = ChatRequest(
            model=self._profile.model,
            messages=messages,
            stream=True,
            **params,
        )
        async for event in self._client.stream_chat(request):
            yield event

    async def chat(self, messages: list[ChatMessage], **overrides: Any) -> ChatResponse:
        """
        Send chat completion with merged parameters.

        Args:
            messages: List of chat messages.
            **overrides: Parameter overrides (temperature, top_p, max_tokens, etc.).

        Returns:
            Chat response.
        """
        params = self._merge_params(overrides)
        request = ChatRequest(
            model=self._profile.model,
            messages=messages,
            stream=False,
            **params,
        )
        return await self._client.chat(request)

    def _merge_params(self, overrides: dict[str, Any]) -> dict[str, Any]:
        """
        Merge parameters in order: profile defaults → profile.extra → overrides.

        Args:
            overrides: Call-level parameter overrides.

        Returns:
            Merged parameter dictionary.
        """
        params: dict[str, Any] = {}

        # Start with profile defaults
        if self._profile.temperature is not None:
            params["temperature"] = self._profile.temperature
        if self._profile.top_p is not None:
            params["top_p"] = self._profile.top_p
        if self._profile.max_tokens is not None:
            params["max_tokens"] = self._profile.max_tokens

        # Merge profile.extra
        params.update(self._profile.extra)

        # Apply overrides (last wins)
        params.update(overrides)

        return params
