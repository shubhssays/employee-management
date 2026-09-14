from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import TASK_PRIORITY, TASK_STATUS
from app.core.security import generate_opaque_token
from app.db.utils import get_dynamic_value
from app.shared.schemas.worker import AddTask

table_name = "task_queue"


class TaskQueueRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_queue: AddTask) -> dict:
        columns_str = "(identifier, task_type, payload, attempts, max_attempts, priority, status, error_msg, run_at)"
        values_str = get_dynamic_value(columns_str)
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
            "error_msg": None
        }
        result = await self.db.execute(text(query_str), values)
        rows = result.fetchall()
        row, *_ = rows
        return row

    # async def update(self, task_queue: TaskQueue, data: dict) -> TaskQueue:
    #     for field, value in data:
    #         setattr(task_queue, field, value)
    #
    #     await self.db.flush()
    #     return task_queue

    # async def get_one(self) -> TaskQueue:
    #     result = await self.db.execute(select(TaskQueue).where(
    #         TaskQueue.status == TASK_STATUS.QUEUED,
    #         TaskQueue.
    #     ))
