"""
Command-Line Task Manager Application
Features: CRUD operations, priority levels, due dates,
JSON persistence, OOP design, input validation, and error handling.
"""

import json
import os
from datetime import datetime


class Task:
    def __init__(self, task_id: int, title: str, priority: str, due_date: str, completed: bool = False):
        self.task_id = task_id
        self.title = title
        self.priority = priority.upper()
        self.due_date = due_date
        self.completed = completed

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            priority=data["priority"],
            due_date=data["due_date"],
            completed=data.get("completed", False),
        )

    def __str__(self) -> str:
        status = "✓ Done" if self.completed else "✗ Pending"
        return f"[{self.task_id}] {self.title} | Priority: {self.priority} | Due: {self.due_date} | Status: {status}"


class TaskManager:
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks: list[Task] = []
        self._load_tasks()

    def _load_tasks(self) -> None:
        if not os.path.exists(self.storage_file):
            self.tasks = []
            return
        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not read {self.storage_file} ({e}). Starting fresh.")
            self.tasks = []

    def save_tasks(self) -> None:
        with open(self.storage_file, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, title: str, priority: str, due_date: str) -> Task:
        new_id = max([t.task_id for t in self.tasks], default=0) + 1
        task = Task(new_id, title, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def list_tasks(self) -> list[Task]:
        return self.tasks

    def update_task(self, task_id: int, new_title: str = None, new_priority: str = None, new_due_date: str = None) -> bool:
        for task in self.tasks:
            if task.task_id == task_id:
                if new_title:
                    task.title = new_title
                if new_priority:
                    task.priority = new_priority.upper()
                if new_due_date:
                    task.due_date = new_due_date
                self.save_tasks()
                return True
        return False

    def mark_completed(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.task_id == task_id:
                task.completed = True
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(self.tasks) < initial_count:
            self.save_tasks()
            return True
        return False


def validate_date(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def main():
    manager = TaskManager()

    while True:
        print("\n=== TASK MANAGER CLI ===")
        print("1. View Tasks (Read)")
        print("2. Add Task (Create)")
        print("3. Update Task (Update)")
        print("4. Mark Task as Complete")
        print("5. Delete Task (Delete)")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            tasks = manager.list_tasks()
            if not tasks:
                print("No tasks available.")
            else:
                print("\nTask List:")
                for task in tasks:
                    print(task)

        elif choice == "2":
            title = input("Enter Task Title: ").strip()
            if not title:
                print("Error: Title cannot be empty.")
                continue

            priority = input("Enter Priority (LOW / MEDIUM / HIGH): ").strip().upper()
            if priority not in ["LOW", "MEDIUM", "HIGH"]:
                print("Invalid priority. Defaulting to MEDIUM.")
                priority = "MEDIUM"

            due_date = input("Enter Due Date (YYYY-MM-DD): ").strip()
            if not validate_date(due_date):
                print("Error: Invalid date format. Use YYYY-MM-DD.")
                continue

            new_task = manager.add_task(title, priority, due_date)
            print(f"Task added successfully: {new_task}")

        elif choice == "3":
            try:
                task_id = int(input("Enter Task ID to update: "))
                title = input("Enter New Title (leave blank to keep current): ").strip()
                priority = input("Enter New Priority (LOW/MEDIUM/HIGH) (leave blank to keep current): ").strip().upper()
                due_date = input("Enter New Due Date (YYYY-MM-DD) (leave blank to keep current): ").strip()

                if priority and priority not in ["LOW", "MEDIUM", "HIGH"]:
                    print("Invalid priority provided. Skipping priority change.")
                    priority = None

                if due_date and not validate_date(due_date):
                    print("Invalid date format. Skipping due date change.")
                    due_date = None

                updated = manager.update_task(
                    task_id,
                    new_title=title if title else None,
                    new_priority=priority if priority else None,
                    new_due_date=due_date if due_date else None,
                )
                if updated:
                    print("Task updated successfully!")
                else:
                    print(f"Task ID {task_id} not found.")
            except ValueError:
                print("Error: Task ID must be a number.")

        elif choice == "4":
            try:
                task_id = int(input("Enter Task ID to mark completed: "))
                if manager.mark_completed(task_id):
                    print(f"Task #{task_id} marked as completed!")
                else:
                    print(f"Task ID {task_id} not found.")
            except ValueError:
                print("Error: Task ID must be a number.")

        elif choice == "5":
            try:
                task_id = int(input("Enter Task ID to delete: "))
                if manager.delete_task(task_id):
                    print(f"Task #{task_id} deleted successfully.")
                else:
                    print(f"Task ID {task_id} not found.")
            except ValueError:
                print("Error: Task ID must be a number.")

        elif choice == "6":
            print("Exiting Task Manager.")
            break
        else:
            print("Invalid option. Please choose between 1 and 6.")


if __name__ == "__main__":
    main()