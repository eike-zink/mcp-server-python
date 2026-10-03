# MCP Server in Python

# Aufgabenverwaltung (Schritt 1: CLI)

Einfache Aufgabenverwaltung in Python als Lernprojekt für MCP-Server.
Eine Aufgabe besteht aus: ID, Titel, Beschreibung, Erledigt-Status und
Priorität (A–D). Die Liste wird lokal in einer JSON-Datei gespeichert.

## Architektur

```
taskserver/
├── __init__.py
├── model.py      # Data model: Task, Priority (dataclass, Enum)
├── repository.py # Persistence: load/save JSON, CRUD logic
└── cli.py        # User interface: argparse with subcommands
```

Die Trennung ist bewusst so gewählt: In Schritt 2 wird mit FastMCP ein
weiterer "Client" (die KI) angebaut. Client und CLI greifen beide nur auf
das `TaskRepository` zu – Modell und Persistenz bleiben unverändert.

Bezeichnungen im Code sind Englisch (PEP 8), Ausgaben und Hilfetexte sind
Deutsch.

## Verwendung

```bash
# Aufgabe anlegen (Priorität A–D, Standard C)
python -m taskserver.cli add "MCP-Server aufbauen" -b "FastMCP-Beispiel" -p A

# Alle Aufgaben anzeigen, sortiert nach Priorität
python -m taskserver.cli list

# Nur offene Aufgaben bzw. nur Priorität A
python -m taskserver.cli list -o
python -m taskserver.cli list -p A

# Details anzeigen, abhaken, löschen
python -m taskserver.cli show <id>
python -m taskserver.cli done <id>
python -m taskserver.cli delete <id>

# Eigener Dateipfad statt tasks.json
python -m taskserver.cli --datei test/aufgaben.json list
```

## Nächster Schritt

Schritt 2: Aufbau des MCP-Servers mit FastMCP (`mcp`-Paket). Die Funktionen
des Repositories werden dann als MCP-Tools (`add_task`, `list_tasks`,
`complete_task`, ...) angeboten, damit die KI die Aufgabenverwaltung direkt
nutzen kann.
