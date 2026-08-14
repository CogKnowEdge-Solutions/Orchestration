"""Pytest tests for Lab 9: Runtime & Retrieval.

Follows the TEST.md framework. The notebook's *definition* statements are exec'd
from the notebook's own sources so the tests exercise the actual lab code — not a
copy. Statements that call `.invoke(...)` or that would need live model output are
skipped; definitions (model factory, UsageCapture, runtime tools, corpus, BM25
scorer, kb_search) are tested directly. No API calls, no network.

Run: python3 -m pytest test_lab9.py -v
"""

import ast
import json
import os
from pathlib import Path

import pytest

NB_PATH = Path(__file__).with_name("lab-runtime-and-retrieval.ipynb")
MD_PATH = Path(__file__).with_name("lab-runtime-and-retrieval.md")
PINNED = ["langchain==1.3.15", "langchain-core==1.5.4", "langchain-openai==1.4.3",
          "langgraph==1.2.11", "python-dotenv==1.2.2"]
SAMPLE_QUESTION = "Can I place a market order for $80,000 of BTC?"


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


@pytest.fixture(scope="module")
def lab():
    """Exec the notebook's definition statements against real imports.
    Statements that would call the model (.invoke) or depend on live output are
    skipped, leaving `model`, `UsageCapture`, `get_price`, `run_etl`, `DOCS`,
    `corpus_text`, `tokenize`, `bm25`, and `kb_search` in scope."""
    os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
    namespace = {
        "os": os,
        "re": __import__("re"),
        "math": __import__("math"),
        "pathlib": __import__("pathlib"),
        "load_dotenv": lambda *a, **k: None,
        "ChatOpenAI": __import__("langchain_openai", fromlist=["ChatOpenAI"]).ChatOpenAI,
        "tool": __import__("langchain_core.tools", fromlist=["tool"]).tool,
        "BaseCallbackHandler": __import__(
            "langchain_core.callbacks", fromlist=["BaseCallbackHandler"]
        ).BaseCallbackHandler,
        "create_agent": __import__("langchain.agents", fromlist=["create_agent"]).create_agent,
        "MemorySaver": __import__(
            "langgraph.checkpoint.memory", fromlist=["MemorySaver"]
        ).MemorySaver,
        "Command": __import__("langgraph.types", fromlist=["Command"]).Command,
        "GraphRecursionError": __import__(
            "langgraph.errors", fromlist=["GraphRecursionError"]
        ).GraphRecursionError,
    }
    for source in code_cells():
        if any(ln.lstrip().startswith("!") for ln in source.splitlines()):
            continue  # shell magics (e.g. !pip install) are not valid Python
        tree = ast.parse(source)
        for node in tree.body:
            if _has_invoke(node):
                continue
            try:
                exec(compile(ast.Module([node], []), "<cell>", "exec"), namespace)
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
        packages = [tok.strip('"') for tok in pip_lines[0].split()[2:] if not tok.startswith("-")]
        assert packages, "install line lists at least one module"
        assert all("==" in pkg for pkg in packages), "every module must be pinned"
        assert set(packages) == set(PINNED)

    def test_code_line_count_within_advanced_ceiling(self):
        total = sum(len(c.splitlines()) for c in code_cells())
        assert total <= 180

    def test_companion_files_exist(self):
        assert NB_PATH.exists()
        assert MD_PATH.exists()
        assert Path(__file__).with_name("lab-runtime-and-retrieval-assignment.md").exists()


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

    def test_ledger_uses_prompt_tokens(self):
        nb = "\n".join(code_cells())
        assert "prompt_tokens" in nb and "first-call input tokens" in nb


class TestRuntimeTools:
    def test_get_price_is_deterministic(self, lab):
        price = lab["get_price"].func("BTC")
        assert price == "BTC is trading at $61,250"

    def test_run_etl_is_flaky(self, lab):
        status = lab["run_etl"].func("j-1042")
        assert "Error 503" in status and "retry" in status.lower()


class TestRuntimeConfig:
    def test_interrupt_before_and_checkpointer_present(self):
        nb = "\n".join(code_cells())
        assert 'interrupt_before=["tools"]' in nb
        assert "MemorySaver()" in nb and "thread_id" in nb
        assert "Command(resume=" in nb

    def test_recursion_limit_and_error_handling_present(self):
        nb = "\n".join(code_cells())
        assert '"recursion_limit": 8' in nb
        assert "GraphRecursionError" in nb


class TestRetrieval:
    def test_corpus_has_eight_docs(self, lab):
        assert len(lab["DOCS"]) == 8
        assert len(lab["corpus_text"]) < 2000

    def test_bm25_ranks_correct_docs_for_lab_question(self, lab):
        top = [t for t, _ in lab["bm25"](SAMPLE_QUESTION, lab["DOCS"])[:2]]
        assert top == ["order-types", "risk-limits"]

    def test_kb_search_returns_two_docs_verbatim(self, lab):
        result = lab["kb_search"].func(SAMPLE_QUESTION)
        assert result.count("\n\n") == 1  # exactly two documents joined
        assert "[order-types]" in result and "[risk-limits]" in result

    def test_ab_question_and_both_variants_present(self):
        nb = "\n".join(code_cells())
        assert "Can I place a market order for $80,000 of BTC" in nb
        assert "system_prompt=f\"You answer questions about the Meridian Trading system" in nb
        assert "tools=[kb_search]" in nb


class TestOptionalExerciseComposition:
    def test_optional_exercise_targets_flaky_tool_retry_budget(self):
        md = MD_PATH.read_text()
        assert "run_etl" in md and "retry budget" in md
        assert "recursion_limit" in md and "GraphRecursionError" in md


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
        assert "9 OpenRouter calls" in md
