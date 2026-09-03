"""tasks_learning_module

TEMPORARY LEARNING MODULE
=========================
This migration creates the `tasks` table used exclusively by the
tasks learning module (app/modules/tasks/).

It is safe to roll back and delete when you remove the module.
See: docs/learning/remove-tasks-module.md

Revision ID: 7a8916fb2031
Revises:
Create Date: 2026-09-02

LEARNING NOTE — How this migration was created:
  1. The Task ORM model was written in app/modules/tasks/models.py
  2. The model was registered in app/db/base.py (for Alembic discovery)
  3. `uv run alembic revision --autogenerate -m "tasks_learning_module"`
     was used to generate the initial structure.
  4. The output was reviewed and written here manually for clarity.

  This is the normal workflow for every new module:
    model → register in base.py → alembic revision → review → upgrade

  To apply:   uv run alembic upgrade head
  To revert:  uv run alembic downgrade -1
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Revision identifiers — used by Alembic to build the migration chain.
revision: str = "7a8916fb2031"
down_revision: str | None = None  # No prior migrations exist yet
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Create the tasks table and task_status_enum PostgreSQL type.

    LEARNING NOTE:
      - We create the Enum type explicitly so that downgrade() can drop it.
        SQLAlchemy would create it implicitly, but then Alembic's downgrade
        cannot drop it reliably.
      - `server_default` values mirror the model's `server_default` so
        that existing rows get sensible defaults when columns are added
        to a table that already has data.
      - `nullable=False` → NOT NULL constraint at DB level.
      - `index=True` on `title` → SQLAlchemy creates the index automatically
        via op.create_index (we do it explicitly below for clarity).
    """
    # 1. Create the PostgreSQL ENUM type safely (idempotent)
    op.execute(sa.text("""
        DO $$ BEGIN
            CREATE TYPE task_status_enum AS ENUM ('TODO', 'IN_PROGRESS', 'COMPLETED');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """))

    # 2. Create the tasks table
    op.create_table(
        "tasks",
        sa.Column(
            "id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(200),
            nullable=False,
            comment="Short summary of the task.",
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
            comment="Optional longer description of the task.",
        ),
        sa.Column(
            "status",
            sa.dialects.postgresql.ENUM(
                "TODO", "IN_PROGRESS", "COMPLETED",
                name="task_status_enum",
                create_type=False,
            ),
            nullable=False,
            server_default="TODO",
            comment="Current lifecycle state of the task.",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    # Index on title (single column — for title-based lookups)
    op.create_index("ix_tasks_title", "tasks", ["title"])

    # Composite index on (status, created_at) — for filtered+sorted queries
    op.create_index("ix_tasks_status_created_at",
                    "tasks", ["status", "created_at"])


def downgrade() -> None:
    """
    Drop the tasks table and task_status_enum PostgreSQL type.

    LEARNING NOTE:
      Reversal order matters — drop indexes first, then the table,
      then the dependent enum type. If you reverse this order,
      PostgreSQL will raise an error because the table still uses the type.

    SAFETY NOTE:
      Running `alembic downgrade -1` will permanently delete all rows
      in the tasks table. Only do this when you are sure you want to
      remove the table and its data.
    """
    # Drop indexes first
    op.drop_index("ix_tasks_status_created_at", table_name="tasks")
    op.drop_index("ix_tasks_title", table_name="tasks")

    # Drop the table
    op.drop_table("tasks")

    # Drop the PostgreSQL enum type (must be after the table is dropped)
    task_status_enum = sa.Enum(name="task_status_enum")
    task_status_enum.drop(op.get_bind())
