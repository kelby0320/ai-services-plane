from typing import Protocol, Optional
from uuid import UUID
from .models import GraphProfile


class GraphProfileRepository(Protocol):
    def get_by_id(self, id: UUID) -> Optional[GraphProfile]:
        """Retrieve a graph profile by its ID."""
        ...
