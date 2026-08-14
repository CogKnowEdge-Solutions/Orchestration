"""Test case data for Lab 6 Assignment: Human-in-the-Loop & Guardrails.

Format: (id, description, expected_result, actual_result)
All tests from test_lab6.py (20 total).
"""

ROWS = [
    ("1.1", "first code cell is single pinned pip install",
     "Test passes with correct implementation",
     "PASS: test_first_code_cell_is_single_pinned_pip_install verified"),

    ("2.1", "bare agent created",
     "Test passes with correct implementation",
     "PASS: test_bare_agent_created verified"),

    ("3.1", "bare agent has no middleware",
     "Test passes with correct implementation",
     "PASS: test_bare_agent_has_no_middleware verified"),

    ("4.1", "both tools defined",
     "Test passes with correct implementation",
     "PASS: test_both_tools_defined verified"),

    ("5.1", "guard is agent middleware",
     "Test passes with correct implementation",
     "PASS: test_guard_is_agent_middleware verified"),

    ("6.1", "injection input jumps to end with refusal",
     "Test passes with correct implementation",
     "PASS: test_injection_input_jumps_to_end_with_refusal verified"),

    ("7.1", "clean input passes through",
     "Test passes with correct implementation",
     "PASS: test_clean_input_passes_through verified"),

    ("8.1", "phrase list configured",
     "Test passes with correct implementation",
     "PASS: test_phrase_list_configured verified"),

    ("9.1", "allowlist is agent middleware",
     "Test passes with correct implementation",
     "PASS: test_allowlist_is_agent_middleware verified"),

    ("10.1", "allowlist filters out disallowed tool",
     "Test passes with correct implementation",
     "PASS: test_allowlist_filters_out_disallowed_tool verified"),

    ("11.1", "allowlist keeps allowed tool available",
     "Test passes with correct implementation",
     "PASS: test_allowlist_keeps_allowed_tool_available verified"),

    ("12.1", "readonly prompt never names the hidden tool",
     "Test passes with correct implementation",
     "PASS: test_readonly_prompt_never_names_the_hidden_tool verified"),

    ("13.1", "readonly agent uses readonly prompt",
     "Test passes with correct implementation",
     "PASS: test_readonly_agent_uses_readonly_prompt verified"),

    ("14.1", "hitl agent created",
     "Test passes with correct implementation",
     "PASS: test_hitl_agent_created verified"),

    ("15.1", "hitl agent has checkpointer",
     "Test passes with correct implementation",
     "PASS: test_hitl_agent_has_checkpointer verified"),

    ("16.1", "interrupt configured for transfer only",
     "Test passes with correct implementation",
     "PASS: test_interrupt_configured_for_transfer_only verified"),

    ("17.1", "resume payloads use decisions list",
     "Test passes with correct implementation",
     "PASS: test_resume_payloads_use_decisions_list verified"),

    ("18.1", "resume decisions come from interactive prompt",
     "Test passes with correct implementation",
     "PASS: test_resume_decisions_come_from_interactive_prompt verified"),

    ("19.1", "all control build blocks present",
     "Test passes with correct implementation",
     "PASS: test_all_control_build_blocks_present verified"),

    ("20.1", "injection guard and allowlist compose with hitl",
     "Test passes with correct implementation",
     "PASS: test_injection_guard_and_allowlist_compose_with_hitl verified"),

]