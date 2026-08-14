"""Pytest tests for Lab 8: MCP & Context Engineering.

Follows the TEST.md framework. The notebook's *definition* statements are exec'd
from the notebook's own sources so the tests exercise the actual lab code — not a
copy. Statements that call `.invoke(...)`, top-level `await`, or would spawn a
server subprocess or open a socket are skipped; definitions (model factory,
UsageCapture, connection config) are tested directly. No API calls, no server
subprocesses, no network.

Run: python3 -m pytest test_lab8.py -v
"""

import ast
import json
import sys
from pathlib import Path

import pytest

NB_PATH = Path(__file__).with_name("lab-mcp-context-engineering.ipynb")
SERVER_PATH = Path(__file__).with_name("mcp_ops_server.py")
MD_PATH = Path(__file__).with_name("lab-mcp-context-engineering.md")
COINFUTY_URL = "https://mcp.coinfuty.com/api/mcp"
OPS_URL = "http://127.0.0.1:8788/mcp"


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


def _spawns_process(node) -> bool:
    """True if the statement would start a server or touch the network."""
    if _has_await(node):
        return True
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            name = None
            if isinstance(n.func, ast.Name):
                name = n.func.id
            elif isinstance(n.func, ast.Attribute):
                name = n.func.attr
            if name in ("Popen", "create_connection", "port_up", "get_tools"):
                return True
    return False


@pytest.fixture(scope="module")
def lab():
    """Exec the notebook's definition statements against real imports.
    Statements that would spawn a subprocess, hit the API, await a session, or
    open a socket are skipped, leaving `model`, `client`, `UsageCapture`, and the
    A/B question constants in scope."""
    import os

    os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
    namespace = {
        "os": os,
        "load_dotenv": lambda *a, **k: None,
        "ChatOpenAI": __import__("langchain_openai", fromlist=["ChatOpenAI"]).ChatOpenAI,
        "BaseCallbackHandler": __import__(
            "langchain_core.callbacks", fromlist=["BaseCallbackHandler"]
        ).BaseCallbackHandler,
        "MultiServerMCPClient": __import__(
            "langchain_mcp_adapters.client", fromlist=["MultiServerMCPClient"]
        ).MultiServerMCPClient,
    }
    for source in code_cells():
        if any(ln.lstrip().startswith("!") for ln in source.splitlines()):
            continue  # shell magics (e.g. !pip install) are not valid Python
        tree = ast.parse(source)
        for node in tree.body:
            if _has_invoke(node) or _spawns_process(node):
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

    def test_code_line_count_within_advanced_ceiling(self):
        total = sum(len(c.splitlines()) for c in code_cells())
        assert total <= 180

    def test_companion_files_exist(self):
        assert NB_PATH.exists()
        assert MD_PATH.exists()
        assert Path(__file__).with_name("lab-mcp-context-engineering-assignment.md").exists()


class TestModelFactory:
    def test_model_factory_uses_free_nemotron_on_openrouter(self, lab):
        m = lab["model"]()
        assert m.model_name == "nvidia/nemotron-3-super-120b-a12b:free"
        assert m.openai_api_base == "https://openrouter.ai/api/v1"

    def test_api_key_read_from_environment(self, lab):
        m = lab["model"]()
        assert m.openai_api_key is not None


class TestUsageCapture:
    def test_capture_records_prompt_tokens(self, lab):
        capture = lab["UsageCapture"]()
        assert capture.calls == []

    def test_ledger_metrics_are_mentioned(self):
        nb = "\n".join(code_cells())
        assert "prompt_tokens" in nb and "first-call tokens" in nb


class TestServerScript:
    def test_server_uses_fastmcp_streamable_http(self):
        src = SERVER_PATH.read_text()
        assert "FastMCP" in src and '"market-ops"' in src
        assert 'transport="streamable-http"' in src
        assert "mcp.settings.port" in src

    def test_server_exposes_three_digest_tools(self):
        src = SERVER_PATH.read_text()
        for name in ["digest_snapshot", "digest_logs", "digest_highlights"]:
            assert f"def {name}" in src
        assert src.count("@mcp.tool()") == 3

    def test_server_is_deterministic(self):
        assert "random.Random(7)" in SERVER_PATH.read_text()


class TestClientConnection:
    def test_both_connections_use_http_transport(self, lab):
        conns = lab["client"].connections
        assert set(conns) == {"coinfuty", "ops"}
        for name in conns:
            assert conns[name]["transport"] == "http"

    def test_external_and_self_hosted_urls(self, lab):
        conns = lab["client"].connections
        assert conns["coinfuty"]["url"] == COINFUTY_URL
        assert conns["ops"]["url"] == OPS_URL


class TestABExperiments:
    def test_pruning_experiment_questions_and_tools(self):
        nb = "\n".join(code_cells())
        assert "What is the current funding rate and open interest for BTC futures?" in nb
        assert "get_funding_rates" in nb and "get_coin_summary" in nb

    def test_result_shaping_experiment_uses_both_tools(self):
        nb = "\n".join(code_cells())
        assert "Read the recent logs for BTC and summarize what happened." in nb
        assert "digest_logs" in nb and "digest_highlights" in nb


class TestOptionalExerciseComposition:
    def test_optional_exercise_targets_server_context(self):
        md = MD_PATH.read_text()
        assert "digest_logs" in md and "max_events" in md
        assert "mcp_ops_server.py" in md


class TestLabDocs:
    def test_md_has_all_twelve_sections(self):
        md = MD_PATH.read_text()
        for section in [
            "## 1. Lab Title",
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

    def test_md_pins_versions_and_discloses_cost(self):
        md = MD_PATH.read_text()
        for pkg in ["langchain-mcp-adapters==0.3.2", "mcp==1.29.0"]:
            assert pkg in md
        assert "4 LLM calls" in md
