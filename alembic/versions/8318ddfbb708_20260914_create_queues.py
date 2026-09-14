"""create_queues

Revision ID: 8318ddfbb708
Revises: 4c61c12afb97
Create Date: 2026-09-14 16:31:09.847037

Migration ownership: unknown
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8318ddfbb708'
down_revision: Union[str, None] = '4c61c12afb97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    create_queue_task_status_sql = """
       DO $$
       BEGIN
           IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_status') THEN
               CREATE TYPE task_status AS ENUM ('queued', 'processing', 'completed', 'failed');
           END IF;
       END
       $$;
    """
    op.execute(create_queue_task_status_sql)

    create_table_sql = """
        CREATE TABLE IF NOT EXISTS task_queue (
           id INT GENERATED ALWAYS AS IDENTITY,
           uuid UUID NOT NULL,
           task_type VARCHAR(80) NOT NULL,
           payload JSONB,
           attempts INT DEFAULT 0,                   -- Track retries for failed tasks
           max_attempts INT DEFAULT 3,
           status task_status DEFAULT 'queued' NOT NULL,
           error_msg TEXT,
           run_at TIMESTAMPTZ,
           created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
           updated_at TIMESTAMPTZ,
           CONSTRAINT uq_queues_uuid UNIQUE (uuid)
        )
    """
    op.execute(create_table_sql)

    create_index_sql = """
        CREATE INDEX idx_task_queue_fetch ON task_queue (run_at, id) WHERE status = 'queued'; 
    """
    op.execute(create_index_sql)


def downgrade() -> None:
    drop_task_status_sql = """
           DROP TYPE IF EXISTS task_status CASCADE;
        """
    op.execute(drop_task_status_sql)

    drop_index_sql = """
        DROP INDEX IF EXISTS idx_task_queue_fetch;
    """
    op.execute(drop_index_sql)

    drop_constraint_sql = """
        ALTER TABLE task_queue DROP CONSTRAINT IF EXISTS uq_queues_uuid;
    """
    op.execute(drop_constraint_sql)

    drop_table_sql = """
        DROP TABLE IF EXISTS task_queue;
    """
    op.execute(drop_table_sql)
