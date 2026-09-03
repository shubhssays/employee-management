"""create_organization_table

Revision ID: b1a3c0b5cc85
Revises: 068909d5b7e7
Create Date: 2026-09-02 13:41:24.130263

Migration ownership: unknown
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b1a3c0b5cc85"
down_revision: str | None = "068909d5b7e7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create Organization Table
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("slug", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True, server_default=None),
        sa.Column(
            "created_by",
            sa.Integer,
            sa.ForeignKey("admins.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "updated_by", sa.Integer, sa.ForeignKey("admins.id", ondelete="RESTRICT"), nullable=True
        ),
    )

    # Add Index
    op.create_index("idx_organizations_slug", "organizations", ["slug"])


def downgrade() -> None:
    # Drop Index
    op.drop_index("idx_organizations_slug", table_name="organizations")

    # Drop Organization Table
    op.drop_table("organizations")
