"""Kommandozeilen-Oberfläche der Aufgabenverwaltung (argparse).

Die CLI übersetzt Befehle in Aufrufe auf dem AufgabenRepository und
formatiert die Ausgaben für den Menschen.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .model import Prioritaet
from .repository import AufgabenRepository


def _repo(args: argparse.Namespace) -> AufgabenRepository:
    """Erzeugt das Repository mit dem optional per Option gesetzten Dateipfad."""
    return AufgabenRepository(Path(args.datei) if args.datei else None)


def _tabelle_drucken(aufgaben: list) -> None:
    """Gibt die Aufgaben als ausgerichtete Tabelle aus."""
    if not aufgaben:
        print("Keine Aufgaben gefunden.")
        return
    kopf = f"{'ID':<8} {'P':<1} {'Status':<9} Titel"
    print(kopf)
    print("-" * len(kopf))
    for a in aufgaben:
        status = "[x]" if a.erledigt else "[ ]"
        print(f"{a.id:<8} {a.prioritaet.value:<1} {status:<9} {a.titel}")
        if a.beschreibung:
            print(f"{'':<21} {a.beschreibung}")


def befehl_hinzufuegen(args: argparse.Namespace) -> None:
    repo = _repo(args)
    prioritaet = Prioritaet.aus_wert(args.prioritaet)
    aufgabe = repo.hinzufuegen(args.titel, args.beschreibung, prioritaet)
    print(f"Aufgabe '{aufgabe.titel}' angelegt (ID: {aufgabe.id}, "
          f"Priorität: {prioritaet.value}).")


def befehl_liste(args: argparse.Namespace) -> None:
    repo = _repo(args)
    prioritaet = Prioritaet.aus_wert(args.prioritaet) if args.prioritaet else None
    aufgaben = repo.liste(nur_offen=args.offen, prioritaet=prioritaet)
    _tabelle_drucken(aufgaben)


def befehl_zeigen(args: argparse.Namespace) -> None:
    repo = _repo(args)
    aufgabe = repo.finden(args.id)
    if aufgabe is None:
        print(f"Keine Aufgabe mit der ID '{args.id}' gefunden.")
        return
    print(f"ID:           {aufgabe.id}")
    print(f"Titel:        {aufgabe.titel}")
    print(f"Beschreibung: {aufgabe.beschreibung or '-'}")
    print(f"Priorität:    {aufgabe.prioritaet.value}")
    print(f"Status:       {'erledigt' if aufgabe.erledigt else 'offen'}")
    print(f"Erstellt am:  {aufgabe.erstellt_am}")


def befehl_abhaken(args: argparse.Namespace) -> None:
    repo = _repo(args)
    aufgabe = repo.abhaken(args.id)
    if aufgabe is None:
        print(f"Keine Aufgabe mit der ID '{args.id}' gefunden.")
    else:
        print(f"Aufgabe '{aufgabe.titel}' als erledigt markiert.")


def befehl_loeschen(args: argparse.Namespace) -> None:
    repo = _repo(args)
    if repo.loeschen(args.id):
        print(f"Aufgabe {args.id} gelöscht.")
    else:
        print(f"Keine Aufgabe mit der ID '{args.id}' gefunden.")


def parser_bauen() -> argparse.ArgumentParser:
    """Baut den argparse-Parser mit allen Unterbefehlen auf."""
    parser = argparse.ArgumentParser(
        prog="aufgabenverwaltung",
        description="Einfache Aufgabenverwaltung mit JSON-Speicherung.",
    )
    parser.add_argument(
        "--datei",
        help="Pfad zur JSON-Datei (Standard: aufgaben.json im aktuellen Verzeichnis).",
    )
    sub = parser.add_subparsers(dest="befehl", required=True)

    p_add = sub.add_parser("add", help="Neue Aufgabe anlegen")
    p_add.add_argument("titel", help="Kurzer Titel der Aufgabe")
    p_add.add_argument("-b", "--beschreibung", default="", help="Optionale Beschreibung")
    p_add.add_argument("-p", "--prioritaet", choices=["A", "B", "C", "D"], default="C")
    p_add.set_defaults(funktion=befehl_hinzufuegen)

    p_list = sub.add_parser("list", help="Aufgaben anzeigen")
    p_list.add_argument("-o", "--offen", action="store_true", help="Nur offene Aufgaben")
    p_list.add_argument("-p", "--prioritaet", choices=["A", "B", "C", "D"])
    p_list.set_defaults(funktion=befehl_liste)

    p_show = sub.add_parser("show", help="Details einer Aufgabe anzeigen")
    p_show.add_argument("id", help="ID der Aufgabe")
    p_show.set_defaults(funktion=befehl_zeigen)

    p_done = sub.add_parser("done", help="Aufgabe als erledigt markieren")
    p_done.add_argument("id", help="ID der Aufgabe")
    p_done.set_defaults(funktion=befehl_abhaken)

    p_del = sub.add_parser("delete", help="Aufgabe löschen")
    p_del.add_argument("id", help="ID der Aufgabe")
    p_del.set_defaults(funktion=befehl_loeschen)

    return parser


def main() -> None:
    args = parser_bauen().parse_args()
    args.funktion(args)


if __name__ == "__main__":
    main()
