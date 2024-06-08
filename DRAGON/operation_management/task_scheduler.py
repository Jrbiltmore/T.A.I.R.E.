"""
task_scheduler.py

This module is responsible for scheduling and prioritizing tasks. 
It integrates multiple scheduling techniques to ensure tasks are executed efficiently and effectively.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
from datetime import datetime, timedelta
import heapq

class TaskScheduler:
    def __init__(self, tasks_file):
        """
        Initialize the TaskScheduler with a list of tasks.
        
        :param tasks_file: Path to the JSON file containing tasks.
        """
        self.tasks_file = tasks_file
        self.tasks = self.load_tasks()
        self.schedule = []

    def load_tasks(self):
        """
        Load tasks from the provided JSON file.
        
        :return: List of tasks.
        """
        try:
            with open(self.tasks_file, 'r') as file:
                tasks = json.load(file)
                return tasks.get("tasks", [])
        except Exception as e:
            print(f"Error occurred while loading tasks: {e}")
            return []

    def schedule_tasks(self):
        """
        Schedule tasks based on their priority and execution time.
        """
        try:
            heapq.heapify(self.tasks)
            while self.tasks:
                task = heapq.heappop(self.tasks)
                execution_time = datetime.now() + timedelta(seconds=task['duration'])
                self.schedule.append({"task": task, "execution_time": execution_time.isoformat()})
                print(f"Task '{task['name']}' scheduled for execution at {execution_time}.")
        except Exception as e:
            print(f"Error occurred while scheduling tasks: {e}")

    def save_schedule(self, file_path):
        """
        Save the scheduled tasks to a JSON file.
        
        :param file_path: Path to the file where the schedule will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.schedule, file, indent=4)
            print(f"Task schedule successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving task schedule: {e}")

    def load_schedule(self, file_path):
        """
        Load scheduled tasks from a JSON file.
        
        :param file_path: Path to the file from which the schedule will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.schedule = json.load(file)
            print(f"Task schedule successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading task schedule: {e}")

    def print_summary(self):
        """
        Print a summary of the scheduled tasks.
        """
        print("Task Schedule:")
        for i, entry in enumerate(self.schedule):
            print(f"Task {i + 1}: '{entry['task']['name']}' scheduled for {entry['execution_time']}")

if __name__ == "__main__":
    tasks_file_path = 'tasks.json'
    schedule_file_path = 'task_schedule.json'

    # Example content for tasks.json
    if not os.path.exists(tasks_file_path):
        default_tasks = {
            "tasks": [
                {
                    "name": "Example Task 1",
                    "priority": 1,
                    "duration": 30  # duration in seconds
                },
                {
                    "name": "Example Task 2",
                    "priority": 2,
                    "duration": 45  # duration in seconds
                }
            ]
        }
        with open(tasks_file_path, 'w') as file:
            json.dump(default_tasks, file, indent=4)

    scheduler = TaskScheduler(tasks_file_path)
    scheduler.schedule_tasks()
    scheduler.save_schedule(schedule_file_path)
    scheduler.print_summary()
