"""Pytest tests for Lab 4: Short-Term Memory & Streaming.

Follows the TEST.md framework (core logic, output structure, docs-vs-behavior).
The cells are exec'd from the notebook's own sources, so these tests exercise
the actual lab code — not a copy. No API calls are made.

Run: python3 -m pytest test_lab4.py -v
"""

import ast
import json
import os
from pathlib import Path

import pytest
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

NB_PATH = Path(__file__).with_name("lab-memory-streaming.ipynb")


def code_cells():
    with open(NB_PATH) as f:
        notebook = json.load(f)
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


@pytest.fixture(scope="module")
def lab():
    """Exec the notebook's *definition* cells (Steps 2-5 and the trimmer
    header) against real langchain-core classes. Invocation cells (which
    would call the API) are excluded."""
    os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
    namespace = {
        "os": os,
        "ChatOpenAI": ChatOpenAI,
        "InMemoryChatMessageHistory": InMemoryChatMessageHistory,
        "ChatPromptTemplate": ChatPromptTemplate,
        "MessagesPlaceholder": MessagesPlaceholder,
        "RunnableWithMessageHistory": RunnableWithMessageHistory,
        "HumanMessage": HumanMessage,
        "AIMessage": AIMessage,
    }
    cells = code_cells()
    definition_sources = cells[1:5] + [cells[9].split("bounded_chat.invoke(")[0]]
    for source in definition_sources:
        tree = ast.parse(source)
        exec(compile(tree, "<cell>", "exec"), namespace)
    return namespace


class TestPromptAndMemoryStore:
    """Steps 4-5: the prompt has a history slot; the store is per-session."""

    def test_prompt_has_history_placeholder(self, lab):
        placeholders = [
            m for m in lab["prompt"].messages if isinstance(m, MessagesPlaceholder)
        ]
        assert placeholders, "prompt must contain a MessagesPlaceholder"
        assert placeholders[0].variable_name == "history"

    def test_prompt_has_system_and_human(self, lab):
        kinds = {type(m) for m in lab["prompt"].messages}
        assert SystemMessagePromptTemplate in kinds
        assert HumanMessagePromptTemplate in kinds

    def test_store_returns_same_history_per_session(self, lab):
        first = lab["get_session_history"]("ada")
        second = lab["get_session_history"]("ada")
        other = lab["get_session_history"]("bob")
        assert first is second
        assert first is not other
        assert isinstance(first, InMemoryChatMessageHistory)


class TestWrappedChain:
    """Step 5: the chain is wrapped so history is injected and persisted."""

    def test_chat_is_wrapped_with_message_history(self, lab):
        assert isinstance(lab["chat"], RunnableWithMessageHistory)

    def test_message_keys_match_prompt(self, lab):
        assert lab["chat"].input_messages_key == "input"
        assert lab["chat"].history_messages_key == "history"


class TestStreaming:
    """Steps 8-9: the notebook streams both bare and through the wrapper."""

    def test_streams_bare_model(self, lab):
        sources = code_cells()
        assert any("model.stream(" in src for src in sources)

    def test_streams_through_wrapped_chat(self, lab):
        sources = code_cells()
        assert any("chat.stream(" in src for src in sources)


class TestOptionalExerciseTrimmer:
    """Section 11: trim_messages keeps only the most recent messages."""

    def test_trimmer_drops_oldest_messages(self, lab):
        history = [
            HumanMessage("My favorite city is Oslo. Remember it."),
            AIMessage(
                "Got it! I have noted that your favorite city is Oslo "
                "and I will remember it."
            ),
            HumanMessage("I also love winter hiking."),
            AIMessage("That sounds lovely. Winter hiking through the snow "
                      "is really beautiful."),
        ]
        trimmed = lab["trimmer"].invoke(history)
        assert len(trimmed) < len(history)
        combined = " ".join(m.content for m in trimmed)
        assert "Oslo" not in combined, "the oldest turn must fall out of the window"
        assert "winter hiking" in combined, "the recent turn must be kept"


class TestNotebookArtifact:
    """CQ-10: first code cell is a single pinned `!pip install` line."""

    def test_first_code_cell_is_single_pinned_pip_install(self):
        lines = code_cells()[0].splitlines()
        pip_lines = [ln for ln in lines if ln.startswith("!pip install")]
        assert len(pip_lines) == 1
        for line in lines:
            if line.startswith("!pip install"):
                break
            assert line.strip() == "" or line.startswith("#")
        packages = [tok.strip('"') for tok in pip_lines[0].split()[2:]]
        assert packages, "install line lists at least one module"
        assert all("==" in pkg for pkg in packages), "every module must be pinned"
