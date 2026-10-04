"""Persistence for the task list in a local JSON file.

Layer between model and CLI: the rest of the program only works with
`Task` objects, never with the file directly.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import Priority, Task

DEFAULT_FILE = Path("tasks.json")


class TaskRepository:
    """Manages the task list in a JSON file."""

    def __init__(self, file: Path | None = None) -> None:
        self.file = file if file is not None else DEFAULT_FILE
        self.tasks: list[Task] = self._load()

    def _load(self) -> list[Task]:
        """Reads the JSON file; if it is missing, start with an empty list."""
        if not self.file.exists():
            return []
        with self.file.open(encoding="utf-8") as f:
            data: list[dict[str, Any]] = json.load(f)
        return [Task.from_dict(entry) for entry in data]

    def save(self) -> None:
        """Writes the complete task list to the JSON file."""
        with self.file.open("w", encoding="utf-8") as f:
            json.dump(
                [t.to_dict() for t in self.tasks],
                f,
                ensure_ascii=False,
                indent=2,
            )

    def add(
        self, title: str, description: str = "", priority: Priority = Priority.C
    ) -> Task:
        """Creates a new task and saves immediately."""
        task = Task.new_task(title, description, priority)
        self.tasks.append(task)
        self.save()
        return task

    def find(self, task_id: str) -> Task | None:
        """Searches for a task by its id."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def complete(self, task_id: str) -> Task | None:
        """Marks a task as done; None if the id is unknown."""
        task = self.find(task_id)
        if task is None:
            return None
        task.done = True
        self.save()
        return task

    def delete(self, task_id: str) -> bool:
        """Removes a task; True if it was deleted."""
        task = self.find(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        self.save()
        return True

    def list_tasks(
        self,
        only_open: bool = False,
        priority: Priority | None = None,
    ) -> list[Task]:
        """Returns the tasks, optionally filtered by status/priority.

        Sorting: first by priority (A before B before ...), then by title.
        """
        result = self.tasks
        if only_open:
            result = [t for t in result if not t.done]
        if priority is not None:
            result = [t for t in result if t.priority is priority]
        return sorted(
            result,
            key=lambda t: (t.priority.value, t.title.lower()),
        )
