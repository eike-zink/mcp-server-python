"""Persistenz für die Aufgabenliste in einer lokalen JSON-Datei.

Schicht zwischen Modell und CLI: Das restliche Programm arbeitet nur mit
`Aufgabe`-Objekten, nie direkt mit der Datei.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import Aufgabe, Prioritaet

STANDARD_DATEI = Path("aufgaben.json")


class AufgabenRepository:
    """Verwaltet die Aufgabenliste in einer JSON-Datei."""

    def __init__(self, datei: Path | None = None) -> None:
        self.datei = datei if datei is not None else STANDARD_DATEI
        self.aufgaben: list[Aufgabe] = self._laden()

    def _laden(self) -> list[Aufgabe]:
        """Liest die JSON-Datei; fehlt sie, startet man mit einer leeren Liste."""
        if not self.datei.exists():
            return []
        with self.datei.open(encoding="utf-8") as f:
            daten: list[dict[str, Any]] = json.load(f)
        return [Aufgabe.from_dict(eintrag) for eintrag in daten]

    def speichern(self) -> None:
        """Schreibt die vollständige Aufgabenliste in die JSON-Datei."""
        with self.datei.open("w", encoding="utf-8") as f:
            json.dump(
                [a.to_dict() for a in self.aufgaben],
                f,
                ensure_ascii=False,
                indent=2,
            )

    def hinzufuegen(
        self, titel: str, beschreibung: str = "", prioritaet: Prioritaet = Prioritaet.C
    ) -> Aufgabe:
        """Legt eine neue Aufgabe an und speichert sofort."""
        aufgabe = Aufgabe.neue_aufgabe(titel, beschreibung, prioritaet)
        self.aufgaben.append(aufgabe)
        self.speichern()
        return aufgabe

    def finden(self, aufgaben_id: str) -> Aufgabe | None:
        """Sucht eine Aufgabe anhand ihrer ID."""
        for aufgabe in self.aufgaben:
            if aufgabe.id == aufgaben_id:
                return aufgabe
        return None

    def abhaken(self, aufgaben_id: str) -> Aufgabe | None:
        """Markiert eine Aufgabe als erledigt; None, wenn die ID unbekannt ist."""
        aufgabe = self.finden(aufgaben_id)
        if aufgabe is None:
            return None
        aufgabe.erledigt = True
        self.speichern()
        return aufgabe

    def loeschen(self, aufgaben_id: str) -> bool:
        """Entfernt eine Aufgabe; True, wenn sie gelöscht wurde."""
        aufgabe = self.finden(aufgaben_id)
        if aufgabe is None:
            return False
        self.aufgaben.remove(aufgabe)
        self.speichern()
        return True

    def liste(
        self,
        nur_offen: bool = False,
        prioritaet: Prioritaet | None = None,
    ) -> list[Aufgabe]:
        """Liefert die Aufgaben, optional gefiltert nach Status/Priorität.

        Sortierung: erst nach Priorität (A vor B vor ...), dann nach Titel.
        """
        ergebnis = self.aufgaben
        if nur_offen:
            ergebnis = [a for a in ergebnis if not a.erledigt]
        if prioritaet is not None:
            ergebnis = [a for a in ergebnis if a.prioritaet is prioritaet]
        return sorted(
            ergebnis,
            key=lambda a: (a.prioritaet.value, a.titel.lower()),
        )
