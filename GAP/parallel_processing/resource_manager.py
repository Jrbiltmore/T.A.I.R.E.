"""
resource_manager.py

This module is responsible for managing computational resources to facilitate parallel processing. 
It integrates various techniques to allocate and manage resources efficiently across multiple tasks.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
import multiprocessing
from datetime import datetime

class ResourceManager:
    def __init__(self, resources_file):
        """
        Initialize the ResourceManager with a list of resources.
        
        :param resources_file: Path to the JSON file containing resources.
        """
        self.resources_file = resources_file
        self.resources = self.load_resources()
        self.allocation = []

    def load_resources(self):
        """
        Load resources from the provided JSON file.
        
        :return: List of resources.
        """
        try:
            with open(self.resources_file, 'r') as file:
                resources = json.load(file)
                return resources.get("resources", [])
        except Exception as e:
            print(f"Error occurred while loading resources: {e}")
            return []

    def allocate_resources(self, tasks):
        """
        Allocate resources to the specified tasks.
        
        :param tasks: List of tasks to allocate resources to.
        """
        for task in tasks:
            try:
                # Placeholder for resource allocation logic
                allocation = self.allocate_resource(task)
                self.allocation.append({"task": task, "allocation": allocation})
                print(f"Resources allocated for task '{task['name']}'")
            except Exception as e:
                print(f"Error occurred while allocating resources for task '{task['name']}': {e}")

    def allocate_resource(self, task):
        """
        Allocate a specific resource to a task.
        
        :param task: The task to allocate resources to.
        :return: Allocation information.
        """
        # Placeholder for actual allocation logic, returning example data
        return {
            "cpu_cores": min(multiprocessing.cpu_count(), task.get("cpu_cores", 1)),
            "memory": task.get("memory", "1GB")
        }

    def save_allocation(self, file_path):
        """
        Save the resource allocation data to a JSON file.
        
        :param file_path: Path to the file where the allocation data will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.allocation, file, indent=4)
            print(f"Resource allocation successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving resource allocation: {e}")

    def load_allocation(self, file_path):
        """
        Load resource allocation data from a JSON file.
        
        :param file_path: Path to the file from which the allocation data will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.allocation = json.load(file)
            print(f"Resource allocation successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading resource allocation: {e}")

    def print_summary(self):
        """
        Print a summary of the resource allocation.
        """
        print("Resource Allocation Summary:")
        for i, alloc in enumerate(self.allocation):
            print(f"Allocation {i + 1}: Task '{alloc['task']['name']}' - CPU Cores: {alloc['allocation']['cpu_cores']}, Memory: {alloc['allocation']['memory']}")

if __name__ == "__main__":
    resources_file_path = 'resources.json'
    allocation_file_path = 'resource_allocation.json'
    tasks_file_path = 'parallel_tasks.json'

    # Ensure resources.json exists
    if not os.path.exists(resources_file_path):
        print(f"{resources_file_path} not found. Creating default resources file.")
        default_resources = {
            "resources": [
                {
                    "name": "CPU",
                    "type": "processor",
                    "total": multiprocessing.cpu_count()
                },
                {
                    "name": "Memory",
                    "type": "memory",
                    "total": "16GB"
                }
            ]
        }
        with open(resources_file_path, 'w') as file:
            json.dump(default_resources, file, indent=4)

    # Ensure parallel_tasks.json exists
    if not os.path.exists(tasks_file_path):
        print(f"{tasks_file_path} not found. Creating default tasks file.")
        default_tasks = {
            "tasks": [
                {
                    "name": "Example Task 1",
                    "cpu_cores": 2,
                    "memory": "2GB"
                },
                {
                    "name": "Example Task 2",
                    "cpu_cores": 4,
                    "memory": "4GB"
                }
            ]
        }
        with open(tasks_file_path, 'w') as file:
            json.dump(default_tasks, file, indent=4)

    manager = ResourceManager(resources_file_path)
    manager.load_resources()
    manager.allocate_resources(default_tasks["tasks"])
    manager.save_allocation(allocation_file_path)
    manager.print_summary()
