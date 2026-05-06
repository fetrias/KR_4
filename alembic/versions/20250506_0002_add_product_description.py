"""add product description

Revision ID: 20250506_0002
Revises: 20250506_0001
Create Date: 2025-05-06 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "20250506_0002"
down_revision = "20250506_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
            server_default=sa.text("''"),
        ),
    )


def downgrade() -> None:
    op.drop_column("products", "description")
