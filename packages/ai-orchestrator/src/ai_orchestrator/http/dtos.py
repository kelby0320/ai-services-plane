from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GraphProfileResponse(BaseModel):
    id: UUID
    name: str
    version_major: int
    version_minor: int
    graph_name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ModelProfileResponse(BaseModel):
    id: UUID
    name: str
    description: str
    model: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
