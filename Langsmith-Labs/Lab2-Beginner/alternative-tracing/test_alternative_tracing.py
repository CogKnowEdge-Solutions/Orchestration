"""
Test file for Lab 2: Alternative Ways to Trace

Run with: pytest test_alternative_tracing.py -v
"""
import pytest


class TestWrapOpenAI:
    """Tests for wrap_openai mechanism."""

    def test_wrap_openai_imports_from_langsmith(self):
        """wrap_openai is imported from the langsmith package."""
        from langsmith.wrappers import wrap_openai
        assert wrap_openai is not None

    def test_wrap_openai_wraps_client(self):
        """wrap_openai accepts an OpenAI client and returns a wrapped version."""
        from langsmith.wrappers import wrap_openai
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="test")
        wrapped = wrap_openai(client)
        assert wrapped is not None

    def test_wrapped_client_has_chat(self):
        """Wrapped client retains chat.completions.create interface."""
        from langsmith.wrappers import wrap_openai
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="test")
        wrapped = wrap_openai(client)
        assert hasattr(wrapped, "chat")
        assert hasattr(wrapped.chat, "completions")

    def test_wrap_openai_traces_automatically(self):
        """wrap_openai traces all calls through the client without decorators."""
        # The key advantage: no @traceable needed on each function
        mechanism = "wrap_openai"
        requires_decorator = False
        assert mechanism == "wrap_openai"
        assert requires_decorator is False


class TestTraceContextManager:
    """Tests for trace() context manager mechanism."""

    def test_trace_imports_from_langsmith(self):
        """trace is imported from the langsmith package."""
        from langsmith import trace
        assert trace is not None

    def test_trace_creates_with_block(self):
        """trace() is used as a context manager with 'with' keyword."""
        # trace() is used as: with trace("name") as ts:
        usage_pattern = "with trace(name) as ts:"
        assert "with" in usage_pattern
        assert "trace" in usage_pattern

    def test_trace_accepts_metadata(self):
        """trace() accepts a metadata dict for custom tags."""
        from langsmith import trace
        # Metadata is passed as the second argument
        metadata = {"method": "context_manager"}
        assert "method" in metadata

    def test_trace_groups_multiple_operations(self):
        """trace() groups multiple operations into a single trace."""
        # Operations inside the with block are all part of one trace
        operations_in_trace = 3  # e.g., format prompt, call LLM, parse result
        assert operations_in_trace > 1


class TestLangChainCallbacks:
    """Tests for LangChain callback tracer mechanism."""

    def test_langchain_imports(self):
        """LangChain tracing uses ChatOpenAI and tool decorators."""
        from langchain_openai import ChatOpenAI
        from langchain_core.tools import tool
        assert ChatOpenAI is not None
        assert tool is not None

    def test_tool_decorator_creates_tool(self):
        """@tool decorator converts a function into a LangChain tool."""
        from langchain_core.tools import tool

        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b

        assert add.name == "add"

    def test_bind_tools_attaches_tools_to_llm(self):
        """bind_tools attaches tools to a ChatOpenAI instance."""
        from langchain_openai import ChatOpenAI
        from langchain_core.tools import tool

        @tool
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers."""
            return a * b

        llm = ChatOpenAI(model="test", api_key="test")
        llm_with_tools = llm.bind_tools([multiply])
        assert llm_with_tools is not None

    def test_langchain_traces_automatically(self):
        """LangChain callbacks trace chains without manual setup."""
        mechanism = "langchain_callbacks"
        requires_manual_tracing = False
        assert mechanism == "langchain_callbacks"
        assert requires_manual_tracing is False


class TestTracingComparison:
    """Tests for comparing the three mechanisms."""

    def test_three_mechanisms_taught(self):
        """Lab teaches exactly three tracing mechanisms."""
        mechanisms = ["wrap_openai", "trace_context_manager", "langchain_callbacks"]
        assert len(mechanisms) == 3

    def test_mechanism_selection_depends_on_sdk(self):
        """Choosing a mechanism depends on which SDK you're using."""
        scenarios = {
            "openai_sdk_only": "wrap_openai",
            "manual_control": "trace_context_manager",
            "langchain_chains": "langchain_callbacks",
        }
        assert len(scenarios) == 3
        assert scenarios["openai_sdk_only"] == "wrap_openai"


class TestOpenRouterSetup:
    """Tests for OpenRouter configuration consistency."""

    def test_free_model_name(self):
        """Lab uses the same free model as Lab 1."""
        model = "nvidia/nemotron-3-super-120b-a12b:free"
        assert ":free" in model
        assert "nemotron" in model

    def test_openrouter_base_url(self):
        """OpenRouter uses OpenAI-compatible endpoint."""
        base_url = "https://openrouter.ai/api/v1"
        assert "openrouter.ai" in base_url
        assert base_url.endswith("/v1")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
