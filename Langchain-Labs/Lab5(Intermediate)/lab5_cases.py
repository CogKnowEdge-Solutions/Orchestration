"""Test case data for Lab 5 Assignment: Agent Middleware.

Format: (id, description, expected_result, actual_result)
All tests from test_lab5.py (17 total).
"""

ROWS = [
    ("1.1", "first code cell is single pinned pip install",
     "Test passes with correct implementation",
     "PASS: test_first_code_cell_is_single_pinned_pip_install verified"),

    ("2.1", "agent created",
     "Test passes with correct implementation",
     "PASS: test_agent_created verified"),

    ("3.1", "agent uses no middleware",
     "Test passes with correct implementation",
     "PASS: test_agent_uses_no_middleware verified"),

    ("4.1", "redact scrubs email from input",
     "Test passes with correct implementation",
     "PASS: test_redact_scrubs_email_from_input verified"),

    ("5.1", "redact leaves clean input untouched",
     "Test passes with correct implementation",
     "PASS: test_redact_leaves_clean_input_untouched verified"),

    ("6.1", "block raises before any call",
     "Test passes with correct implementation",
     "PASS: test_block_raises_before_any_call verified"),

    ("7.1", "both pii agents built",
     "Test passes with correct implementation",
     "PASS: test_both_pii_agents_built verified"),

    ("8.1", "at limit jumps to end",
     "Test passes with correct implementation",
     "PASS: test_at_limit_jumps_to_end verified"),

    ("9.1", "under limit allows call",
     "Test passes with correct implementation",
     "PASS: test_under_limit_allows_call verified"),

    ("10.1", "budget agent has weather tool",
     "Test passes with correct implementation",
     "PASS: test_budget_agent_has_weather_tool verified"),

    ("11.1", "logging middleware is agent middleware",
     "Test passes with correct implementation",
     "PASS: test_logging_middleware_is_agent_middleware verified"),

    ("12.1", "timing wrap returns model response",
     "Test passes with correct implementation",
     "PASS: test_timing_wrap_returns_model_response verified"),

    ("13.1", "decorators produce middleware instances",
     "Test passes with correct implementation",
     "PASS: test_decorators_produce_middleware_instances verified"),

    ("14.1", "custom agents created",
     "Test passes with correct implementation",
     "PASS: test_custom_agents_created verified"),

    ("15.1", "stacked agent created",
     "Test passes with correct implementation",
     "PASS: test_stacked_agent_created verified"),

    ("16.1", "notebook stacks three middleware kinds",
     "Test passes with correct implementation",
     "PASS: test_notebook_stacks_three_middleware_kinds verified"),

    ("17.1", "hook execution order",
     "Test passes with correct implementation",
     "PASS: test_hook_execution_order verified"),

]