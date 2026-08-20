"""
Test file for Lab 4: Prompt Playground & Prompt Hub

Run with: pytest test_prompt_playground_prompt_hub.py -v
"""
import os
import pytest
from unittest.mock import patch, MagicMock


class TestEnvironmentSetup:
    """Tests for environment and client initialization."""

    def test_openrouter_key_exists(self):
        """OPENROUTER_API_KEY must be set for LLM calls."""
        from dotenv import load_dotenv
        load_dotenv()
        assert os.getenv("OPENROUTER_API_KEY"), "OPENROUTER_API_KEY not found in environment"

    def test_langsmith_key_exists(self):
        """LANGSMITH_API_KEY must be set for Hub operations."""
        from dotenv import load_dotenv
        load_dotenv()
        assert os.getenv("LANGSMITH_API_KEY"), "LANGSMITH_API_KEY not found in environment"

    def test_tracing_enabled(self):
        """LANGSMITH_TRACING should be set to true."""
        from dotenv import load_dotenv
        load_dotenv()
        tracing = os.getenv("LANGSMITH_TRACING")
        assert tracing == "true", f"LANGSMITH_TRACING should be 'true', got '{tracing}'"


class TestPromptCreation:
    """Tests for creating ChatPromptTemplate objects."""

    def test_prompt_has_system_and_user_messages(self):
        """A tool-selector prompt needs both system and user messages."""
        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("user", "{query}")
        ])
        assert len(prompt.messages) == 2
        assert prompt.messages[0].type == "system"
        assert prompt.messages[1].type == "user"

    def test_prompt_has_input_variable(self):
        """The prompt must accept a {query} variable."""
        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Route queries to tools."),
            ("user", "{query}")
        ])
        assert "query" in prompt.input_variables

    def test_prompt_invokes_with_variable(self):
        """Invoking the prompt fills in the variable."""
        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a tool-router."),
            ("user", "{query}")
        ])
        formatted = prompt.invoke({"query": "What is 2+2?"})
        assert len(formatted.messages) == 2
        assert "2+2" in formatted.messages[1].content

    def test_refined_prompt_has_format_instruction(self):
        """The refined prompt should specify an output format."""
        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Respond with Tool: [name] | Reason: [why]"),
            ("user", "{query}")
        ])
        assert "Tool:" in prompt.messages[0].content
        assert "Reason:" in prompt.messages[0].content


class TestPromptHubOperations:
    """Tests for push, pull, and list operations."""

    def test_push_prompt_returns_url(self):
        """push_prompt() should return a URL string."""
        mock_client = MagicMock()
        mock_client.push_prompt.return_value = "https://smith.langchain.com/prompts/test"
        url = mock_client.push_prompt("test-prompt", object=MagicMock())
        assert url.startswith("https://")

    def test_pull_prompt_returns_template(self):
        """pull_prompt() should return a ChatPromptTemplate."""
        from langchain_core.prompts import ChatPromptTemplate
        mock_client = MagicMock()
        expected = ChatPromptTemplate.from_messages([
            ("system", "Test"), ("user", "{query}")
        ])
        mock_client.pull_prompt.return_value = expected
        pulled = mock_client.pull_prompt("test-prompt")
        assert isinstance(pulled, ChatPromptTemplate)

    def test_pull_prompt_with_version(self):
        """pull_prompt() with :2 suffix pulls version 2."""
        mock_client = MagicMock()
        mock_client.pull_prompt.return_value = MagicMock()
        mock_client.pull_prompt("my-prompt:2")
        mock_client.pull_prompt.assert_called_with("my-prompt:2")

    def test_list_prompts_returns_iterable(self):
        """list_prompts() should return an iterable of prompts."""
        mock_client = MagicMock()
        mock_prompt = MagicMock()
        mock_prompt.repo_handle = "test-prompt"
        mock_client.list_prompts.return_value = [mock_prompt]
        prompts = list(mock_client.list_prompts(limit=10))
        assert len(prompts) == 1
        assert prompts[0].repo_handle == "test-prompt"


class TestVersioning:
    """Tests for prompt versioning concepts."""

    def test_same_name_creates_new_version(self):
        """Pushing the same name twice creates version 1 and 2."""
        mock_client = MagicMock()
        mock_client.push_prompt.side_effect = [
            "https://example.com/v1",
            "https://example.com/v2"
        ]
        v1 = mock_client.push_prompt("my-prompt", object=MagicMock())
        v2 = mock_client.push_prompt("my-prompt", object=MagicMock())
        assert v1 != v2
        assert mock_client.push_prompt.call_count == 2

    def test_pull_without_version_returns_latest(self):
        """Pulling without a version suffix returns the latest."""
        mock_client = MagicMock()
        mock_client.pull_prompt.return_value = MagicMock()
        mock_client.pull_prompt("my-prompt")
        mock_client.pull_prompt.assert_called_with("my-prompt")

    def test_version_pinning_prevents_breakage(self):
        """Pinning to a specific version ensures stable behavior."""
        versions = {"1": "old prompt", "2": "new prompt"}
        pinned_version = "1"
        assert versions[pinned_version] == "old prompt"


class TestLLMIntegration:
    """Tests for formatting messages and sending to LLM."""

    def test_format_messages_for_openai(self):
        """Formatted messages must use role/content dict format for OpenAI."""
        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Be helpful."), ("user", "{query}")
        ])
        formatted = prompt.invoke({"query": "Hello"})
        openai_msgs = [{"role": m.type, "content": m.content} for m in formatted.messages]
        assert len(openai_msgs) == 2
        assert openai_msgs[0]["role"] == "system"
        assert openai_msgs[1]["role"] == "user"

    def test_openai_client_uses_openrouter(self):
        """OpenAI client must point to OpenRouter for free tier."""
        from openai import OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="test-key"
        )
        assert "openrouter.ai" in client.base_url


class TestFewShotPrompts:
    """Tests for few-shot prompt concepts."""

    def test_few_shot_includes_examples(self):
        """A few-shot prompt contains example input/output pairs."""
        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Route queries to tools."),
            ("user", "What is 2+2?"),
            ("assistant", "Tool: calculator | Reason: math query"),
            ("user", "{query}")
        ])
        # 1 system + 1 example user + 1 example assistant + 1 actual user = 4
        assert len(prompt.messages) == 4

    def test_few_shot_learns_format(self):
        """Few-shot examples teach the model the expected output format."""
        examples = [
            {"input": "What is 5+3?", "output": "Tool: calculator | Reason: math"},
            {"input": "Search for cats", "output": "Tool: search | Reason: web query"},
        ]
        assert len(examples) == 2
        assert "Tool:" in examples[0]["output"]
        assert "Tool:" in examples[1]["output"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
