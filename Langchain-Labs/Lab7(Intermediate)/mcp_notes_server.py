"""A local MCP server: your personal notes store, backed by a JSON file.

This file is an MCP *server*. It runs as its own process and talks to MCP
clients over stdio (standard input/output). It knows nothing about LangChain,
agents, or models — it only exposes a small set of tools over the MCP protocol.

Run directly to test it:  python mcp_notes_server.py
"""

import json
import logging
import warnings
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# The MCP SDK logs every request it processes at INFO. Quiet the server's own
# log stream and a noisy pydantic warning so the notebook output stays clean.
logging.getLogger("mcp").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", module="pydantic_settings")

NOTES_FILE = Path(__file__).with_name("notes.json")

mcp = FastMCP("notes-server")


def load_notes() -> dict:
    if NOTES_FILE.exists():
        return json.loads(NOTES_FILE.read_text())
    return {}


def save_notes(notes: dict) -> None:
    NOTES_FILE.write_text(json.dumps(notes, indent=2))


@mcp.tool()
def add_note(title: str, content: str) -> str:
    """Add a note and return its id. The id is a sequential number."""
    notes = load_notes()
    note_id = str(len(notes) + 1)
    notes[note_id] = {"title": title, "content": content}
    save_notes(notes)
    return f"Added note {note_id}: {title}"


@mcp.tool()
def list_notes() -> str:
    """List all notes as one line per note (id + title)."""
    notes = load_notes()
    if not notes:
        return "No notes yet."
    return "\n".join(f"[{note_id}] {note['title']}" for note_id, note in notes.items())


@mcp.tool()
def get_note(note_id: str) -> str:
    """Return one note by its id, with title and content."""
    notes = load_notes()
    note = notes.get(note_id)
    if note is None:
        return f"No note with id {note_id}."
    return f"[{note_id}] {note['title']}\n{note['content']}"


@mcp.tool()
def delete_note(note_id: str) -> str:
    """Delete a note by its id. Returns a confirmation."""
    notes = load_notes()
    if note_id not in notes:
        return f"No note with id {note_id}."
    del notes[note_id]
    save_notes(notes)
    return f"Deleted note {note_id}."


if __name__ == "__main__":
    mcp.run()
