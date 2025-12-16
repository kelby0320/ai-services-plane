from __future__ import annotations
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ai_core.models import GraphProfile, ModelProfile


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


class ModelProfileOrm(Base):
    __tablename__ = "model_profile"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    top_p: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    extra: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    def to_domain(self) -> ModelProfile:
        return ModelProfile(
            id=self.id,
            name=self.name,
            description=self.description,
            model=self.model,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            extra=self.extra or {},
        )

    @staticmethod
    def from_domain(model_profile: ModelProfile) -> ModelProfileOrm:
        return ModelProfileOrm(
            id=model_profile.id,
            name=model_profile.name,
            description=model_profile.description,
            model=model_profile.model,
            created_at=model_profile.created_at,
            updated_at=model_profile.updated_at,
            is_active=model_profile.is_active,
            temperature=model_profile.temperature,
            top_p=model_profile.top_p,
            max_tokens=model_profile.max_tokens,
            extra=model_profile.extra if model_profile.extra else None,
        )
