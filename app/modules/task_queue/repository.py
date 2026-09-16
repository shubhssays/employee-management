from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import TASK_PRIORITY, TASK_STATUS
from app.core.security import generate_opaque_token
from app.db.utils import build_sql_values_clause_for_insert, build_sql_set_clause_for_update, build_sql_where_clause, \
    rows_to_dict_list
from app.shared.schemas.worker import AddTask, UpdateTask

table_name = "task_queue"


class TaskQueueRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_queue: AddTask) -> dict[Any, Any] | list[Any] | None:
        columns_str = "(identifier, task_type, payload, attempts, max_attempts, priority, status, error_msg, run_at)"
        values_str = build_sql_values_clause_for_insert(columns_str)
        returning_str = " RETURNING id, identifier"
        query_str = f"INSERT INTO {table_name} {columns_str} {values_str} {returning_str}"

        identifier = task_queue.identifier

        if not identifier:
            if task_queue.payload:
                identifier = generate_opaque_token(task_queue.payload)
            else:
                raise ValueError("Provide identifier or valid payload")

        values = {
            "identifier": identifier,
            "task_type": task_queue.task_type,
            "payload": task_queue.payload,
            "attempts": task_queue.attempts or 0,
            "max_attempts": task_queue.max_attempts or 5,
            "priority": task_queue.priority or TASK_PRIORITY.MEDIUM,
            "status": TASK_STATUS.QUEUED,
            "run_at": task_queue.run_at,
            "processing_started_at": None,
            "error_msg": None
        }
        result = await self.db.execute(text(query_str), values)
        rows = result.fetchall()
        rows = result.fetchall()
        return rows_to_dict_list(rows)

    async def update(self, task_queue: UpdateTask, where_condition: dict) -> dict[Any, Any] | list[Any] | None:
        task_queue_dict = task_queue.model_dump(exclude_none=True)
        if task_queue_dict.get("updated_at", None) is None:
            task_queue_dict["updated_at"] = "NOW"

        column_details = build_sql_set_clause_for_update(task_queue_dict)
        where_details = build_sql_where_clause(where_condition)
        returning_str = " RETURNING id, identifier"
        values = column_details["column_value"] | where_details["where_value"]
        query_str = f"UPDATE {table_name} {column_details["column_str"]} {where_details["where_str"]} {returning_str}"
        result = await self.db.execute(text(query_str), values)
        rows = result.fetchall()
        return rows_to_dict_list(rows)

    async def get_one_pending(self) -> dict[Any, Any] | list[Any] | None:
        columns = "id, identifier, task_type, payload, attempts, max_attempts, priority, status, error_msg, run_at"
        query_str = f"""SELECT {columns} FROM {table_name} WHERE attempts < max_attempts AND status = :status AND (run_at IS NULL OR run_at < NOW())
           ORDER BY
           CASE priority
               WHEN '{TASK_PRIORITY.HIGH}' THEN 1
               WHEN '{TASK_PRIORITY.MEDIUM}' THEN 2
               WHEN '{TASK_PRIORITY.LOW}' THEN 3
           END,
           created_at ASC LIMIT 1 FOR UPDATE SKIP LOCKED;"""
        values = {
            "status": TASK_STATUS.QUEUED
        }
        result = await self.db.execute(text(query_str), values)
        rows = result.fetchall()
        return rows_to_dict_list(rows)
