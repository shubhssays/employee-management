import json
import time
from datetime import datetime

file_path = "/test.json"


class TaskWorker:

    def __init__(self, poll_interval_secs: int = 5):
        self.poll_interval_secs = poll_interval_secs

    def start(self):
        while True:
            print("Worker started...")

            task = self.fetch_work()

            while task:
                self.process_task(task)
                task = self.fetch_work()

            # All task done or no task found, so sleeping for a minute
            print("Worker is sleeping...")
            time.sleep(self.poll_interval_secs)

    def fetch_work(self):
        with open(file_path, 'r') as file:
            tasks = json.load(file)
            for task in tasks:
                if task["status"] == 'pending':
                    return task

    def process_task(self, current_task):
        print(f"Task with id - {current_task["id"]} started")

        # Sleeping for 3 seconds to mimic the processing
        time.sleep(3)

        # Finding the index of current task
        with open(file_path, "r") as file:
            tasks = json.load(file)

            if tasks:

                task_index = None

                for index, task in enumerate(tasks):
                    if task["id"] == current_task["id"]:
                        task_index = index
                        break

                # Updating status of task
                tasks[task_index]["status"] = "completed"
                tasks[task_index]["completed"] = str(datetime.now())

                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(tasks, file, indent=4)

                print(f"Task with id - {current_task["id"]} is completed")

            else:
                raise ValueError("Invalid task found %s ", current_task)


tw = TaskWorker(60)
tw.start()
