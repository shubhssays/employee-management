"""create_reset_token

Revision ID: 4c61c12afb97
Revises: df4e965a4f26
Create Date: 2026-09-10 09:26:07.627499

Migration ownership: unknown
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4c61c12afb97'
down_revision: Union[str, None] = 'df4e965a4f26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql_text_create_table_with_constraint = """
        CREATE TABLE reset_token (
            id INT GENERATED ALWAYS AS IDENTITY,
            emp_id INT REFERENCES employees(id) NOT NULL,
            token VARCHAR(100) NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            used_at TIMESTAMPTZ DEFAULT NULL,
            expiry_at TIMESTAMPTZ NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ,
            CONSTRAINT uq_emp_id_token UNIQUE (emp_id, token)
        );
    """
    op.execute(sql_text_create_table_with_constraint)

    sql_text_emp_token_index = """
         CREATE INDEX idx_emp_id_token ON reset_token (emp_id, token) WHERE is_active = TRUE;
    """
    op.execute(sql_text_emp_token_index)

    sql_text_token_index = """
             CREATE INDEX idx_token ON reset_token (token) WHERE is_active = TRUE;
        """
    op.execute(sql_text_token_index)


def downgrade() -> None:
    sql_drop_emp_token_index = """
        DROP INDEX IF EXISTS idx_emp_id_token;
    """
    op.execute(sql_drop_emp_token_index)

    sql_drop_token_index = """
            DROP INDEX IF EXISTS idx_token;
        """
    op.execute(sql_drop_token_index)

    sql_drop_constraint_text = """
        ALTER TABLE reset_token DROP CONSTRAINT IF EXISTS uq_emp_id_token;
    """
    op.execute(sql_drop_constraint_text)

    sql_drop_table_text = """
        DROP TABLE IF EXISTS reset_token;
    """
    op.execute(sql_drop_table_text)
