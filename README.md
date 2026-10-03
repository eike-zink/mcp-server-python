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
├── cli.py        # User interface: argparse with subcommands
└── mcp_server.py # MCP interface for AI clients (MCPServer/FastMCP)
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

## Schritt 2: MCP-Server

Der MCP-Server (`taskserver/mcp_server.py`) stellt dieselben
Repository-Funktionen als MCP-Tools bereit – vollständíg englisch,
da die Tool-Beschreibungen von der KI gelesen werden:

| Tool | Beschreibung |
|------|--------------|
| `add_task` | Neue Aufgabe anlegen (Titel, Beschreibung, Priorität A–D) |
| `list_tasks` | Aufgaben anzeigen, filterbar nach Status und Priorität |
| `get_task` | Details einer Aufgabe anzeigen |
| `complete_task` | Aufgabe als erledigt markieren |
| `delete_task` | Aufgabe löschen |

Server starten (Stdio-Transport, Kommunikation über stdin/stdout):

```bash
python -m taskserver.mcp_server
```

Zum Testen ohne eigene KI eignet sich der MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python -m taskserver.mcp_server
```

Installation des SDK: `pip install "mcp>=2.0"` (siehe `requirements.txt`).
Hinweis: In SDK 2.x heißt die Serverklasse `MCPServer`
(`from mcp.server.mcpserver import MCPServer`); in älteren Versionen
hieß sie `FastMCP`.
