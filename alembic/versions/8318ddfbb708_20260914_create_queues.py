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
               CREATE TYPE task_status AS ENUM ('QUEUED', 'PROCESSING', 'COMPLETED', 'FAILED');
           END IF;
       END
       $$;
    """
    op.execute(create_queue_task_status_sql)

    create_queue_priority_sql = """
           DO $$
           BEGIN
               IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'priority_type') THEN
                   CREATE TYPE priority_type AS ENUM ('HIGH', 'MEDIUM', 'LOW');
               END IF;
           END
           $$;
        """
    op.execute(create_queue_priority_sql)

    create_table_sql = """
        CREATE TABLE IF NOT EXISTS task_queue (
           id INT GENERATED ALWAYS AS IDENTITY,
           identifier VARCHAR(200) NOT NULL,
           task_type VARCHAR(80) NOT NULL,
           payload JSONB,
           attempts INT DEFAULT 0,                   -- Track retries for failed tasks
           max_attempts INT DEFAULT 3,
           priority priority_type DEFAULT 'MEDIUM' NOT NULL,                   -- Track priority for failed tasks
           status task_status DEFAULT 'QUEUED' NOT NULL,
           error_msg TEXT DEFAULT NULL,
           run_at TIMESTAMPTZ DEFAULT NULL,
           processing_started_at TIMESTAMPTZ DEFAULT NULL,
           created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
           updated_at TIMESTAMPTZ,
           CONSTRAINT uq_queues_identifier UNIQUE (identifier)
        )
    """
    op.execute(create_table_sql)

    create_index_run_at_id_sql = """
        CREATE INDEX idx_task_queue_fetch ON task_queue (run_at, id) WHERE status = 'QUEUED'; 
    """
    op.execute(create_index_run_at_id_sql)

    create_index_run_identifier_sql = """
            CREATE INDEX idx_task_queue_identifier ON task_queue (identifier); 
        """
    op.execute(create_index_run_identifier_sql)


def downgrade() -> None:
    drop_task_status_sql = """
           DROP TYPE IF EXISTS task_status CASCADE;
        """
    op.execute(drop_task_status_sql)

    drop_priority_type_sql = """
               DROP TYPE IF EXISTS priority_type CASCADE;
            """
    op.execute(drop_priority_type_sql)

    drop_index_run_at_id_sql = """
        DROP INDEX IF EXISTS idx_task_queue_fetch;
    """
    op.execute(drop_index_run_at_id_sql)

    drop_index_run_identifier_sql = """
            DROP INDEX IF EXISTS idx_task_queue_identifier;
        """
    op.execute(drop_index_run_identifier_sql)

    drop_constraint_sql = """
        ALTER TABLE task_queue DROP CONSTRAINT IF EXISTS identifier;
    """
    op.execute(drop_constraint_sql)

    drop_table_sql = """
        DROP TABLE IF EXISTS task_queue;
    """
    op.execute(drop_table_sql)
