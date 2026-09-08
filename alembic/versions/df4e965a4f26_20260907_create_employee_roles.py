"""create_employee_roles

Revision ID: df4e965a4f26
Revises: 3079e5941675
Create Date: 2026-09-07 21:34:45.581018

Migration ownership: unknown
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'df4e965a4f26'
down_revision: Union[str, None] = '3079e5941675'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employee_roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("emp_id", sa.Integer, nullable=False),
        sa.Column("role_id", sa.Integer, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("TRUE")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )

    op.create_index("idx_employee_roles_emp_id_role_id", "employee_roles", ["emp_id", "role_id"])


def downgrade() -> None:
    op.drop_index("idx_employee_roles_emp_id_role_id", "employee_roles")
    op.drop_table("employee_roles")
