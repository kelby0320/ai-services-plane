"""add_model_profile_config_fields

Revision ID: 38faba8f1474
Revises: 355dea3fc267
Create Date: 2025-12-15 16:04:06.612419

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "38faba8f1474"
down_revision: Union[str, Sequence[str], None] = "355dea3fc267"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("model_profile", sa.Column("temperature", sa.Float(), nullable=True))
    op.add_column("model_profile", sa.Column("top_p", sa.Float(), nullable=True))
    op.add_column("model_profile", sa.Column("max_tokens", sa.Integer(), nullable=True))
    op.add_column("model_profile", sa.Column("extra", sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("model_profile", "extra")
    op.drop_column("model_profile", "max_tokens")
    op.drop_column("model_profile", "top_p")
    op.drop_column("model_profile", "temperature")
