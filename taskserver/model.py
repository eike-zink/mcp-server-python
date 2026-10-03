"""Data model for tasks.

Kept intentionally simple: id, title, description, done flag,
priority (A-D).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Priority(str, Enum):
    """Priority of a task: A (highest) to D (lowest)."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"

    @classmethod
    def from_value(cls, value: str | None) -> "Priority":
        """Returns the priority for a string, defaulting to C."""
        if value is None:
            return cls.C
        return cls(value.strip().upper())


@dataclass
class Task:
    """Represents a single task."""

    id: str
    title: str
    description: str = ""
    done: bool = False
    priority: Priority = Priority.C
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @staticmethod
    def new_task(
        title: str, description: str = "", priority: Priority = Priority.C
    ) -> "Task":
        """Creates a new task with an automatically assigned id."""
        return Task(
            id=uuid.uuid4().hex[:8],
            title=title,
            description=description,
            priority=priority,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serializes the task for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority.value,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Loads a task from a dictionary (JSON)."""
        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            done=bool(data.get("done", False)),
            priority=Priority.from_value(data.get("priority")),
            created_at=str(data.get("created_at", "")),
        )
