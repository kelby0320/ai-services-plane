from __future__ import annotations

import logging
import time
from typing import Any

import grpc
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

log = logging.getLogger("grpc")


class ChatTurnAttributesInterceptor(grpc.aio.ServerInterceptor):
    """
    Interceptor for ChatTurn gRPC method.

    Sets OTel span attributes, extracts correlation IDs from requests,
    and logs request start/finish events with latency and chunk counts.
    """

    async def intercept_service(
        self, continuation, handler_call_details: grpc.HandlerCallDetails
    ) -> Any:
        handler = await continuation(handler_call_details)
        if handler is None:
            return None

        # Match the ChatTurn unary-stream method only
        method = handler_call_details.method
        if method.endswith("/ChatTurn") and handler.unary_stream:
            inner = handler.unary_stream

            async def wrapped(request: Any, context: grpc.aio.ServicerContext) -> Any:
                start = time.perf_counter()

                # Extract correlation IDs from request
                request_id = getattr(request, "request_id", None)
                session_id = getattr(request, "session_id", None)
                user_id = getattr(request, "user_id", None)

                # OTel's aio_server_interceptor should have created the server span already.
                span = trace.get_current_span()
                if span and span.is_recording():
                    span.set_attribute("rpc.system", "grpc")
                    span.set_attribute("rpc.method", method)
                    span.set_attribute("request_id", request_id)
                    span.set_attribute("session_id", session_id)
                    span.set_attribute("user_id", user_id)

                log.info(
                    "request.start",
                    extra={
                        "request_id": request_id,
                        "session_id": session_id,
                        "user_id": user_id,
                    },
                )

                chunks = 0
                try:
                    async for event in inner(request, context):
                        chunks += 1
                        yield event
                except Exception as e:
                    # Record on current span (the gRPC server span)
                    span = trace.get_current_span()
                    if span and span.is_recording():
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR))
                    raise
                finally:
                    latency_ms = int((time.perf_counter() - start) * 1000)
                    span = trace.get_current_span()
                    if span and span.is_recording():
                        span.set_attribute("chunks", chunks)

                    log.info(
                        "request.finish",
                        extra={
                            "request_id": request_id,
                            "session_id": session_id,
                            "user_id": user_id,
                            "chunks": chunks,
                            "latency_ms": latency_ms,
                        },
                    )

            wrapped_handler = grpc.RpcMethodHandler()
            wrapped_handler.unary_unary = handler.unary_unary
            wrapped_handler.unary_stream = wrapped
            wrapped_handler.stream_unary = handler.stream_unary
            wrapped_handler.stream_stream = handler.stream_stream
            wrapped_handler.request_streaming = handler.request_streaming
            wrapped_handler.response_streaming = handler.response_streaming
            wrapped_handler.request_deserializer = handler.request_deserializer
            wrapped_handler.response_serializer = handler.response_serializer

            return wrapped_handler

        return handler
