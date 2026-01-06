from __future__ import annotations

import logging
import time
from typing import Callable

from fastapi import Request
from fastapi import status
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

log = logging.getLogger("http")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware for request context tracking.

    Creates OTel spans for HTTP requests, extracts request IDs,
    and logs request start/finish events with latency.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()

        request_id = request.headers.get("x-request-id") or "missing"
        # Stash for log record extras downstream
        request.state.request_id = request_id

        tracer = trace.get_tracer("http")
        # If FastAPI OTel instrumentation is enabled, a server span may already exist.
        # We create a child span "http.request" to match naming conventions.
        with tracer.start_as_current_span("http.request") as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.route", request.url.path)
            span.set_attribute("request_id", request_id)

            log.info("request.start", extra={"request_id": request_id})

            response: Response | None = None
            try:
                response = await call_next(request)
                if response is not None:
                    span.set_attribute("http.status_code", response.status_code)
                return response
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("http.status_code", 500)
                span.set_status(Status(StatusCode.ERROR))
                raise
            finally:
                latency_ms = int((time.perf_counter() - start) * 1000)
                status_code = (
                    response.status_code
                    if response is not None
                    else status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                log.info(
                    "request.finish",
                    extra={
                        "request_id": request_id,
                        "status_code": status_code,
                        "latency_ms": latency_ms,
                    },
                )
