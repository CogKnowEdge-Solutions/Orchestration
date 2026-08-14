"""Test case data for Lab 12: Capstone Project — Intelligent Customer Support Platform.

Format: (id, description, expected_result, actual_result)
All tests from test_lab12.py (capstone integration validation).
"""

ROWS = [
    ("1.1", "Notebook exists and loads correctly",
     "lab-capstone-project.ipynb found and valid JSON",
     "PASS: Notebook file verified"),

    ("1.2", "First code cell is single pinned pip install",
     "Exactly one !pip install with pinned versions",
     "PASS: Pinned dependencies verified"),

    ("1.3", "Code line count within capstone ceiling (200 lines)",
     "Total code cells ≤ 200 lines",
     "PASS: Code size verified"),

    ("1.4", "Code cells between 10 and 12",
     "10 ≤ cell count ≤ 12",
     "PASS: Cell count verified"),

    ("1.5", "Companion files exist",
     "lab-capstone-project.md, -assignment.md, test_lab12.py all present",
     "PASS: Companion files verified"),

    ("2.1", "Model factory uses free Nemotron on OpenRouter",
     "Model name contains 'nemotron', uses 'openrouter'",
     "PASS: Model configuration verified"),

    ("2.2", "API key loaded from environment",
     "OPENROUTER_API_KEY present in notebook",
     "PASS: API key loading verified"),

    ("3.1", "Markdown has all twelve sections",
     "All sections 1-12 present (Title through What We Learnt)",
     "PASS: All sections verified"),

    ("3.2", "Markdown mentions all 11 prior labs",
     "Lab 1 through Lab 11 referenced in documentation",
     "PASS: All labs referenced"),

    ("3.3", "Markdown includes mermaid diagrams",
     "≥2 mermaid diagram blocks",
     "PASS: Diagrams verified"),

    ("3.4", "Cost and quota disclosed",
     "OpenRouter calls mentioned (~25 calls)",
     "PASS: Cost disclosure verified"),

    ("4.1", "Routing system implemented",
     "Supervisor + 4 departments (Billing, Tech, Account, Security)",
     "PASS: Routing architecture verified"),

    ("4.2", "Multi-agent routing uses Command",
     "Supervisor returns Command(goto=...) based on route tools",
     "PASS: Command-based routing verified"),

    ("5.1", "Long-term memory implemented",
     "load_memory dossier + remember tool + InMemoryStore",
     "PASS: Memory system verified"),

    ("5.2", "Customer memory isolation",
     "Two customer profiles with separate namespaces",
     "PASS: Memory isolation verified"),

    ("6.1", "Knowledge base retrieval implemented",
     "10+ documents, overlap-based ranking, top-2 injection",
     "PASS: Retrieval system verified"),

    ("6.2", "Retrieval scores by word overlap",
     "recall_score pattern from Lab 11 used",
     "PASS: Overlap scoring verified"),

    ("7.1", "Support tools defined",
     "≥6 tools: Billing (2), Tech (2), Account (2), Security (2+)",
     "PASS: Tool definitions verified"),

    ("8.1", "Handoff escalation implemented",
     "transfer_to_* tools with Command(graph=Command.PARENT)",
     "PASS: Handoff mechanics verified"),

    ("8.2", "Handoff budget guard prevents runaway",
     "One handoff per ticket, second attempt blocked",
     "PASS: Budget guard verified"),

    ("9.1", "Token budgeting implemented",
     "UsageCapture callback, per-decision tracking, ledger",
     "PASS: Token tracking verified"),

    ("10.1", "Graph wiring complete",
     "StateGraph + MemorySaver + store + Runtime[Guest]",
     "PASS: Graph wiring verified"),

    ("11.1", "Assignment document complete",
     "Deliverables, rubric, grading, success criteria",
     "PASS: Assignment verified"),

    ("11.2", "Assignment mentions optional exercise",
     "Sentiment analysis or extension mentioned",
     "PASS: Optional exercise documented"),

    ("12.1", "All prior labs integrated",
     "Labs 1-11 concepts visible in implementation",
     "PASS: Full integration verified"),
]
