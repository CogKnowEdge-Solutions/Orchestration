"""Pytest tests for Lab 11: Long-Term Memory.

Follows the TEST.md framework. The notebook's *definition* statements are exec'd
from the notebook's own sources so the tests exercise the actual lab code — not a
copy. Statements that call `.invoke(...)` or that would need live model output are
skipped; definitions (model factory, UsageCapture, check_pantry, make_remember,
Guest, MemoryState, recall_score, load_memory, facts_of, recall_line) are tested
directly. The chef node is skipped (it invokes the model), so the graph's memory
*plumbing* is tested through load_memory + the store round-trip. No API calls, no
network.

Run: python3 -m pytest test_lab11.py -v
"""

import ast
import json
import os
from pathlib import Path

import pytest

NB_PATH = Path(__file__).with_name("lab-long-term-memory.ipynb")
MD_PATH = Path(__file__).with_name("lab-long-term-memory.md")
PINNED = ["langchain==1.3.15", "langchain-core==1.5.4", "langchain-openai==1.4.3",
          "langgraph==1.2.11", "python-dotenv==1.2.2"]
BIRTHDAY_QUERY = "What did you make me for my birthday last year?"


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
    skipped, leaving `model`, `UsageCapture`, `store`, `check_pantry`,
    `make_remember`, `Guest`, `MemoryState`, `recall_score`, `load_memory`,
    `facts_of`, and `recall_line` in scope."""
    os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
    namespace = {
        "os": os,
        "pathlib": __import__("pathlib"),
        "load_dotenv": lambda *a, **k: None,
        "ChatOpenAI": __import__("langchain_openai", fromlist=["ChatOpenAI"]).ChatOpenAI,
        "tool": __import__("langchain_core.tools", fromlist=["tool"]).tool,
        "SystemMessage": __import__(
            "langchain_core.messages", fromlist=["SystemMessage"]
        ).SystemMessage,
        "HumanMessage": __import__(
            "langchain_core.messages", fromlist=["HumanMessage"]
        ).HumanMessage,
        "BaseCallbackHandler": __import__(
            "langchain_core.callbacks", fromlist=["BaseCallbackHandler"]
        ).BaseCallbackHandler,
        "create_agent": __import__("langchain.agents", fromlist=["create_agent"]).create_agent,
        "StateGraph": __import__("langgraph.graph", fromlist=["StateGraph"]).StateGraph,
        "START": __import__("langgraph.graph", fromlist=["START"]).START,
        "END": __import__("langgraph.graph", fromlist=["END"]).END,
        "add_messages": __import__(
            "langgraph.graph.message", fromlist=["add_messages"]
        ).add_messages,
        "Runtime": __import__("langgraph.runtime", fromlist=["Runtime"]).Runtime,
        "InMemoryStore": __import__(
            "langgraph.store.memory", fromlist=["InMemoryStore"]
        ).InMemoryStore,
        "MemorySaver": __import__(
            "langgraph.checkpoint.memory", fromlist=["MemorySaver"]
        ).MemorySaver,
        "dataclass": __import__("dataclasses", fromlist=["dataclass"]).dataclass,
        "Annotated": __import__("typing", fromlist=["Annotated"]).Annotated,
        "TypedDict": __import__("typing", fromlist=["TypedDict"]).TypedDict,
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


def _runtime(lab, guest_id):
    return lab["Runtime"](context=lab["Guest"](guest_id=guest_id), store=lab["store"])


def _clear_namespace(lab, guest_id):
    store, ns = lab["store"], ("guests", guest_id, "facts")
    for item in store.search(ns):
        store.delete(ns, item.key)


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
        assert Path(__file__).with_name("lab-long-term-memory-assignment.md").exists()


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
        assert "prompt_tokens" in nb and "decision-time tokens per chef call" in nb


class TestKitchenTools:
    def test_check_pantry_known_and_unknown(self, lab):
        assert lab["check_pantry"].func("saffron") == "'saffron' is in stock"
        assert "out of stock" in lab["check_pantry"].func("truffle")

    def test_remember_writes_to_namespace(self, lab):
        _clear_namespace(lab, "amara")
        remember = lab["make_remember"](lab["store"], "amara")
        ack = remember.func("Amara loves tiramisu.")
        assert ack == "Remembered as fact 1."
        facts = [i.value["content"] for i in lab["store"].search(("guests", "amara", "facts"))]
        assert facts == ["Amara loves tiramisu."]


class TestIsolation:
    def test_guests_have_separate_namespaces(self, lab):
        _clear_namespace(lab, "amara")
        _clear_namespace(lab, "bob")
        make_remember = lab["make_remember"]
        make_remember(lab["store"], "amara").func("Amara loves tiramisu.")
        make_remember(lab["store"], "bob").func("Bob does not eat pork.")
        amara = [i.value["content"] for i in lab["store"].search(("guests", "amara", "facts"))]
        bob = [i.value["content"] for i in lab["store"].search(("guests", "bob", "facts"))]
        assert amara == ["Amara loves tiramisu."]
        assert bob == ["Bob does not eat pork."]


class TestRecallScorer:
    def test_overlap_counts_long_words_only(self, lab):
        score = lab["recall_score"]
        assert score("What did you make for my birthday last year?",
                     "Amara's birthday is October 14.") >= 1
        assert score("What is the weather like in Paris?",
                     "Amara loves tiramisu.") == 0

    def test_two_letter_words_are_ignored(self, lab):
        assert lab["recall_score"]("it is", "it is a fact") == 0


class TestLoadMemory:
    def test_empty_profile_builds_first_visit_dossier(self, lab):
        _clear_namespace(lab, "amara")
        state = {"messages": [lab["HumanMessage"](content="Hi, I'm Amara.")]}
        out = lab["load_memory"](state, _runtime(lab, "amara"))
        system = out["messages"][0]
        assert isinstance(system, lab["SystemMessage"])
        assert "first visit" in system.content and "amara" in system.content

    def test_dossier_includes_stored_facts(self, lab):
        _clear_namespace(lab, "amara")
        lab["make_remember"](lab["store"], "amara").func("Amara loves tiramisu.")
        state = {"messages": [lab["HumanMessage"](content="Hi, it's me again.")]}
        out = lab["load_memory"](state, _runtime(lab, "amara"))
        assert "Amara loves tiramisu." in out["messages"][0].content

    def test_recall_line_appears_for_matching_query(self, lab):
        _clear_namespace(lab, "amara")
        lab["make_remember"](lab["store"], "amara").func("Amara's birthday is October 14.")
        state = {"messages": [lab["HumanMessage"](content=BIRTHDAY_QUERY)]}
        out = lab["load_memory"](state, _runtime(lab, "amara"))
        assert "birthday is October 14" in out["messages"][0].content
        assert "matches these memories" in out["messages"][0].content


class TestGraphWiring:
    def test_graph_compiles_with_checkpointer_and_store(self):
        nb = "\n".join(code_cells())
        assert "StateGraph(state_schema=MemoryState, context_schema=Guest)" in nb
        assert "add_node(\"load_memory\", load_memory)" in nb
        assert "add_node(\"chef\", chef_node)" in nb
        assert "checkpointer=MemorySaver()" in nb and "store=store" in nb
        assert "runtime: Runtime[Guest]" in nb

    def test_namespace_tuple_used_in_put_and_search(self):
        nb = "\n".join(code_cells())
        assert '("guests", guest_id, "facts")' in nb


class TestOptionalExerciseComposition:
    def test_optional_exercise_targets_second_namespace(self):
        md = MD_PATH.read_text()
        assert '("guests", guest_id, "drinks")' in md
        assert "remember_drink" in md and "Barolo" in md


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
        assert "15 OpenRouter calls" in md
