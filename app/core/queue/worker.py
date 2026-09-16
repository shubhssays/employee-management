import asyncio
import inspect

from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.enums import TASK_STATUS
from app.core.queue.db import worker_db_engine
from app.core.queue.handler import task_handler_func
from app.modules.task_queue.repository import TaskQueueRepository
from app.shared.schemas.worker import UpdateTask


class TaskWorker:

    def __init__(self, db: AsyncConnection, sleep_interval_secs: int = 60):
        self.db = db
        self.tq_repo = TaskQueueRepository(db)
        self.sleep_interval_secs = sleep_interval_secs

    async def start(self):
        while True:
            print("Worker started...")

            task = await self.claim_work()

            while task:
                await self.process_task(task)
                task = await self.claim_work()

            # All task done or no task found, so sleeping for a minute
            print("Worker is sleeping...")
            await asyncio.sleep(self.sleep_interval_secs)

    async def claim_work(self) -> dict | None:
        async with self.db.begin():
            task = await self.tq_repo.get_one_pending()

            print("***task*** %s", type(task), task)

            if not task:
                return None

            task["attempts"] = int(task["attempts"]) + 1

            task_value_dict = {
                "attempts": task["attempts"],
                "status": TASK_STATUS.PROCESSING,
                "processing_started_at": "NOW"
            }

            await self.update_task(task_value_dict, task)

            return task

    async def process_task(self, current_task):
        print(f"Task with id - {current_task["id"]} started")

        # Finding the handler function and calling it
        task_type = current_task.get("task_type")
        payload = current_task.get("payload")
        schema = task_handler_func[task_type]["schema"]
        handler = task_handler_func[task_type]["handler"]
        payload = schema(**payload)

        error_msg = []

        print("***task_type***, %s", task_type)
        print("***payload***, %s", payload)

        try:
            if inspect.iscoroutinefunction(handler):
                await handler(payload)
            else:
                await asyncio.to_thread(handler, payload)

            task_value_dict = {
                "status": TASK_STATUS.COMPLETED,
            }

            await self.update_task(task_value_dict, current_task)

        except Exception as e:

            print(f"Error occurred while processing task - {current_task["id"]}, Retrying again")

            error_msg.append(str(e))

            current_attempt = int(current_task.get("attempts"))
            max_attempts = current_task.get("max_attempts")

            retry_success = False

            # Retrying the task till it max_attempts
            while current_attempt <= max_attempts and retry_success is False:

                # Calculating dynamically sleep timer
                sleep_time_in_secs = (current_attempt - 1) * 5
                print(f"Worker is sleeping, will retry in {sleep_time_in_secs} seconds")

                # Pausing the worker
                await asyncio.sleep(sleep_time_in_secs)

                print(f"Worker resumed again to process task {current_task["id"]}, attempt number is {current_attempt}")

                try:
                    if inspect.iscoroutinefunction(handler):
                        await handler(payload)
                    else:
                        await asyncio.to_thread(handler, payload)
                    retry_success = True

                except Exception as e:
                    # Collecting error
                    error_msg.append(str(e))

                    # Updating attempts in db for tracking
                    task_value_dict = {
                        "attempts": current_attempt,
                        "error_msg": "*****".join(error_msg)
                    }

                    await self.update_task(task_value_dict, current_task)

                    # Increasing attempt
                    current_attempt += 1

            if retry_success is False:
                print(f"Retry failed for task {current_task["id"]}")
                # Max attempt exhausted, now mark it as failed
                task_value_dict = {
                    "status": TASK_STATUS.FAILED,
                }

                await self.update_task(task_value_dict, current_task)
            else:
                print(f"Retry Successful for task {current_task["id"]}")

                task_value_dict = {
                    "status": TASK_STATUS.COMPLETED,
                }

                await self.update_task(task_value_dict, current_task)

    async def update_task(self, task_value_dict: dict, current_task: dict) -> None:
        task_value = UpdateTask(**task_value_dict)
        task_where_cond_dict = {
            "id": current_task["id"]
        }
        if self.db.in_transaction():
            await self.tq_repo.update(task_value, task_where_cond_dict)
        else:
            async with self.db.begin():
                await self.tq_repo.update(task_value, task_where_cond_dict)


async def main():
    async with worker_db_engine.connect() as db:
        task_worker1 = TaskWorker(db)

        # start the worker
        await task_worker1.start()


asyncio.run(main())
