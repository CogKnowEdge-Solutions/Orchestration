"""Pytest tests for Lab 2: Messages & Tools.

Follows the TEST.md framework (core logic, boundaries, input validity,
output structure, docs-vs-behavior). The tool and message code is exec'd from
the notebook's own cells, so these tests exercise the actual lab code — not a
copy. No API calls are made.

Run: python3 -m pytest test_lab2.py -v
"""

import json
from pathlib import Path

import pytest
from langchain_core.utils.function_calling import convert_to_openai_tool

NB_PATH = Path(__file__).with_name("lab-messages-tools.ipynb")


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
def tools():
    return run_cell("def add")


class TestAddCoreLogic:
    def test_add_two_numbers(self, tools):
        assert tools["add"](5, 3) == 8

    def test_add_with_zero(self, tools):
        assert tools["add"](0, 5) == 5

    def test_add_negative_numbers(self, tools):
        assert tools["add"](-5, -3) == -8

    def test_add_large_numbers(self, tools):
        assert tools["add"](1e308, 1e308) is not None

    def test_add_none_raises_type_error(self, tools):
        with pytest.raises(TypeError):
            tools["add"](None, 5)

    def test_add_wrong_type_raises_type_error(self, tools):
        with pytest.raises(TypeError):
            tools["add"]("a", 5)


class TestMultiplyCoreLogic:
    def test_multiply_two_numbers(self, tools):
        assert tools["multiply"](4, 5) == 20

    def test_multiply_by_zero(self, tools):
        assert tools["multiply"](0, 5) == 0

    def test_multiply_decimals(self, tools):
        assert tools["multiply"](2.5, 4.2) == 10.5

    def test_multiply_negative_numbers(self, tools):
        assert tools["multiply"](-8, 7) == -56


class TestToolSchema:
    """Docs-vs-behavior: the schema the model sees matches each function."""

    @pytest.mark.parametrize(
        "name,description",
        [
            ("add", "Add two numbers and return their sum."),
            ("multiply", "Multiply two numbers and return their product."),
        ],
    )
    def test_schema_name_and_description(self, tools, name, description):
        schema = convert_to_openai_tool(tools[name])["function"]
        assert schema["name"] == name
        assert schema["description"] == description

    @pytest.mark.parametrize("name", ["add", "multiply"])
    def test_schema_parameters(self, tools, name):
        parameters = convert_to_openai_tool(tools[name])["function"]["parameters"]
        assert parameters["type"] == "object"
        assert parameters["properties"]["a"] == {"type": "number"}
        assert parameters["properties"]["b"] == {"type": "number"}
        assert parameters["required"] == ["a", "b"]


class TestMessageTypes:
    """Output structure: each message object carries the right type and content."""

    @pytest.fixture(scope="class")
    def messages(self):
        return run_cell("tool_call_id")

    def test_system_message(self, messages):
        assert messages["system_message"].type == "system"
        assert messages["system_message"].content == "You are a math helper."

    def test_human_message(self, messages):
        assert messages["human_message"].type == "human"
        assert messages["human_message"].content == "What is 8 + 7?"

    def test_ai_message(self, messages):
        assert messages["ai_message"].type == "ai"
        assert messages["ai_message"].content == "I'll compute that with a tool."

    def test_tool_message(self, messages):
        assert messages["tool_message"].type == "tool"
        assert messages["tool_message"].content == "15"
        assert messages["tool_message"].tool_call_id == "call_1"


class TestChatHistory:
    """A conversation is a list of messages, oldest first."""

    def test_history_is_list_of_messages(self):
        namespace = {}
        exec(cell_source("tool_call_id"), namespace)  # Step 3 imports the message classes
        exec(cell_source("traffic light"), namespace)  # Step 4 builds the history list
        types = [m.type for m in namespace["history"]]
        assert types == ["system", "human", "ai", "human"]


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
        packages = [tok.strip('"') for tok in pip_lines[0].split()[2:] if not tok.startswith("-")]
        assert packages, "install line lists at least one module"
        assert all("==" in pkg for pkg in packages), "every module must be pinned"
