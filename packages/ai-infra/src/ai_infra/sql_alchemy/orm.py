from __future__ import annotations
from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ai_core.models import GraphProfile


class Base(DeclarativeBase):
    pass


class GraphProfileOrm(Base):
    __tablename__ = "graph_profile"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version_major: Mapped[int] = mapped_column(Integer, nullable=False)
    version_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    graph_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_domain(self) -> GraphProfile:
        return GraphProfile(
            id=self.id,
            name=self.name,
            version_major=self.version_major,
            version_minor=self.version_minor,
            graph_name=self.graph_name,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
        )

    @staticmethod
    def from_domain(graph_profile: GraphProfile) -> GraphProfileOrm:
        return GraphProfileOrm(
            id=graph_profile.id,
            name=graph_profile.name,
            version_major=graph_profile.version_major,
            version_minor=graph_profile.version_minor,
            graph_name=graph_profile.graph_name,
            created_at=graph_profile.created_at,
            updated_at=graph_profile.updated_at,
            is_active=graph_profile.is_active,
        )
