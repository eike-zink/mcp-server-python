"""Interactive MCP client for the taskserver (for learning and testing).

Connects to the MCP server via stdio and lets a human exercise the
protocol by hand: list tools, call tools, read resources, get prompts.
This shows the client side of MCP before connecting a real AI.
"""

from __future__ import annotations

import asyncio
import shlex

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HILFE = """\
Verfügbare Befehle:
  hilfe                     Diese Übersicht anzeigen
  tools                     Verfügbare Tools des Servers auflisten
  add <titel> [-b <text>] [-p <A-D>]   Aufgabe über das Tool add_task anlegen
  liste [-o] [-p <A-D>]     Aufgaben über das Tool list_tasks anzeigen
  zeige <id>                Details über das Tool get_task abrufen
  abhaken <id>              Aufgabe über das Tool complete_task erledigen
  loeschen <id>             Aufgabe über das Tool delete_task löschen
  ressourcen                Ressourcen des Servers auflisten
  lies <uri>                Ressource lesen (z. B. taskserver://priorities)
  prompts                   Prompts des Servers auflisten
  prompt <name>             Prompt abrufen (z. B. plan_my_day)
  ende                      Client beenden
"""


def _parse_option(tokens: list[str], flag: str) -> str | None:
    """Extracts the value after a flag like -b or -p, if present."""
    if flag in tokens:
        idx = tokens.index(flag)
        if idx + 1 < len(tokens):
            return tokens[idx + 1]
    return None


def _parse_title(tokens: list[str]) -> str:
    """Collects the positional words (title) and skips flag/value pairs."""
    titel_teile: list[str] = []
    skip_next = False
    for token in tokens:
        if skip_next:
            skip_next = False
            continue
        if token in ("-b", "-p"):
            skip_next = True
            continue
        titel_teile.append(token)
    return " ".join(titel_teile)


async def _handle_command(session: ClientSession, line: str) -> bool:
    """Executes one user command; returns False when the client should stop."""
    tokens = shlex.split(line)
    if not tokens:
        return True
    befehl, arg = tokens[0], tokens[1:]

    if befehl in ("ende", "exit", "quit"):
        return False

    if befehl == "hilfe":
        print(HILFE)

    elif befehl == "tools":
        antwort = await session.list_tools()
        for t in antwort.tools:
            print(f"- {t.name}: {t.description.splitlines()[0]}")

    elif befehl == "add":
        beschreibung = _parse_option(arg, "-b")
        prioritaet = _parse_option(arg, "-p")
        titel = _parse_title(arg)
        ergebnis = await session.call_tool(
            "add_task",
            {"title": titel, "description": beschreibung or "", "priority": prioritaet or "C"},
        )
        print(ergebnis.content[0].text)

    elif befehl == "liste":
        nur_offen = "-o" in arg
        prioritaet = _parse_option(arg, "-p")
        ergebnis = await session.call_tool(
            "list_tasks",
            {"only_open": nur_offen, "priority": prioritaet or ""},
        )
        print(ergebnis.content[0].text)

    elif befehl == "zeige":
        ergebnis = await session.call_tool("get_task", {"task_id": arg[0]})
        print(ergebnis.content[0].text)

    elif befehl == "abhaken":
        ergebnis = await session.call_tool("complete_task", {"task_id": arg[0]})
        print(ergebnis.content[0].text)

    elif befehl == "loeschen":
        ergebnis = await session.call_tool("delete_task", {"task_id": arg[0]})
        print(ergebnis.content[0].text)

    elif befehl == "ressourcen":
        antwort = await session.list_resources()
        for r in antwort.resources:
            print(f"- {r.uri}: {r.description}")

    elif befehl == "lies":
        antwort = await session.read_resource(arg[0])
        print(antwort.contents[0].text)

    elif befehl == "prompts":
        antwort = await session.list_prompts()
        for p in antwort.prompts:
            print(f"- {p.name}: {p.description}")

    elif befehl == "prompt":
        antwort = await session.get_prompt(arg[0])
        for nachricht in antwort.messages:
            print(nachricht.content.text)

    else:
        print(f"Unbekannter Befehl: {befehl} ( 'hilfe' zeigt alle Befehle)")

    return True


async def main() -> None:
    params = StdioServerParameters(
        command="python",
        args=["-m", "taskserver.mcp_server"],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Verbunden mit MCP-Server 'taskserver'.")
            print("Tippe 'hilfe' für alle Befehle, 'ende' zum Beenden.")
            while True:
                try:
                    line = input("> ")
                except (EOFError, KeyboardInterrupt):
                    break
                if not await _handle_command(session, line):
                    break
    print("Verbindung getrennt. Bis bald!")


if __name__ == "__main__":
    asyncio.run(main())
