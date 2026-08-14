"""Pytest tests for Lab 5: Agent Middleware.

Follows the TEST.md framework (core logic, output structure, docs-vs-behavior).
The notebook's *definition* statements are exec'd from the notebook's own
sources, so these tests exercise the actual lab code — not a copy. Statements
that call `.invoke(...)` (which would hit the API) are skipped, and the
prebuilt/custom middleware are then tested directly against real langchain
classes with hand-built states. No API calls are made.

Run: python3 -m pytest test_lab5.py -v
"""

import ast
import json
import os
from pathlib import Path

import pytest
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import AIMessage, HumanMessage

NB_PATH = Path(__file__).with_name("lab-agent-middleware.ipynb")


def code_cells():
    with open(NB_PATH) as f:
        notebook = json.load(f)
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def _calls_invoke(node) -> bool:
    return any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "invoke"
        for n in ast.walk(node)
    )


@pytest.fixture(scope="module")
def lab():
    """Exec the notebook's definition statements against real langchain classes.
    Invocation statements (which would call the API) and statements that depend
    on an invoke result (they NameError) are skipped, leaving every middleware
    class, tool, and agent in the namespace — including `stacked_agent`."""
    os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
    namespace = {"os": os, "load_dotenv": lambda *a, **k: None}
    for source in code_cells():
        if any(ln.lstrip().startswith("!") for ln in source.splitlines()):
            continue  # shell magics (e.g. !pip install) are not valid Python
        tree = ast.parse(source)
        for node in tree.body:
            if _calls_invoke(node):
                continue
            try:
                exec(compile(ast.Module([node], []), "<cell>", "exec"), namespace)
            except NameError:
                continue
    yield namespace


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
        packages = [tok.strip('"') for tok in pip_lines[0].split()[2:] if not tok.startswith("-")]
        assert packages, "install line lists at least one module"
        assert all("==" in pkg for pkg in packages), "every module must be pinned"


class TestPlainAgent:
    """Step 4: the lab builds a plain agent with create_agent."""

    def test_agent_created(self, lab):
        assert "agent" in lab
        assert "create_agent" in lab

    def test_agent_uses_no_middleware(self, lab):
        sources = code_cells()
        plain = [s for s in sources if "create_agent(\n" in s and "middleware=" not in s]
        assert plain, "Step 4 builds a bare agent without middleware"


class TestPrebuiltPII:
    """Steps 5: PIIMiddleware redacts input before the model sees it; block raises."""

    def test_redact_scrubs_email_from_input(self, lab):
        middleware = lab["PIIMiddleware"]("email", strategy="redact", apply_to_input=True)
        state = {"messages": [HumanMessage("Contact me at test@example.com")]}
        result = middleware.before_model(state, None)
        new_human = [m for m in result["messages"] if m.type == "human"][-1]
        assert "test@example.com" not in str(new_human.content)
        assert "[REDACTED_EMAIL]" in str(new_human.content)

    def test_redact_leaves_clean_input_untouched(self, lab):
        middleware = lab["PIIMiddleware"]("email", strategy="redact", apply_to_input=True)
        state = {"messages": [HumanMessage("No sensitive data here")]}
        assert middleware.before_model(state, None) is None

    def test_block_raises_before_any_call(self, lab):
        middleware = lab["PIIMiddleware"]("email", strategy="block", apply_to_input=True)
        state = {"messages": [HumanMessage("Contact me at test@example.com")]}
        with pytest.raises(lab["PIIDetectionError"]):
            middleware.before_model(state, None)

    def test_both_pii_agents_built(self, lab):
        assert "pii_redact" in lab and "pii_block" in lab


class TestPrebuiltCallLimit:
    """Step 6: ModelCallLimitMiddleware refuses a call once the run budget is spent."""

    def test_at_limit_jumps_to_end(self, lab):
        middleware = lab["ModelCallLimitMiddleware"](run_limit=1, exit_behavior="end")
        state = {"thread_model_call_count": 0, "run_model_call_count": 1}
        result = middleware.before_model(state, None)
        assert result is not None and result.get("jump_to") == "end"

    def test_under_limit_allows_call(self, lab):
        middleware = lab["ModelCallLimitMiddleware"](run_limit=1, exit_behavior="end")
        state = {"thread_model_call_count": 0, "run_model_call_count": 0}
        assert middleware.before_model(state, None) is None

    def test_budget_agent_has_weather_tool(self, lab):
        assert "budget_agent" in lab
        assert lab["get_weather"].name == "get_weather"


class TestCustomMiddleware:
    """Steps 7-9: class-based, wrap-based, and decorator-based middleware exist
    and expose the hooks the notebook uses."""

    def test_logging_middleware_is_agent_middleware(self, lab):
        assert issubclass(lab["LoggingMiddleware"], AgentMiddleware)

    def test_logging_hooks_return_none(self, lab, capsys):
        middleware = lab["LoggingMiddleware"]()
        assert middleware.before_model({"messages": [HumanMessage("hi")]}, None) is None
        state = {"messages": [HumanMessage("hi"), AIMessage("hello")]}
        assert middleware.after_model(state, None) is None
        out = capsys.readouterr().out
        assert "[before_model]" in out and "[after_model]" in out

    def test_timing_wrap_returns_model_response(self, lab):
        middleware = lab["TimingMiddleware"]()
        fake_request = object()
        response = lab["ModelResponse"](result=[AIMessage(content="ok")])

        def handler(_request):
            return response

        assert middleware.wrap_model_call(fake_request, handler) is response

    def test_decorators_produce_middleware_instances(self, lab):
        assert isinstance(lab["log_before"], AgentMiddleware)
        assert isinstance(lab["log_after"], AgentMiddleware)

    def test_custom_agents_created(self, lab):
        for name in ("logging_agent", "timing_agent", "decorated_agent"):
            assert name in lab, f"{name} was not created"


class TestOptionalExerciseComposition:
    """Section 11: one agent stacks all three kinds of middleware."""

    def test_stacked_agent_created(self, lab):
        assert "stacked_agent" in lab

    def test_notebook_stacks_three_middleware_kinds(self):
        sources = code_cells()
        assert any("LoggingMiddleware()," in s for s in sources)
        assert any('PIIMiddleware("email", strategy="redact"' in s for s in sources)
        assert any("ModelCallLimitMiddleware(run_limit=1" in s for s in sources)

    def test_hook_execution_order(self, lab):
        middleware = lab["LoggingMiddleware"]()
        seen = []
        original_before = middleware.before_model
        original_after = middleware.after_model
        middleware.before_model = lambda s, r: seen.append("before") or original_before(s, r)
        middleware.after_model = lambda s, r: seen.append("after") or original_after(s, r)
        middleware.before_model({"messages": [HumanMessage("hi")]}, None)
        middleware.after_model({"messages": [HumanMessage("hi"), AIMessage("hi")]}, None)
        assert seen == ["before", "after"]
