"""Pytest tests for Lab 10: Multi-Agent Coordination.

Follows the TEST.md framework. The notebook's *definition* statements are exec'd
from the notebook's own sources so the tests exercise the actual lab code — not a
copy. Statements that would call the model (any `.invoke(...)` executed at the top
level) or that depend on live output are skipped; definitions (model factory,
UsageCapture, the six tools, the route tools, the supervisor/specialist node
factories, `build_desk`, the handoff tools) are tested directly. Because the node
*functions* never call the model until invoked, the fixture can compile the real
`desk` graph offline — no API calls, no network.

Run: python3 -m pytest test_lab10.py -v
"""

import ast
import json
import os
from pathlib import Path

import pytest
from langgraph.types import Command

NB_PATH = Path(__file__).with_name("lab-multi-agent-coordination.ipynb")
MD_PATH = Path(__file__).with_name("lab-multi-agent-coordination.md")
PINNED = ["langchain==1.3.15", "langchain-core==1.5.4", "langchain-openai==1.4.3",
          "langgraph==1.2.11", "python-dotenv==1.2.2"]


def code_cells():
    with open(NB_PATH) as f:
        notebook = json.load(f)
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def _invoke_in_scope(node) -> bool:
    """True if `node` calls `.invoke` directly in the current scope — i.e. the
    statement would make a live model call when exec'd. Calls nested inside a
    `def` body are *not* direct (the body only runs when the function is called),
    so a node-function definition is safe to exec."""
    stack = [node]
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue  # do not descend into function bodies
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "invoke"):
            return True
        stack.extend(ast.iter_child_nodes(n))
    return False


@pytest.fixture(scope="module")
def lab():
    """Exec the notebook's definition statements against real imports.
    Live `.invoke` statements and top-level `print(...)` calls are skipped,
    leaving `model`, `UsageCapture`, the six tools, `ALL_TOOLS`, the route
    tools, `ROUTE_TO_NODE`, `RoutingState`, `supervisor_node`,
    `specialist_node`, `build_desk`, the two handoff tools, and the compiled
    `desk` graph in scope."""
    os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
    namespace = {
        "os": os,
        "pathlib": __import__("pathlib"),
        "load_dotenv": lambda *a, **k: None,
        "ChatOpenAI": __import__("langchain_openai", fromlist=["ChatOpenAI"]).ChatOpenAI,
        "tool": __import__("langchain_core.tools", fromlist=["tool"]).tool,
        "BaseCallbackHandler": __import__(
            "langchain_core.callbacks", fromlist=["BaseCallbackHandler"]
        ).BaseCallbackHandler,
        "SystemMessage": __import__(
            "langchain_core.messages", fromlist=["SystemMessage"]
        ).SystemMessage,
        "create_agent": __import__("langchain.agents", fromlist=["create_agent"]).create_agent,
        "StateGraph": __import__("langgraph.graph", fromlist=["StateGraph"]).StateGraph,
        "START": __import__("langgraph.graph", fromlist=["START"]).START,
        "END": __import__("langgraph.graph", fromlist=["END"]).END,
        "add_messages": __import__(
            "langgraph.graph.message", fromlist=["add_messages"]
        ).add_messages,
        "Command": __import__("langgraph.types", fromlist=["Command"]).Command,
        "Annotated": __import__("typing", fromlist=["Annotated"]).Annotated,
        "TypedDict": __import__("typing", fromlist=["TypedDict"]).TypedDict,
    }
    for source in code_cells():
        if any(ln.lstrip().startswith("!") for ln in source.splitlines()):
            continue  # shell magics (e.g. !pip install) are not valid Python
        tree = ast.parse(source)
        for node in tree.body:
            if _invoke_in_scope(node):
                continue
            stmt = ast.Module([node], [])
            if (isinstance(node, ast.Expr)
                    and isinstance(node.value, ast.Call)
                    and getattr(node.value.func, "id", None) == "print"):
                continue
            try:
                exec(compile(stmt, "<cell>", "exec"), namespace)
            except Exception:
                continue  # statement depends on a skipped live run
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
        packages = [tok.strip('"') for tok in pip_lines[0].split()[2:]]
        assert packages, "install line lists at least one module"
        assert all("==" in pkg for pkg in packages), "every module must be pinned"
        assert set(packages) == set(PINNED)

    def test_code_line_count_within_advanced_ceiling(self):
        total = sum(len(c.splitlines()) for c in code_cells())
        assert total <= 180

    def test_companion_files_exist(self):
        assert NB_PATH.exists()
        assert MD_PATH.exists()
        assert Path(__file__).with_name("lab-multi-agent-coordination-assignment.md").exists()


class TestModelFactory:
    def test_model_factory_uses_free_nemotron_on_openrouter(self, lab):
        m = lab["model"]()
        assert m.model_name == "nvidia/nemotron-3-super-120b-a12b:free"
        assert m.openai_api_base == "https://openrouter.ai/api/v1"

    def test_api_key_read_from_environment(self, lab):
        assert lab["model"]().openai_api_key is not None


class TestUsageCapture:
    def test_capture_starts_empty(self, lab):
        assert lab["UsageCapture"]().calls == []

    def test_capture_records_prompt_tokens_on_end(self, lab):
        class FakeResponse:
            llm_output = {"token_usage": {"prompt_tokens": 660}}

        capture = lab["UsageCapture"]()
        capture.on_llm_end(FakeResponse())
        assert capture.calls == [660]


class TestTools:
    def test_get_invoice(self, lab):
        assert lab["get_invoice"].func("acct-2214") == (
            "Invoice #INV-2214: $99.00 charged on 2026-08-01; "
            "a duplicate $99.00 charge appeared on 2026-08-12."
        )

    def test_process_refund(self, lab):
        assert "Refund of $99.00" in lab["process_refund"].func("INV-2214")

    def test_check_service_status(self, lab):
        assert "HTTP 503" in lab["check_service_status"].func()

    def test_search_kb(self, lab):
        assert "KB-301" in lab["search_kb"].func("503")

    def test_get_plan(self, lab):
        assert "Team (10 seats)" in lab["get_plan"].func("acct-2214")

    def test_set_seats(self, lab):
        assert "12 seats" in lab["set_seats"].func("acct-2214", 12)

    def test_all_tools_lists_all_six(self, lab):
        funcs = [t.func.__name__ for t in lab["ALL_TOOLS"]]
        assert funcs == ["get_invoice", "process_refund", "check_service_status",
                         "search_kb", "get_plan", "set_seats"]


class TestRoutingTools:
    def test_route_tools_return_their_route(self, lab):
        assert lab["route_billing"].func() == "routed to billing"
        assert lab["route_tech"].func() == "routed to tech"
        assert lab["route_account"].func() == "routed to account"

    def test_route_tool_names_map_to_nodes(self, lab):
        assert lab["ROUTE_TO_NODE"] == {
            "route_billing": "billing",
            "route_tech": "tech",
            "route_account": "account",
        }

    def test_supervisor_prompt_covers_all_departments(self):
        nb = "\n".join(code_cells())
        assert "SUPERVISOR_PROMPT" in nb
        for word in ["Billing", "Tech", "Account"]:
            assert word in nb


class TestGraphWiring:
    def test_desk_compiles_offline_with_four_nodes(self, lab):
        desk = lab["desk"]
        assert {"supervisor", "billing", "tech", "account"} <= set(desk.nodes)

    def test_routing_state_uses_add_messages(self, lab):
        state = lab["RoutingState"]
        assert "messages" in state.__annotations__
        nb = "\n".join(code_cells())
        assert "Annotated[list, add_messages]" in nb


class TestHandoffTools:
    def _reset_budget(self, lab):
        lab["handoff_budget"]["left"] = 1
        lab["transfer_log"].clear()

    def test_transfer_to_tech_returns_parent_command(self, lab):
        self._reset_budget(lab)
        cmd = lab["transfer_to_tech"].func("api is down")
        assert cmd.goto == "tech" and cmd.graph == Command.PARENT

    def test_transfer_to_billing_returns_parent_command(self, lab):
        self._reset_budget(lab)
        cmd = lab["transfer_to_billing"].func("double charge")
        assert cmd.goto == "billing" and cmd.graph == Command.PARENT

    def test_handoff_budget_blocks_second_transfer(self, lab):
        self._reset_budget(lab)
        assert lab["transfer_log"] == []
        lab["transfer_to_tech"].func("down")
        assert lab["handoff_budget"]["left"] == 0
        assert lab["transfer_log"] == ["transfer_to_tech"]
        blocked = lab["transfer_to_tech"].func("still down")
        assert isinstance(blocked, str) and "already transferred" in blocked
        assert lab["transfer_log"] == ["transfer_to_tech"]


class TestOptionalExerciseComposition:
    def test_optional_exercise_targets_fourth_department(self):
        md = MD_PATH.read_text()
        assert "security" in md and "route_security" in md
        assert "review_account_access" in md


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

    def test_md_has_mermaid_diagrams(self):
        assert MD_PATH.read_text().count("```mermaid") >= 2

    def test_md_pins_versions_and_discloses_cost(self):
        md = MD_PATH.read_text()
        for pkg in ["langchain==1.3.15", "langgraph==1.2.11", "python-dotenv==1.2.2"]:
            assert pkg in md
        assert "OpenRouter calls" in md
