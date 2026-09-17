from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db.session import AsyncSessionLocal
from app.modules.task_queue.repository import TaskQueueRepository

is_restart_stucked_tasks_running = False


async def restart_stucked_tasks():
    global is_restart_stucked_tasks_running

    if is_restart_stucked_tasks_running:
        print("restart_stucked_tasks is already running")
        return

    is_restart_stucked_tasks_running = True

    try:
        async with AsyncSessionLocal() as db:
            async with db.begin():
                tq_repo = TaskQueueRepository(db)

                # Fetching stucked jobs
                stucked_tasks = await tq_repo.get_stucked_jobs()
                print("Stucked task found", len(stucked_tasks))

                # Resetting them
                if stucked_tasks:
                    stucked_task_ids = [stucked_task["id"] for stucked_task in stucked_tasks]
                    await tq_repo.update_stucked_jobs(stucked_task_ids)
                else:
                    print("No stucked task found")



    except Exception as e:
        print("Error in cron restart_stucked_tasks ", e)
    finally:
        # Making flag false when its execution is already completed
        is_restart_stucked_tasks_running = False


scheduler = AsyncIOScheduler()

cron_list = [
    {
        "handler": restart_stucked_tasks,
        # "hour": 0,
        "minute": "*"
    }
]

for cron in cron_list:
    scheduler.add_job(
        cron["handler"],
        trigger="cron",
        # hour=cron["hour"],
        minute=cron["minute"]
    )
