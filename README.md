# MCP Server in Python

# Aufgabenverwaltung (Schritt 1: CLI)

Einfache Aufgabenverwaltung in Python als Lernprojekt für MCP-Server.
Eine Aufgabe besteht aus: ID, Titel, Beschreibung, Erledigt-Status und
Priorität (A–D). Die Liste wird lokal in einer JSON-Datei gespeichert.

## Architektur

```
aufgabenserver/
├── __init__.py
├── model.py     # Datenmodell: Aufgabe, Prioritaet (dataclass, Enum)
├── repository.py # Persistenz: JSON laden/speichern, CRUD-Logik
└── cli.py       # Benutzungsoberfläche: argparse mit Unterbefehlen
```

Die Trennung ist bewusst so gewählt: In Schritt 2 wird mit FastMCP ein
weiterer "Klient" (die KI) angebaut. Klient und CLI greifen beide nur auf
das `AufgabenRepository` zu – das Modell und die Persistenz bleiben
unverändert.

## Verwendung

```bash
# Aufgabe anlegen (Priorität A–D, Standard C)
python -m aufgabenserver.cli add "MCP-Server aufbauen" -b "FastMCP-Beispiel" -p A

# Alle Aufgaben anzeigen, sortiert nach Priorität
python -m aufgabenserver.cli list

# Nur offene Aufgaben bzw. nur Priorität A
python -m aufgabenserver.cli list -o
python -m aufgabenserver.cli list -p A

# Details anzeigen, abhaken, löschen
python -m aufgabenserver.cli show <id>
python -m aufgabenserver.cli done <id>
python -m aufgabenserver.cli delete <id>

# Eigener Dateipfad statt aufgaben.json
python -m aufgabenserver.cli --datei test/aufgaben.json list
```

## Nächster Schritt

Schritt 2: Aufbau des MCP-Servers mit FastMCP (`mcp`-Paket). Die Funktionen
des Repositories werden dann als MCP-Tools (`aufgabe_anlegen`,
`aufgaben_auflisten`, `aufgabe_abhaken`, ...) angeboten, damit die KI die
Aufgabenverwaltung direkt nutzen kann.
