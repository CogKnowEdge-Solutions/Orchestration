"""Test case data for Lab 10: Multi-Agent Coordination — Orchestrator-Worker Routing.

Format: (id, description, expected_result, actual_result)
All tests from test_lab10.py (26 total).
"""

ROWS = [
    ("1.1", "First code cell is single pinned pip install",
     "Exactly one !pip install with all packages pinned (==)",
     "PASS: First cell verified as pinned pip install"),

    ("1.2", "Code line count within advanced ceiling (180 lines)",
     "Total code cells ≤ 180 lines",
     "PASS: Code cells verified within 180-line limit"),

    ("1.3", "Companion files exist",
     "lab-multi-agent-coordination.ipynb, .md, and -assignment.md all present",
     "PASS: All companion files verified"),

    ("2.1", "Model factory uses free Nemotron on OpenRouter",
     "model_name='nvidia/nemotron-3-super-120b-a12b:free', openai_api_base='https://openrouter.ai/api/v1'",
     "PASS: Model factory uses correct endpoint and model"),

    ("2.2", "API key read from environment",
     "model().openai_api_key is not None",
     "PASS: API key loaded from .env"),

    ("3.1", "UsageCapture starts empty",
     "capture.calls == []",
     "PASS: UsageCapture initialized empty"),

    ("3.2", "UsageCapture records prompt tokens on end",
     "capture.calls contains token counts after on_llm_end",
     "PASS: Token recording verified"),

    ("4.1", "get_invoice tool returns expected message",
     "Contains 'Invoice #INV-2214: $99.00' and duplicate charge mention",
     "PASS: get_invoice tool verified"),

    ("4.2", "process_refund tool returns refund confirmation",
     "Contains 'Refund of $99.00'",
     "PASS: process_refund tool verified"),

    ("4.3", "check_service_status tool returns status",
     "Contains 'HTTP 503'",
     "PASS: check_service_status tool verified"),

    ("4.4", "search_kb tool finds articles",
     "Contains 'KB-301'",
     "PASS: search_kb tool verified"),

    ("4.5", "get_plan tool returns plan info",
     "Contains 'Team (10 seats)'",
     "PASS: get_plan tool verified"),

    ("4.6", "set_seats tool updates seat count",
     "Contains '12 seats'",
     "PASS: set_seats tool verified"),

    ("4.7", "ALL_TOOLS lists all six tools",
     "Tool names: [get_invoice, process_refund, check_service_status, search_kb, get_plan, set_seats]",
     "PASS: All six tools verified in ALL_TOOLS"),

    ("5.1", "route_billing tool returns correct route",
     "route_billing() == 'routed to billing'",
     "PASS: route_billing tool verified"),

    ("5.2", "route_tech tool returns correct route",
     "route_tech() == 'routed to tech'",
     "PASS: route_tech tool verified"),

    ("5.3", "route_account tool returns correct route",
     "route_account() == 'routed to account'",
     "PASS: route_account tool verified"),

    ("5.4", "Route tool names map to nodes",
     "ROUTE_TO_NODE == {route_billing: billing, route_tech: tech, route_account: account}",
     "PASS: Route-to-node mapping verified"),

    ("5.5", "Supervisor prompt covers all departments",
     "SUPERVISOR_PROMPT contains Billing, Tech, Account",
     "PASS: Supervisor prompt covers all departments"),

    ("6.1", "Desk compiles offline with four nodes",
     "desk.nodes contains {supervisor, billing, tech, account}",
     "PASS: Graph compiles with four nodes"),

    ("6.2", "RoutingState uses add_messages",
     "messages field is Annotated[list, add_messages]",
     "PASS: RoutingState uses add_messages correctly"),

    ("7.1", "transfer_to_tech returns parent command",
     "cmd.goto='tech', cmd.graph=Command.PARENT",
     "PASS: transfer_to_tech returns correct command"),

    ("7.2", "transfer_to_billing returns parent command",
     "cmd.goto='billing', cmd.graph=Command.PARENT",
     "PASS: transfer_to_billing returns correct command"),

    ("7.3", "Handoff budget blocks second transfer",
     "First transfer succeeds, second returns 'already transferred' message",
     "PASS: Handoff budget guard verified"),

    ("11.1", "Optional exercise targets fourth department",
     "MD contains 'security', 'route_security', 'review_account_access'",
     "PASS: Optional exercise documentation verified"),

    ("12.1-12.2", "MD has all twelve sections and mermaid diagrams",
     "All 12 section headers present, ≥2 mermaid diagrams",
     "PASS: Documentation structure complete"),
]
