from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    http_port: int
    grpc_port: int
    ai_api_key: str
    ai_base_url: str
    pg_dsn: PostgresDsn
