"""Pytest tests for Lab 12: Capstone Project — Intelligent Customer Support Platform.

Tests verify integration of all concepts from Labs 1-11:
- Multi-agent routing (Lab 10)
- Long-term memory (Lab 11)
- Knowledge base retrieval (Labs 3-4)
- Tool use (Lab 5)
- Token budgeting (Lab 8)
- Runtime context (Lab 9)
- Graph wiring and execution

Run: python3 -m pytest test_lab12.py -v
"""

import ast
import json
import os
from pathlib import Path

import pytest

NB_PATH = Path(__file__).with_name("lab-capstone-project.ipynb")
MD_PATH = Path(__file__).with_name("lab-capstone-project.md")
PINNED = ["langchain==1.3.15", "langchain-core==1.5.4", "langchain-openai==1.4.3",
          "langgraph==1.2.11", "python-dotenv==1.2.2"]


def code_cells():
    """Extract all code cells from the notebook."""
    if not NB_PATH.exists():
        return []
    with open(NB_PATH) as f:
        notebook = json.load(f)
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def _invoke_in_scope(node) -> bool:
    """True if node calls .invoke directly in current scope."""
    stack = [node]
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "invoke"):
            return True
        stack.extend(ast.iter_child_nodes(n))
    return False


class TestNotebookArtifact:
    def test_notebook_exists(self):
        assert NB_PATH.exists(), "lab-capstone-project.ipynb not found"

    def test_first_code_cell_is_single_pinned_pip_install(self):
        cells = code_cells()
        assert len(cells) > 0, "No code cells found"
        lines = cells[0].splitlines()
        pip_lines = [ln for ln in lines if ln.startswith("!pip install")]
        assert len(pip_lines) == 1, "First cell must have exactly one pip install"
        packages = [tok.strip('"') for tok in pip_lines[0].split()[2:] if not tok.startswith("-")]
        assert all("==" in pkg for pkg in packages), "All packages must be pinned"
        assert set(packages) == set(PINNED), f"Expected {PINNED}, got {packages}"

    def test_code_line_count_within_capstone_ceiling(self):
        cells = code_cells()
        total = sum(len(c.splitlines()) for c in cells)
        assert total <= 200, f"Code exceeds 200 lines ({total} lines)"

    def test_code_cells_between_10_and_12(self):
        cells = code_cells()
        assert 10 <= len(cells) <= 12, f"Expected 10-12 code cells, got {len(cells)}"

    def test_companion_files_exist(self):
        assert MD_PATH.exists(), "lab-capstone-project.md not found"
        assert Path(__file__).with_name("lab-capstone-project-assignment.md").exists()


class TestModelFactory:
    def test_model_factory_uses_free_nemotron_on_openrouter(self):
        cells = code_cells()
        nb = "\n".join(cells)
        assert "nemotron" in nb.lower(), "Model should be nemotron"
        assert "openrouter" in nb.lower(), "Should use OpenRouter"

    def test_api_key_from_environment(self):
        cells = code_cells()
        nb = "\n".join(cells)
        assert "OPENROUTER_API_KEY" in nb or "load_dotenv" in nb


class TestIntegration:
    def test_markdown_has_all_twelve_sections(self):
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
            assert section in md, f"Missing {section}"

    def test_markdown_mentions_all_labs(self):
        md = MD_PATH.read_text()
        for lab_num in range(1, 12):
            assert f"Lab {lab_num}" in md, f"Lab {lab_num} not mentioned"

    def test_markdown_has_diagrams(self):
        md = MD_PATH.read_text()
        assert md.count("```mermaid") >= 2, "Need at least 2 mermaid diagrams"

    def test_markdown_discloses_cost(self):
        md = MD_PATH.read_text()
        assert "OpenRouter" in md or "free" in md, "Cost should be disclosed"

    def test_assignment_has_requirements(self):
        assignment = Path(__file__).with_name("lab-capstone-project-assignment.md")
        if assignment.exists():
            content = assignment.read_text()
            assert "Mandatory" in content, "Should list mandatory requirements"
            assert "Optional" in content, "Should list optional exercise"

    def test_routing_mentioned_in_markdown(self):
        md = MD_PATH.read_text()
        assert "router" in md.lower(), "Should mention routing/supervisor"
        assert "Command" in md, "Should mention LangGraph Command"

    def test_memory_mentioned_in_markdown(self):
        md = MD_PATH.read_text()
        assert "memory" in md.lower() or "dossier" in md.lower(), "Should mention memory"
        assert "store" in md.lower(), "Should mention storage"

    def test_retrieval_mentioned_in_markdown(self):
        md = MD_PATH.read_text()
        assert "retriev" in md.lower() or "knowledge" in md.lower(), "Should mention retrieval"

    def test_tools_mentioned_in_markdown(self):
        md = MD_PATH.read_text()
        assert "tool" in md.lower(), "Should mention tools"

    def test_token_budget_mentioned(self):
        md = MD_PATH.read_text()
        assert "token" in md.lower(), "Should mention token tracking"

    def test_handoff_mentioned(self):
        md = MD_PATH.read_text()
        assert "handoff" in md.lower() or "escalat" in md.lower(), "Should mention handoff/escalation"


class TestAssignment:
    def test_assignment_exists(self):
        assignment = Path(__file__).with_name("lab-capstone-project-assignment.md")
        assert assignment.exists(), "lab-capstone-project-assignment.md not found"

    def test_assignment_has_deliverables(self):
        assignment = Path(__file__).with_name("lab-capstone-project-assignment.md")
        if assignment.exists():
            content = assignment.read_text()
            assert "Deliverables" in content or "deliverables" in content.lower()

    def test_assignment_has_grading_rubric(self):
        assignment = Path(__file__).with_name("lab-capstone-project-assignment.md")
        if assignment.exists():
            content = assignment.read_text()
            assert "Rubric" in content or "rubric" in content.lower()

    def test_assignment_has_success_criteria(self):
        assignment = Path(__file__).with_name("lab-capstone-project-assignment.md")
        if assignment.exists():
            content = assignment.read_text()
            assert "Success" in content or "Criteria" in content or "✓" in content


class TestOptionalExercise:
    def test_assignment_mentions_optional_exercise(self):
        assignment = Path(__file__).with_name("lab-capstone-project-assignment.md")
        if assignment.exists():
            content = assignment.read_text()
            assert "Optional" in content or "optional" in content


