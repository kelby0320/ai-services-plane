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
