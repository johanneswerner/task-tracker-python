"""Task Tracker CLI.

This module provides a command-line interface for managing tasks.
Tasks can be added, updated, deleted, marked as in-progress or done, and listed.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

TASKS_FILE = "tasks.json"

class TaskManager:
    """A class to manage tasks.

    Attributes:
        tasks_file (str): The path to the tasks file.
        load_tasks(): Loads tasks from the tasks file.
        save_tasks(): Saves the current list of tasks to the tasks file.
        add_task(description): Adds a new task to the task list.
        update_task(task_id, description): Updates the description of an existing task.
        delete_task(task_id): Deletes a task by its ID.
        mark_task_in_progress(task_id): Marks a task as in-progress by its ID.
        mark_task_done(task_id): Marks a task as done by its ID.
        list_tasks(status): Lists tasks, optionally filtered by status.

    """

    def __init__(self, tasks_file: str = TASKS_FILE) -> None:
        """Initialize the TaskManager with a tasks file.

        Args:
            tasks_file (str): The path to the tasks file.

        Returns:
            None

        """
        self.tasks_file = tasks_file
        self.tasks = self.load_tasks()

    def load_tasks(self) -> list:
        """Load tasks from the tasks file.

        Returns:
            list: A list of tasks loaded from the file.

        """
        if not Path(self.tasks_file).exists():
            return []
        with Path(self.tasks_file).open("r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Error: The tasks file contains invalid JSON.")
                return []

    def save_tasks(self) -> None:
        """Save the current list of tasks to the tasks file.

        Returns:
            None

        """
        with Path(self.tasks_file).open("w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, description: str) -> None:
        """Add a new task to the task list.

        Args:
            description (str): The description of the task to add.

        Returns:
            None

        """
        if not description.strip():
            print("Task description cannot be empty.")
            return
        task_id = max([task["id"] for task in self.tasks], default=0) + 1
        current_time = datetime.now().isoformat()
        self.tasks.append({
            "id": task_id,
            "description": description,
            "status": "todo",
            "createdAt": current_time,
            "updatedAt": current_time,
        })
        self.save_tasks()
        print(f"Task added: {description}")

    def update_task(self, task_id: int, description: str) -> None:
        """Update the description of an existing task.

        Args:
            task_id (int): The ID of the task to update.
            description (str): The new description of the task.

        Returns:
            None

        """
        for task in self.tasks:
            if task["id"] == task_id:
                if description.strip():
                    task["description"] = description
                task["updatedAt"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task updated: {task}")
                return
        print("Task not found.")

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            None

        """
        if not any(task["id"] == task_id for task in self.tasks):
            print("Task not found.")
            return
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
        print(f"Task {task_id} deleted.")

    def mark_task_in_progress(self, task_id: int) -> None:
        """Mark a task as in-progress by its ID.

        Args:
            task_id (int): The ID of the task to mark as in-progress.

        Returns:
            None

        """
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "in-progress"
                self.save_tasks()
                print(f"Task {task_id} marked as in-progress.")
                return
        print("Task not found.")

    def mark_task_done(self, task_id: int) -> None:
        """Mark a task as done by its ID.

        Args:
            task_id (int): The ID of the task to mark as done.

        Returns:
            None

        """
        if not any(task["id"] == task_id for task in self.tasks):
            print("Task not found.")
            return
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "done"
                self.save_tasks()
                print(f"Task {task_id} marked as done.")
                return
        print("Task not found.")

    def list_tasks(self, status: Optional[str] = None) -> None:
        """List tasks, optionally filtered by status.

        Args:
            status (Optional[str], optional): The status to filter tasks by. Defaults to None.

        Returns:
            None

        """
        filtered_tasks = self.tasks
        if status:
            filtered_tasks = [task for task in self.tasks if task["status"] == status]
        for task in filtered_tasks:
            print(f"ID: {task['id']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print(f"Created At: {task['createdAt']}")
            print(f"Updated At: {task['updatedAt']}")
            print()
        if not filtered_tasks:
            print("No tasks found.")

def main() -> None:
    """Run main function to run the Task Tracker CLI.

    Returns:
        None

    """
    task_manager = TaskManager()

    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Description of the task")

    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("id", type=int, help="ID of the task to update")
    update_parser.add_argument(
        "description",
        type=str,
        help="New description of the task"
    )

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete")

    mark_in_progress_parser = subparsers.add_parser(
        "mark-in-progress",
        help="Mark a task as in-progress"
    )
    mark_in_progress_parser.add_argument(
        "id",
        type=int,
        help="ID of the task to mark as in-progress"
    )

    mark_done_parser = subparsers.add_parser("mark-done", help="Mark a task as done")
    mark_done_parser.add_argument("id", type=int, help="ID of the task to mark as done")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "status",
        nargs="?",
        choices=["todo", "in-progress", "done"],
        help="Status of tasks to list"
    )

    args = parser.parse_args()

    if args.command == "add":
        task_manager.add_task(args.description)
    elif args.command == "update":
        task_manager.update_task(args.id, args.description)
    elif args.command == "delete":
        task_manager.delete_task(args.id)
    elif args.command == "mark-in-progress":
        task_manager.mark_task_in_progress(args.id)
    elif args.command == "mark-done":
        task_manager.mark_task_done(args.id)
    elif args.command == "list":
        task_manager.list_tasks(args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
