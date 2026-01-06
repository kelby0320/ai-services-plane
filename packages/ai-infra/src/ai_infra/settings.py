from pydantic import HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="AI_ORCHESTRATOR__", extra="allow"
    )

    http_port: int
    grpc_port: int
    ai_api_key: str
    ai_base_url: str
    pg_dsn: PostgresDsn
    log_level: str = "INFO"
    enable_tracing: bool = False
    service_name: str = "ai-orchestrator"
    otel_exporter_otlp_endpoint: HttpUrl | None = None
