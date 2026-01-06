from __future__ import annotations

import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pythonjsonlogger import jsonlogger

from ai_infra.settings import Settings


def configure_logging(settings: Settings) -> None:
    """
    Configure JSON-formatted logging.

    Sets up logging with JSON formatter, configures log level from settings,
    and instruments logging with OpenTelemetry to inject trace/span IDs.
    """
    level = settings.log_level.upper()

    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
    )
    handler.setFormatter(formatter)
    root.handlers = [handler]

    # Inject trace/span ids into logs (works nicely with OTel)
    LoggingInstrumentor().instrument(set_logging_format=False)


def configure_tracing(settings: Settings) -> None:
    """
    Configure OpenTelemetry tracing.

    Sets up tracer provider with OTLP exporter if tracing is enabled.
    """
    if not settings.enable_tracing:
        return

    if settings.otel_exporter_otlp_endpoint is None:
        raise ValueError(
            "otel_exporter_otlp_endpoint must be set when enable_tracing=True"
        )

    resource = Resource.create(
        {
            "service.name": settings.service_name,
        }
    )
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    exporter = OTLPSpanExporter(
        endpoint=str(settings.otel_exporter_otlp_endpoint), insecure=True
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
