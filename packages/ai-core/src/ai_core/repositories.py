from typing import Protocol, Optional
from uuid import UUID
from .models import GraphProfile, ModelProfile


class GraphProfileRepository(Protocol):
    def get_by_id(self, id: UUID) -> Optional[GraphProfile]:
        """Retrieve a graph profile by its ID."""
        ...


class ModelProfileRepository(Protocol):
    def get_by_id(self, id: UUID) -> Optional[ModelProfile]:
        """Retrieve a model profile by its ID."""
        ...
