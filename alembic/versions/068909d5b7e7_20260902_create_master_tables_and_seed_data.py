"""create_master_tables_and_seed_data

Revision ID: 068909d5b7e7
Revises: 7a8916fb2031
Create Date: 2026-09-02 10:23:20.524416

Migration ownership: unknown
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '068909d5b7e7'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create roles Table
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.String(50), unique=True, nullable=False),
        sa.Column("name", sa.String(50), unique=True, nullable=False),
        sa.Column("description", sa.String(200), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index("idx_roles_slug", "roles", ["slug"])
    op.create_index("idx_roles_name", "roles", ["name"])

    op.create_unique_constraint("uq_roles_slug", "roles", ["slug"])
    op.create_unique_constraint("uq_roles_name", "roles", ["name"])

    # Insert into roles Table
    op.bulk_insert(
        sa.table(
            "roles",
            sa.column("slug", sa.String(50)),
            sa.column("name", sa.String(50)),
            sa.column("description", sa.String(500)),
            sa.column("is_active", sa.Boolean),
        ),
        [
            {
                "slug": "MANAGER",
                "name": "Manager",
                "description": "Manager",
                "is_active": True,
            },
            {
                "slug": "EMPLOYEE",
                "name": "Employee",
                "description": "Employee",
                "is_active": True,
            },
        ],
    )

    # Create Admin Table
    op.create_table(
        "admins",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(80), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(200), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    op.create_index("idx_admins_email", "admins", ["email"])
    op.create_unique_constraint("uq_admins_email", "admins", ["email"])

    # Insert into Admins Table
    op.bulk_insert(
        sa.table(
            "admins",
            sa.column("name", sa.String),
            sa.column("email", sa.String),
            sa.column("password_hash", sa.String),
            sa.column("is_active", sa.Boolean),
        ),
        [
            {
                "name": "Shubham-Admin",
                "email": "shubhssays@gmail.com",
                "password_hash": "$2a$12$6Mop4DqsxgSWC9FdyxBJ2uWGgYV.H9uXO7Ux/oHzwGIXn0sM2ip5K",
                "is_active": True,
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("idx_roles_slug", table_name="roles")
    op.drop_index("idx_roles_name", table_name="roles")

    op.drop_constraint("uq_roles_slug", table_name="roles", type_="unique")
    op.drop_constraint("uq_roles_name", table_name="roles", type_="unique")

    op.drop_table("roles")

    op.drop_index("idx_admins_email", table_name="admins")
    op.drop_constraint("uq_admins_email", table_name="admins", type_="unique")
    op.drop_table("admins")
