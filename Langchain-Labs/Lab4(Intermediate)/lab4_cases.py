"""Test case data for Lab 4 Assignment: Short-Term Memory & Streaming.

Format: (id, description, expected_result, actual_result)
All tests from test_lab4.py (10 total).
"""

ROWS = [
    ("1.1", "prompt has history placeholder",
     "Test passes with correct implementation",
     "PASS: test_prompt_has_history_placeholder verified"),

    ("2.1", "prompt has system and human",
     "Test passes with correct implementation",
     "PASS: test_prompt_has_system_and_human verified"),

    ("3.1", "store returns same history per session",
     "Test passes with correct implementation",
     "PASS: test_store_returns_same_history_per_session verified"),

    ("4.1", "chat is wrapped with message history",
     "Test passes with correct implementation",
     "PASS: test_chat_is_wrapped_with_message_history verified"),

    ("5.1", "message keys match prompt",
     "Test passes with correct implementation",
     "PASS: test_message_keys_match_prompt verified"),

    ("6.1", "streams bare model",
     "Test passes with correct implementation",
     "PASS: test_streams_bare_model verified"),

    ("7.1", "streams through wrapped chat",
     "Test passes with correct implementation",
     "PASS: test_streams_through_wrapped_chat verified"),

    ("8.1", "cog history survives restart",
     "Test passes with correct implementation",
     "PASS: test_cog_history_survives_restart verified"),

    ("9.1", "restored messages match original",
     "Test passes with correct implementation",
     "PASS: test_restored_messages_match_original verified"),

    ("10.1", "first code cell is single pinned pip install",
     "Test passes with correct implementation",
     "PASS: test_first_code_cell_is_single_pinned_pip_install verified"),

]