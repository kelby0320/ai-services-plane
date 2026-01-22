"""seed baseline profiles

Revision ID: d00f8a9cff48
Revises: 355dea3fc267
Create Date: 2026-01-18 10:51:41.833465

"""

from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d00f8a9cff48"
down_revision: Union[str, Sequence[str], None] = "355dea3fc267"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    graph_profile_table = sa.table(
        "graph_profile",
        sa.column("id", sa.Uuid()),
        sa.column("name", sa.String(length=255)),
        sa.column("version_major", sa.Integer()),
        sa.column("version_minor", sa.Integer()),
        sa.column("graph_name", sa.String(length=255)),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
        sa.column("is_active", sa.Boolean()),
    )
    model_profile_table = sa.table(
        "model_profile",
        sa.column("id", sa.Uuid()),
        sa.column("name", sa.String(length=255)),
        sa.column("description", sa.Text()),
        sa.column("model", sa.String(length=255)),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
        sa.column("is_active", sa.Boolean()),
        sa.column("temperature", sa.Float()),
        sa.column("top_p", sa.Float()),
        sa.column("max_tokens", sa.Integer()),
    )

    now = datetime.now(timezone.utc)
    op.bulk_insert(
        graph_profile_table,
        [
            {
                "id": "572d61fc-cf7a-4c15-9534-32000b1a9572",
                "name": "default_v1",
                "version_major": 0,
                "version_minor": 1,
                "graph_name": "default_v1",
                "created_at": now,
                "updated_at": now,
                "is_active": True,
            }
        ],
    )
    op.bulk_insert(
        model_profile_table,
        [
            {
                "id": "86d4ea3b-b9de-4e32-adb2-41f2f4bff0bd",
                "name": "GPT OSS 120b",
                "description": "",
                "model": "openai/gpt-oss-120b",
                "created_at": now,
                "updated_at": now,
                "is_active": True,
                "temperature": None,
                "top_p": None,
                "max_tokens": None,
            }
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    graph_profile_table = sa.table(
        "graph_profile",
        sa.column("id", sa.Uuid()),
    )
    model_profile_table = sa.table(
        "model_profile",
        sa.column("id", sa.Uuid()),
    )
    op.execute(
        sa.delete(graph_profile_table).where(
            graph_profile_table.c.id == "572d61fc-cf7a-4c15-9534-32000b1a9572"
        )
    )
    op.execute(
        sa.delete(model_profile_table).where(
            model_profile_table.c.id == "86d4ea3b-b9de-4e32-adb2-41f2f4bff0bd"
        )
    )
