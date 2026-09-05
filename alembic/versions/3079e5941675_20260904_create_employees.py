"""create_employees

Revision ID: 3079e5941675
Revises: b1a3c0b5cc85
Create Date: 2026-09-04 13:04:43.258834

Migration ownership: unknown
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

from app.core.enums import DepartmentType

# revision identifiers, used by Alembic.
revision: str = '3079e5941675'
down_revision: Union[str, None] = 'b1a3c0b5cc85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create the PostgreSQL ENUM type safely (idempotent)
    op.execute(sa.text("""
        DO $$ BEGIN
            CREATE TYPE department_enum AS ENUM ('DEVELOPER', 'SUPPORT', 'HR', 'MANAGEMENT');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """))

    # 2. Create Employees Table using postgresql.ENUM with create_type=False
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=True),
        sa.Column("email", sa.String(50), nullable=False),
        sa.Column("mobile", sa.String(20), nullable=True),
        sa.Column("password_hash", sa.String(80), nullable=False),
        sa.Column("address", sa.String(200), nullable=True),
        sa.Column(
            "department",
            postgresql.ENUM(
                "DEVELOPER", "SUPPORT", "HR", "MANAGEMENT",
                name="department_enum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("organization_id", sa.Integer, sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True, server_default=None),
        sa.Column("created_by_emp", sa.Integer, sa.ForeignKey("employees.id"), nullable=True),
        sa.Column("created_by_admin", sa.Integer, sa.ForeignKey("admins.id"), nullable=True),
        sa.Column("updated_by_emp", sa.Integer, sa.ForeignKey("employees.id"), nullable=True),
        sa.Column("updated_by_admin", sa.Integer, sa.ForeignKey("admins.id"), nullable=True),
    )

    # Add Check Constraints
    op.create_check_constraint(
        constraint_name="check_created_by_emp_or_created_by_admin_positive",
        table_name="employees",
        condition="created_by_emp IS NOT NULL OR created_by_admin IS NOT NULL",
    )

    op.create_check_constraint(
        constraint_name="check_created_by_emp_or_created_by_admin_negative",
        table_name="employees",
        condition="created_by_emp IS NULL OR created_by_admin IS NULL",
    )

    # Add Indexes
    op.create_index("idx_employees_email", "employees", columns=["email"])
    op.create_index("idx_employees_mobile", "employees", columns=["mobile"])


def downgrade() -> None:
    op.drop_constraint("check_created_by_emp_or_created_by_admin_negative", "employees")
    op.drop_constraint("check_created_by_emp_or_created_by_admin_positive", "employees")
    op.drop_index("idx_employees_mobile", table_name="employees")
    op.drop_index("idx_employees_email", table_name="employees")
    op.drop_table("employees")
    op.execute(sa.text("DROP TYPE IF EXISTS department_enum;"))
