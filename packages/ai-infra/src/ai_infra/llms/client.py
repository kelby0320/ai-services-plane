"""OpenAI-compatible LLM client."""

from __future__ import annotations

import json
from typing import Any, AsyncIterator

import httpx

from ai_infra.llms.models import (
    ChatRequest,
    ChatResponse,
    ChatStreamEvent,
    LLMClientConfig,
    StreamDone,
    StreamUsage,
    TokenDelta,
    messages_to_json,
    parse_usage,
)


class LLMClient:
    """Client for OpenAI-compatible LLM endpoints."""

    def __init__(self, config: LLMClientConfig) -> None:
        """
        Initialize the LLM client.

        Args:
            config: Client configuration.
        """
        self._config = config
        headers = config.default_headers.copy()
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"

        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            headers=headers,
            timeout=config.timeout_s,
            verify=config.verify_tls,
        )

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Send a non-streaming chat request.

        Args:
            request: Chat request parameters.

        Returns:
            Chat response with text and metadata.

        Raises:
            httpx.HTTPStatusError: If the request fails with a non-2xx status.
        """
        payload = self._build_payload(request)

        response = await self._client.post("/chat/completions", json=payload)
        response.raise_for_status()

        data = response.json()
        return self._parse_response(data)

    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[ChatStreamEvent]:
        """
        Send a streaming chat request.

        Args:
            request: Chat request parameters (stream will be forced to True).

        Yields:
            ChatStreamEvent objects (TokenDelta, StreamUsage, StreamDone).

        Raises:
            httpx.HTTPStatusError: If the request fails with a non-2xx status.
        """
        request.stream = True
        payload = self._build_payload(request)

        async with self._client.stream(
            "POST", "/chat/completions", json=payload
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                line = line.strip()
                if not line:
                    continue

                if line.startswith("data: "):
                    data_str = line[6:]  # Remove "data: " prefix
                    if data_str == "[DONE]":
                        yield StreamDone()
                        break

                    try:
                        chunk_data = json.loads(data_str)
                    except json.JSONDecodeError:
                        continue

                    # Yield token delta if present
                    if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                        choice = chunk_data["choices"][0]
                        delta = choice.get("delta", {})
                        if "content" in delta and delta["content"]:
                            yield TokenDelta(text=delta["content"])

                    # Yield usage if present
                    if "usage" in chunk_data:
                        usage = parse_usage(chunk_data)
                        if usage:
                            yield StreamUsage(usage=usage)

                    # Check for finish reason
                    if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                        choice = chunk_data["choices"][0]
                        finish_reason = choice.get("finish_reason")
                        if finish_reason:
                            yield StreamDone(finish_reason=finish_reason)
                            break

    async def aclose(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    def _build_payload(self, request: ChatRequest) -> dict[str, Any]:
        """Build JSON payload from ChatRequest."""
        payload: dict[str, Any] = {
            "model": request.model,
            "messages": messages_to_json(request.messages),
            "stream": request.stream,
        }

        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.top_p is not None:
            payload["top_p"] = request.top_p
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens
        if request.stop is not None:
            payload["stop"] = request.stop

        # Merge extra fields
        payload.update(request.extra)

        return payload

    def _parse_response(self, data: dict[str, Any]) -> ChatResponse:
        """Parse OpenAI-compatible response."""
        text = ""
        finish_reason = None

        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            # Prefer message.content, fallback to text
            if "message" in choice:
                message = choice["message"]
                text = message.get("content", "")
            elif "text" in choice:
                text = choice.get("text", "")

            finish_reason = choice.get("finish_reason")

        usage = parse_usage(data)

        return ChatResponse(
            text=text,
            finish_reason=finish_reason,
            usage=usage,
            raw=data,
        )
