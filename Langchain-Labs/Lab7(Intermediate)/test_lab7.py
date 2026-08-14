"""Pytest tests for Lab 7: Local MCP — Connect to a Locally-Run MCP Server.

Follows the TEST.md framework. The notebook's *definition* statements are exec'd
from the notebook's own sources so the tests exercise the actual lab code — not a
copy. Statements that call `.invoke(...)`, top-level `await`, or reference the
MCP client session (which would spawn subprocesses) are skipped; the definitions
(model, connection config, agent) are tested directly. No API calls and no server
subprocesses are spawned.

Run: python3 -m pytest test_lab7.py -v
"""

import ast
import json
import sys
from pathlib import Path

import pytest
from langchain_mcp_adapters.client import MultiServerMCPClient

NB_PATH = Path(__file__).with_name("lab-local-mcp.ipynb")
SERVER_PATH = Path(__file__).with_name("mcp_notes_server.py")
MD_PATH = Path(__file__).with_name("lab-local-mcp.md")


def code_cells():
    with open(NB_PATH) as f:
        notebook = json.load(f)
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def _has_invoke(node) -> bool:
    return any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "invoke"
        for n in ast.walk(node)
    )


def _has_await(node) -> bool:
    return any(isinstance(n, ast.Await) for n in ast.walk(node))


@pytest.fixture(scope="module")
def lab():
    """Exec the notebook's definition statements against real langchain classes.
    Statements that would spawn a subprocess, hit the API, or await a session are
    skipped, leaving `model`, `client`, and `agent` definitions in scope."""
    import os

    os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
    namespace = {"os": os, "load_dotenv": lambda *a, **k: None}
    for source in code_cells():
        if any(ln.lstrip().startswith("!") for ln in source.splitlines()):
            continue  # shell magics (e.g. !pip install) are not valid Python
        tree = ast.parse(source)
        for node in tree.body:
            if _has_invoke(node) or _has_await(node):
                continue
            try:
                exec(compile(ast.Module([node], []), "<cell>", "exec"), namespace)
            except NameError:
                continue
    yield namespace


class TestNotebookArtifact:
    def test_first_code_cell_is_single_pinned_pip_install(self):
        lines = code_cells()[0].splitlines()
        pip_lines = [ln for ln in lines if ln.startswith("!pip install")]
        assert len(pip_lines) == 1
        for line in lines:
            if line.startswith("!pip install"):
                break
            assert line.strip() == "" or line.startswith("#")
        packages = [tok.strip('"') for tok in pip_lines[0].split()[2:] if not tok.startswith("-")]
        assert packages, "install line lists at least one module"
        assert all("==" in pkg for pkg in packages), "every module must be pinned"
        for pkg in ["langchain-mcp-adapters==0.3.2", "mcp==1.29.0"]:
            assert pkg in pip_lines[0]

    def test_code_line_count_within_intermediate_ceiling(self):
        total = sum(len(c.splitlines()) for c in code_cells())
        assert total <= 150

    def test_companion_files_exist(self):
        assert NB_PATH.exists()
        assert MD_PATH.exists()
        assert Path(__file__).with_name("lab-local-mcp-assignment.md").exists()


class TestModel:
    def test_model_uses_free_nemotron_on_openrouter(self, lab):
        assert lab["model"].model_name == "nvidia/nemotron-3-super-120b-a12b:free"
        assert lab["model"].openai_api_base == "https://openrouter.ai/api/v1"

    def test_api_key_read_from_environment(self, lab):
        assert lab["model"].openai_api_key is not None


class TestServerScript:
    def test_server_uses_fastmcp(self):
        src = SERVER_PATH.read_text()
        assert "FastMCP" in src and '"notes-server"' in src

    def test_server_exposes_four_notes_tools(self):
        src = SERVER_PATH.read_text()
        for name in ["add_note", "list_notes", "get_note", "delete_note"]:
            assert f"def {name}" in src
        assert src.count("@mcp.tool()") == 4

    def test_server_persists_to_json_and_runs(self):
        src = SERVER_PATH.read_text()
        assert "notes.json" in src
        assert "mcp.run()" in src


class TestClientConnection:
    def test_connection_uses_stdio_and_current_interpreter(self, lab):
        conn = lab["client"].connections["notes"]
        assert conn["transport"] == "stdio"
        assert conn["command"] == sys.executable
        assert "mcp_notes_server.py" in conn["args"][0]

    def test_multiserver_client_supports_name_prefix(self):
        # tool_name_prefix is exercised in Step 13's connection dict
        step13 = next(c for c in code_cells() if "tool_name_prefix" in c)
        assert "tool_name_prefix=True" in step13


class TestAgent:
    def test_agent_built_with_create_agent_from_mcp_tools(self):
        cell = next(c for c in code_cells() if "create_agent" in c and "agent =" in c)
        assert "create_agent(model=model, tools=tools)" in cell


class TestOptionalExerciseComposition:
    def test_optional_exercise_describes_search_tool(self):
        md = MD_PATH.read_text()
        assert "search_notes" in md
        assert "mcp_notes_server.py" in md


class TestLabDocs:
    def test_md_has_all_twelve_sections(self):
        md = MD_PATH.read_text()
        for section in [
            "## 1. Local MCP",
            "## 2. Problem Statement",
            "## 3. Input Data",
            "## 4. Processing",
            "## 5. Output",
            "## 6. Tech Stack",
            "## 7. Underlying Concepts",
            "## 8. Prerequisites",
            "## 9. Environment / Dependencies Setup",
            "## 10. Step-wise Development Instructions",
            "## 11. Optional Exercise",
            "## 12. What We Learnt",
        ]:
            assert section in md, f"missing {section}"

    def test_md_has_mermaid_diagram(self):
        assert "```mermaid" in MD_PATH.read_text()

    def test_md_pins_versions_in_tech_stack(self):
        md = MD_PATH.read_text()
        for pkg in ["langchain-mcp-adapters==0.3.2", "mcp==1.29.0"]:
            assert pkg in md
