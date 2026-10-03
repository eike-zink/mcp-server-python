"""Command line interface for the task management (argparse).

The CLI translates commands into calls on the TaskRepository and
formats the output for humans. All user-facing strings are German.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .model import Priority
from .repository import TaskRepository


def _repo(args: argparse.Namespace) -> TaskRepository:
    """Creates the repository using the optional file path option."""
    return TaskRepository(Path(args.datei) if args.datei else None)


def _print_table(tasks: list) -> None:
    """Prints the tasks as an aligned table."""
    if not tasks:
        print("Keine Aufgaben gefunden.")
        return
    header = f"{'ID':<8} {'P':<1} {'Status':<9} Titel"
    print(header)
    print("-" * len(header))
    for t in tasks:
        status = "[x]" if t.done else "[ ]"
        print(f"{t.id:<8} {t.priority.value:<1} {status:<9} {t.title}")
        if t.description:
            print(f"{'':<21} {t.description}")


def cmd_add(args: argparse.Namespace) -> None:
    repo = _repo(args)
    priority = Priority.from_value(args.prioritaet)
    task = repo.add(args.title, args.beschreibung, priority)
    print(f"Aufgabe '{task.title}' angelegt (ID: {task.id}, "
          f"Priorität: {priority.value}).")


def cmd_list(args: argparse.Namespace) -> None:
    repo = _repo(args)
    priority = Priority.from_value(args.prioritaet) if args.prioritaet else None
    tasks = repo.list_tasks(only_open=args.offen, priority=priority)
    _print_table(tasks)


def cmd_show(args: argparse.Namespace) -> None:
    repo = _repo(args)
    task = repo.find(args.id)
    if task is None:
        print(f"Keine Aufgabe mit der ID '{args.id}' gefunden.")
        return
    print(f"ID:           {task.id}")
    print(f"Titel:        {task.title}")
    print(f"Beschreibung: {task.description or '-'}")
    print(f"Priorität:    {task.priority.value}")
    print(f"Status:       {'erledigt' if task.done else 'offen'}")
    print(f"Erstellt am:  {task.created_at}")


def cmd_done(args: argparse.Namespace) -> None:
    repo = _repo(args)
    task = repo.complete(args.id)
    if task is None:
        print(f"Keine Aufgabe mit der ID '{args.id}' gefunden.")
    else:
        print(f"Aufgabe '{task.title}' als erledigt markiert.")


def cmd_delete(args: argparse.Namespace) -> None:
    repo = _repo(args)
    if repo.delete(args.id):
        print(f"Aufgabe {args.id} gelöscht.")
    else:
        print(f"Keine Aufgabe mit der ID '{args.id}' gefunden.")


def build_parser() -> argparse.ArgumentParser:
    """Builds the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="aufgabenverwaltung",
        description="Einfache Aufgabenverwaltung mit JSON-Speicherung.",
    )
    parser.add_argument(
        "--datei",
        help="Pfad zur JSON-Datei (Standard: tasks.json im aktuellen Verzeichnis).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Neue Aufgabe anlegen")
    p_add.add_argument("title", help="Kurzer Titel der Aufgabe")
    p_add.add_argument("-b", "--beschreibung", default="", help="Optionale Beschreibung")
    p_add.add_argument("-p", "--prioritaet", choices=["A", "B", "C", "D"], default="C")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="Aufgaben anzeigen")
    p_list.add_argument("-o", "--offen", action="store_true", help="Nur offene Aufgaben")
    p_list.add_argument("-p", "--prioritaet", choices=["A", "B", "C", "D"])
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Details einer Aufgabe anzeigen")
    p_show.add_argument("id", help="ID der Aufgabe")
    p_show.set_defaults(func=cmd_show)

    p_done = sub.add_parser("done", help="Aufgabe als erledigt markieren")
    p_done.add_argument("id", help="ID der Aufgabe")
    p_done.set_defaults(func=cmd_done)

    p_del = sub.add_parser("delete", help="Aufgabe löschen")
    p_del.add_argument("id", help="ID der Aufgabe")
    p_del.set_defaults(func=cmd_delete)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
