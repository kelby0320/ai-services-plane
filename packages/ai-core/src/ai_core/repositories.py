from typing import Protocol, Optional
from uuid import UUID
from .models import GraphProfile, ModelProfile


class GraphProfileRepository(Protocol):
    def get_by_id(self, id: UUID) -> Optional[GraphProfile]:
        """Retrieve a graph profile by its ID."""
        ...

    def get_all(self) -> list[GraphProfile]:
        """Retrieve all graph profiles."""
        ...


class ModelProfileRepository(Protocol):
    def get_by_id(self, id: UUID) -> Optional[ModelProfile]:
        """Retrieve a model profile by its ID."""
        ...

    def get_all(self) -> list[ModelProfile]:
        """Retrieve all model profiles."""
        ...
