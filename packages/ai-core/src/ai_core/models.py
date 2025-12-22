from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class GraphProfile:
    id: UUID
    name: str
    version_major: int
    version_minor: int
    graph_name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


@dataclass
class ModelProfile:
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
