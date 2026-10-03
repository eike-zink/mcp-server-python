"""Datenmodell für Aufgaben.

Bewusst einfach gehalten: ID, Titel, Beschreibung, Erledigt-Status,
Priorität (A–D).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Prioritaet(str, Enum):
    """Priorität einer Aufgabe: A (höchste) bis D (niedrigste)."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"

    @classmethod
    def aus_wert(cls, wert: str | None) -> "Prioritaet":
        """Liefert die Priorität für einen String, Standard ist C."""
        if wert is None:
            return cls.C
        return cls(wert.strip().upper())


@dataclass
class Aufgabe:
    """Repräsentiert eine einzelne Aufgabe."""

    id: str
    titel: str
    beschreibung: str = ""
    erledigt: bool = False
    prioritaet: Prioritaet = Prioritaet.C
    erstellt_am: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @staticmethod
    def neue_aufgabe(
        titel: str, beschreibung: str = "", prioritaet: Prioritaet = Prioritaet.C
    ) -> "Aufgabe":
        """Erzeugt eine neue Aufgabe mit automatisch vergebener ID."""
        return Aufgabe(
            id=uuid.uuid4().hex[:8],
            titel=titel,
            beschreibung=beschreibung,
            prioritaet=prioritaet,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialisiert die Aufgabe für die JSON-Speicherung."""
        return {
            "id": self.id,
            "titel": self.titel,
            "beschreibung": self.beschreibung,
            "erledigt": self.erledigt,
            "prioritaet": self.prioritaet.value,
            "erstellt_am": self.erstellt_am,
        }

    @classmethod
    def from_dict(cls, daten: dict[str, Any]) -> "Aufgabe":
        """Lädt eine Aufgabe aus einem Dictionary (JSON)."""
        return cls(
            id=str(daten["id"]),
            titel=str(daten["titel"]),
            beschreibung=str(daten.get("beschreibung", "")),
            erledigt=bool(daten.get("erledigt", False)),
            prioritaet=Prioritaet.aus_wert(daten.get("prioritaet")),
            erstellt_am=str(daten.get("erstellt_am", "")),
        )
