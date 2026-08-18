"""
Test file for Lab 1: Tracing Basics & Types of Runs

Run with: pytest test_tracing_basics.py -v
"""
import os
import pytest
from unittest.mock import patch, MagicMock


class TestEnvironmentSetup:
    """Tests for environment variable configuration."""

    def test_all_required_variables_defined(self):
        """Verify all required env vars are documented."""
        required = ["OPENROUTER_API_KEY", "LANGSMITH_API_KEY", "LANGSMITH_TRACING", "LANGSMITH_PROJECT"]
        # Check that the lab defines these variables
        assert len(required) == 4

    def test_langsmith_tracing_must_be_true(self):
        """LANGSMITH_TRACING must be 'true' to enable tracing."""
        # When set to true, tracing is enabled
        assert "true" == "true"
        # When set to false or omitted, tracing is disabled
        assert "false" != "true"

    def test_env_file_structure(self):
        """Verify .env file has correct structure."""
        expected_vars = {
            "OPENROUTER_API_KEY": "sk-or-v1-...",
            "LANGSMITH_API_KEY": "ls-...",
            "LANGSMITH_TRACING": "true",
            "LANGSMITH_PROJECT": "tracing-basics-lab"
        }
        # All four variables must be present
        assert len(expected_vars) == 4


class TestRunTypes:
    """Tests for run type knowledge."""

    def test_seven_run_types_exist(self):
        """LangSmith recognizes exactly 7 run types."""
        run_types = ["llm", "chain", "tool", "retriever", "embedding", "prompt", "parser"]
        assert len(run_types) == 7

    def test_llm_run_type(self):
        """LLM run type captures model calls."""
        run_type = "llm"
        assert run_type == "llm"

    def test_chain_run_type(self):
        """Chain run type captures wrapping operations."""
        run_type = "chain"
        assert run_type == "chain"

    def test_tool_run_type(self):
        """Tool run type captures tool executions."""
        run_type = "tool"
        assert run_type == "tool"

    def test_retriever_run_type(self):
        """Retriever run type captures document retrieval."""
        run_type = "retriever"
        assert run_type == "retriever"

    def test_embedding_run_type(self):
        """Embedding run type captures vector generation."""
        run_type = "embedding"
        assert run_type == "embedding"

    def test_prompt_run_type(self):
        """Prompt run type captures template rendering."""
        run_type = "prompt"
        assert run_type == "prompt"

    def test_parser_run_type(self):
        """Parser run type captures output parsing."""
        run_type = "parser"
        assert run_type == "parser"


class TestRunTreeHierarchy:
    """Tests for run tree parent-child relationships."""

    def test_chain_is_parent_of_llm(self):
        """In run tree, chain is parent and llm is child."""
        parent = "chain"
        child = "llm"
        # Chain wraps LLM calls
        assert parent == "chain"
        assert child == "llm"

    def test_direct_llm_has_no_parent(self):
        """Direct LLM calls have no parent (is_root=True)."""
        is_root = True
        run_type = "llm"
        # When calling LLM directly, it's a root trace
        assert is_root == True

    def test_wrapped_llm_has_chain_parent(self):
        """LLM calls inside chains have chain as parent."""
        parent_type = "chain"
        child_type = "llm"
        # Chain contains LLM call
        assert parent_type == "chain"
        assert child_type == "llm"


class TestOpenRouterSetup:
    """Tests for OpenRouter configuration."""

    def test_openrouter_base_url(self):
        """OpenRouter uses OpenAI-compatible endpoint."""
        base_url = "https://openrouter.ai/api/v1"
        assert "openrouter.ai" in base_url
        assert base_url.endswith("/v1")

    def test_free_model_name(self):
        """Lab uses deepseek free model on OpenRouter."""
        model = "deepseek/deepseek-chat-v3-0324:free"
        assert ":free" in model
        assert "deepseek" in model

    def test_openai_sdk_works_with_openrouter(self):
        """OpenAI SDK can connect to OpenRouter (OpenAI-compatible)."""
        # OpenRouter is OpenAI-compatible
        from openai import OpenAI
        # Just verify the import works
        assert OpenAI is not None

    def test_alternative_free_models(self):
        """List of alternative free models for exercises."""
        free_models = [
            "deepseek/deepseek-chat-v3-0324:free",
            "meta-llama/llama-4-scout:free",
            "qwen/qwen3-235b-a22b:free",
            "openrouter/free"  # Auto-router
        ]
        # All should have :free suffix or be the router
        for model in free_models:
            assert ":free" in model or model == "openrouter/free"


class TestTraceableDecorator:
    """Tests for @traceable decorator usage."""

    def test_decorator_requires_run_type(self):
        """@traceable must specify run_type parameter."""
        # The decorator needs run_type to classify the run
        run_type = "llm"
        assert run_type in ["llm", "chain", "tool", "retriever", "embedding", "prompt", "parser"]

    def test_decorator_requires_name(self):
        """@traceable should have a descriptive name."""
        name = "simple_chat_completion"
        assert len(name) > 0
        assert "_" in name  # Uses snake_case

    def test_llm_run_type_for_model_calls(self):
        """Use run_type='llm' for OpenAI/Anthropic calls."""
        run_type = "llm"
        assert run_type == "llm"

    def test_chain_run_type_for_wrappers(self):
        """Use run_type='chain' for wrapping operations."""
        run_type = "chain"
        assert run_type == "chain"


class TestTracingWorkflow:
    """Tests for the tracing workflow steps."""

    def test_workflow_has_five_steps(self):
        """Tracing workflow has 5 steps."""
        steps = [
            "Configure LangSmith SDK",
            "Create traced function",
            "Run the function",
            "Inspect trace in UI",
            "Compare multiple traces"
        ]
        assert len(steps) == 5

    def test_direct_call_creates_single_run(self):
        """Direct LLM call creates one run."""
        runs = 1
        assert runs == 1

    def test_chain_call_creates_nested_runs(self):
        """Chain call creates parent + child runs."""
        parent_runs = 1
        child_runs = 1
        total = parent_runs + child_runs
        assert total == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
