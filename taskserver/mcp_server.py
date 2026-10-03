"""MCP server for the task management.

Exposes the TaskRepository operations as MCP tools so an AI client can
create, query and manage tasks. All names and descriptions are English
because they are consumed by the AI, not by a human user.

Note: the class used to be called `FastMCP`; since mcp SDK 2.0 it is
named `MCPServer` (from mcp.server.mcpserver import MCPServer).
"""

from __future__ import annotations

from pathlib import Path

from mcp.server.mcpserver import MCPServer

from .model import Priority
from .repository import TaskRepository

mcp = MCPServer("taskserver")

_repository = TaskRepository(Path("tasks.json"))


def _task_to_text(task) -> str:
    """Formats a single task for compact output."""
    status = "done" if task.done else "open"
    lines = [f"[{task.id}] ({task.priority.value}) {task.title} - {status}"]
    if task.description:
        lines.append(f"    {task.description}")
    return "\n".join(lines)


@mcp.tool()
def add_task(
    title: str,
    description: str = "",
    priority: str = "C",
) -> str:
    """Create a new task.

    Args:
        title: Short title of the task.
        description: Optional longer description.
        priority: Priority of the task (A, B, C or D; default C).

    Returns:
        Confirmation message with the id of the new task.
    """
    task = _repository.add(title, description, Priority.from_value(priority))
    return f"Task '{task.title}' created with id {task.id}."


@mcp.tool()
def list_tasks(
    only_open: bool = False,
    priority: str = "",
) -> str:
    """List all known tasks, sorted by priority (A first).

    Args:
        only_open: If true, only tasks that are not done yet.
        priority: If set (A, B, C or D), only tasks with this priority.

    Returns:
        All matching tasks, one per line, or a message if none exist.
    """
    tasks = _repository.list_tasks(
        only_open=only_open,
        priority=Priority.from_value(priority) if priority else None,
    )
    if not tasks:
        return "No tasks found."
    return "\n".join(_task_to_text(t) for t in tasks)


@mcp.tool()
def get_task(task_id: str) -> str:
    """Show one task in detail.

    Args:
        task_id: The id of the task.

    Returns:
        All attributes of the task, or a message if the id is unknown.
    """
    task = _repository.find(task_id)
    if task is None:
        return f"No task with id '{task_id}' found."
    return "\n".join(
        [
            f"id:          {task.id}",
            f"title:       {task.title}",
            f"description: {task.description or '-'}",
            f"priority:    {task.priority.value}",
            f"status:      {'done' if task.done else 'open'}",
            f"created at:  {task.created_at}",
        ]
    )


@mcp.tool()
def complete_task(task_id: str) -> str:
    """Mark a task as done.

    Args:
        task_id: The id of the task.

    Returns:
        Confirmation message, or a message if the id is unknown.
    """
    task = _repository.complete(task_id)
    if task is None:
        return f"No task with id '{task_id}' found."
    return f"Task '{task.title}' marked as done."


@mcp.tool()
def delete_task(task_id: str) -> str:
    """Delete a task permanently.

    Args:
        task_id: The id of the task.

    Returns:
        Confirmation message, or a message if the id is unknown.
    """
    if _repository.delete(task_id):
        return f"Task {task_id} deleted."
    return f"No task with id '{task_id}' found."


if __name__ == "__main__":
    mcp.run()
