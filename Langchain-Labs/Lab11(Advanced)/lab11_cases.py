"""Test case data for Lab 11: Long-Term Memory — the Maitre d'.

Format: (id, description, expected_result, actual_result)
All tests from test_lab11.py (21 total).
"""

ROWS = [
    ("1.1", "First code cell is single pinned pip install",
     "Exactly one !pip install with all packages pinned (==)",
     "PASS: First cell verified as pinned pip install"),

    ("1.2", "Code line count within advanced ceiling (180 lines)",
     "Total code cells ≤ 180 lines",
     "PASS: Code cells verified within 180-line limit"),

    ("1.3", "Companion files exist",
     "lab-long-term-memory.ipynb, .md, and -assignment.md all present",
     "PASS: All companion files verified"),

    ("2.1", "Model factory uses free Nemotron on OpenRouter",
     "model_name='nvidia/nemotron-3-super-120b-a12b:free', openai_api_base='https://openrouter.ai/api/v1'",
     "PASS: Model factory uses correct endpoint and model"),

    ("2.2", "API key read from environment",
     "model().openai_api_key is not None",
     "PASS: API key loaded from .env"),

    ("3.1", "UsageCapture records prompt tokens",
     "capture.calls initialized as empty list",
     "PASS: UsageCapture initialized correctly"),

    ("3.2", "Ledger uses prompt_tokens in documentation",
     "MD contains 'prompt_tokens' and 'decision-time tokens per chef call'",
     "PASS: Documentation references token usage"),

    ("4.1", "check_pantry tool: ingredient in stock",
     "check_pantry('saffron') == \"'saffron' is in stock\"",
     "PASS: check_pantry returns stock confirmation"),

    ("4.2", "check_pantry tool: ingredient out of stock",
     "check_pantry('truffle') contains 'out of stock'",
     "PASS: check_pantry returns stock-out message"),

    ("4.3", "remember tool writes to namespace",
     "remember.func('Amara loves tiramisu.') == 'Remembered as fact 1.'",
     "PASS: remember tool writes fact to store"),

    ("5.1", "Guests have separate namespaces",
     "Amara and Bob facts isolated in separate ('guests', guest_id, 'facts') namespaces",
     "PASS: Guest namespaces are isolated"),

    ("6.1", "Overlap scorer counts long words only",
     "score(birthday_query, 'birthday is October 14') >= 1",
     "PASS: Overlap scoring works for long words"),

    ("6.2", "Two-letter words are ignored in scoring",
     "score('it is', 'it is a fact') == 0",
     "PASS: Short words excluded from scoring"),

    ("7.1", "Empty profile builds first visit dossier",
     "load_memory for new guest produces 'first visit' dossier",
     "PASS: First-visit dossier generated"),

    ("7.2", "Dossier includes stored facts",
     "load_memory appends stored facts to system message",
     "PASS: Stored facts appear in dossier"),

    ("7.3", "Recall line appears for matching query",
     "load_memory for birthday query appends recall line with matching fact",
     "PASS: Recall matching verified"),

    ("8.1", "Graph compiles with checkpointer and store",
     "StateGraph with context_schema=Guest, checkpointer=MemorySaver(), store=store",
     "PASS: Graph wiring verified"),

    ("8.2", "Namespace tuple used in put and search",
     "Graph uses ('guests', guest_id, 'facts') namespace pattern",
     "PASS: Namespace pattern verified"),

    ("11.1", "Optional exercise targets second namespace",
     "MD contains ('guests', guest_id, 'drinks'), 'remember_drink', 'Barolo'",
     "PASS: Optional exercise documentation verified"),

    ("12.1-12.2", "MD has all twelve sections and mermaid diagrams",
     "All 12 section headers present, ≥2 mermaid diagrams",
     "PASS: Documentation structure complete"),

    ("12.3", "MD pins versions and discloses cost",
     "MD contains version pins and '15 OpenRouter calls'",
     "PASS: Version pins and cost disclosure verified"),
]
