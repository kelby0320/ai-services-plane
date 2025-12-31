from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AI_ORCHESTRATOR__")

    http_port: int
    grpc_port: int
    ai_api_key: str
    ai_base_url: str
    pg_dsn: PostgresDsn
