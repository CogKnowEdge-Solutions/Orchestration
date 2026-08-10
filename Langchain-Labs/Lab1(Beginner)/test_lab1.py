"""Pytest tests for Lab 1: Agents & Models.

Follows the TEST.md framework (core logic, boundaries, input validity, error
handling, docs-vs-behavior, security/config hygiene). The tool code is exec'd
from the notebook's own cells, so these tests exercise the actual lab code —
not a copy. No API calls are made.

Run: python3 -m pytest test_lab1.py -v
"""

import json
from pathlib import Path

import pytest
from langchain_core.utils.function_calling import convert_to_openai_tool

NB_PATH = Path(__file__).with_name("lab-agents-models.ipynb")


def code_cells():
    with open(NB_PATH) as f:
        notebook = json.load(f)
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def cell_source(snippet):
    for source in code_cells():
        if snippet in source:
            return source
    raise AssertionError(f"No code cell contains: {snippet}")


def run_cell(snippet):
    namespace = {}
    exec(cell_source(snippet), namespace)
    return namespace


@pytest.fixture(scope="module")
def multiply():
    return run_cell("def multiply")["multiply"]


class TestMultiplyCoreLogic:
    def test_multiply_two_numbers(self, multiply):
        assert multiply(8, 7) == 56

    def test_multiply_by_zero(self, multiply):
        assert multiply(0, 5) == 0

    def test_multiply_negative_numbers(self, multiply):
        assert multiply(-8, 7) == -56

    def test_multiply_negative_times_negative(self, multiply):
        assert multiply(-3.5, -2.5) == 8.75

    def test_multiply_decimals(self, multiply):
        assert multiply(2.5, 4.2) == 10.5

    def test_multiply_large_numbers(self, multiply):
        assert multiply(999999, 888888) == 888887111112

    def test_multiply_single_digit(self, multiply):
        assert multiply(1, 1) == 1

    def test_multiply_large_decimal(self, multiply):
        assert multiply(123.456, 789.012) == pytest.approx(97408.265472)

    def test_multiply_is_deterministic(self, multiply):
        assert multiply(123.456, 789.012) == multiply(123.456, 789.012)


class TestMultiplyInputValidity:
    def test_wrong_type_raises_type_error(self, multiply):
        with pytest.raises(TypeError):
            multiply("a", "b")

    def test_none_raises_type_error(self, multiply):
        with pytest.raises(TypeError):
            multiply(None, 5)


class TestToolSchema:
    """Docs-vs-behavior: the schema the model sees matches the function."""

    def test_docstring_present(self, multiply):
        assert multiply.__doc__ is not None
        assert "product" in multiply.__doc__

    def test_type_hints_present(self, multiply):
        annotations = multiply.__annotations__
        assert annotations.get("a") is float
        assert annotations.get("b") is float
        assert annotations.get("return") is float

    def test_schema_name_and_description(self, multiply):
        schema = convert_to_openai_tool(multiply)["function"]
        assert schema["name"] == "multiply"
        assert schema["description"] == "Multiply two numbers and return their product."

    def test_schema_parameters(self, multiply):
        parameters = convert_to_openai_tool(multiply)["function"]["parameters"]
        assert parameters["type"] == "object"
        assert parameters["properties"]["a"] == {"type": "number"}
        assert parameters["properties"]["b"] == {"type": "number"}
        assert parameters["required"] == ["a", "b"]


class TestApiKeyHandling:
    """Error handling: a missing key fails fast with a clear message."""

    @staticmethod
    def _key_cell():
        return cell_source("load_dotenv")

    def test_missing_key_raises_system_exit(self, monkeypatch):
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
        monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: None)
        with pytest.raises(SystemExit) as exc_info:
            exec(self._key_cell(), {})
        assert "OPENROUTER_API_KEY" in str(exc_info.value)

    def test_key_present_does_not_raise(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")
        monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: None)
        exec(self._key_cell(), {})


class TestNotebookArtifact:
    """CQ-10: the first code cell is a single pinned `!pip install` line."""

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
