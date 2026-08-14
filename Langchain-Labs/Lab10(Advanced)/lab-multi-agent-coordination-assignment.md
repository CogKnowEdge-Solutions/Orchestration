# Lab 10 Assignment — Multi-Agent Coordination

Test what you learned from `lab-multi-agent-coordination.md`. Doable from the lab alone; no need to re-run the notebook. Answers are in the key at the end — try the questions first.

---

**1. (Concept)** The baseline single agent paid ~660 input tokens on its first call, the supervisor router ~445, and a specialist ~380–410. Decompose that 660 into the context-budget terms from Lab 8, and say which terms change when the ticket routes to a specialist instead. *(See Section 7 and Steps 4–7.)*

**2. (Concept)** Why is the supervisor's routing call the "cheapest call in the system" *and* the most stable as the company grows? What exactly happens to the router's decision-time context when a fourth department is added — and what happens to the baseline agent's? *(See Section 7 and Step 6.)*

**3. (Code)** The supervisor node returns `Command(goto=ROUTE_TO_NODE[call])`. What is `Command`, and what would you change so that the router, instead of jumping to a specialist, *writes its decision into the shared state* and lets a normal edge carry control? Name the `RoutingState` field the decision would live in and why it needs that annotation. *(See Step 6.)*

**4. (Code)** Write the `Command` that a `transfer_to_tech` tool must return so the jump happens in the *outer* desk graph and not inside the specialist's own agent loop. Why does `graph=Command.PARENT` matter — what would happen with the default? *(See Section 7 and Step 8.)*

**5. (Concept)** During the handoff run, Billing calls `transfer_to_tech` and the graph jumps to Tech — but `specialist_log` only records Tech's context, not Billing's. Explain the mechanism behind that missing entry. *(See Step 9 and Section 7.)*

**6. (Concept)** What is `handoff_budget` guarding against, and how is that guard different from the retry bound in Lab 9? Describe what the *second* transfer attempt returns and what the agent does with it. *(See Section 7 and Step 8.)*

**7. (Concept)** The lab says the "contract between departments is the ticket itself." What does the receiving specialist see when the graph jumps to it, and what does that design buy you over passing the full conversation history? *(See Section 7 and Step 9.)*

**8. (Applied)** Is the multi-agent desk cheaper per ticket than the baseline? Answer with the ledger numbers, then say precisely what the extra routing call buys that a single-agent prompt can't. *(See Steps 7, 10 and Section 7.)*

**9. (Code)** The optional exercise adds a `route_security` tool. Write the one-line addition to the supervisor node's `ROUTE_TO_NODE` map and the `Command` change (if any) needed so a compromised-account ticket is handled by the new security specialist. *(See Step 6 and Section 11.)*

---

## Answer Key

**1.** The baseline's 660 tokens are dominated by the **Σ tool schemas** term: all six tools' name+description+JSON-schema triple in the system message, plus the generic support prompt. The specialist run splits that: the router pays its own prompt + the three *short* route schemas (~445), and the specialist pays its department prompt + its two tools (~380–410). The **history/results** terms are the same for both — each call carries the ticket. The multi-agent design moves the tool-schema cost *out of the per-ticket bill* and into the cheapest, least-varied call (the router).

**2.** The router's context is bounded by the number of *route tools* it carries, and route tools are one-sentence schemas — so its decision-time cost grows by ~30 tokens per department and stays a small fraction of the baseline's. The baseline agent binds all six (later seven, eight...) tools to *every* request, so its first-call context grows by a full tool schema triple per department on every ticket — including tickets that never touch the new department. The router decides in ~445 tokens today and ~475 with four departments; the baseline grows by the schema cost of the new department for every ticket it ever handles.

**3.** `Command` is the control-flow primitive — a node (or tool) can return one to say "next node is X" instead of the graph following a static edge. To store the decision instead of jump: return `{"messages": [AIMessage(content=decision)]}` from the supervisor node and add a normal `supervisor → specialist` conditional edge that reads it. The decision would live in `RoutingState`, and `messages` must stay `Annotated[list, add_messages]` so the graph *merges* the supervisor's message into the shared state rather than overwriting it.

**4.** `Command(goto="tech", graph=Command.PARENT)`. The default (`graph="self"`) tells the *current* graph — the specialist agent's own model/tools loop — to jump to a node named `tech`, which doesn't exist inside a single `create_agent`. `Command.PARENT` climbs out to the desk graph where the `tech` node does exist, handing the whole conversation over so the outer graph routes to it.

**5.** When a specialist's agent returns a `Command` with `graph=Command.PARENT`, the agent's `invoke` raises an internal `ParentCommand` exception that LangGraph's runner uses to propagate the jump. The exception unwinds through the node function *before* the lines after `agent.invoke(...)` run — so Billing's `specialist_log.append(...)` never executes. Only the specialist that finishes the ticket (Tech) records its context. The jump isn't "returning a value to Billing's wrapper"; it is control-flow taking over the wrapper mid-function.

**6.** `handoff_budget` caps one transfer per run, guarding against the ping-pong loop of two specialists that each decide the other department owns the problem — the exact failure a recursion limit can't fix because each jump is only one graph step. The second transfer attempt finds `left <= 0` and returns plain *text* ("resolve it yourself with your own tools") instead of a `Command`; the agent treats it as a tool result and proceeds with its own tools. Lab 9's bound was an execution ceiling on retries; this is a domain-level contract on escalation.

**7.** The receiving specialist sees the original ticket (and the shared `messages` state) — not the transferring specialist's whole reasoning trace. That buys two things: each specialist's context stays small and department-scoped (Tech never pays for Billing's invoice checks), and the handoff is a handoff of *responsibility* — the new specialist re-reads the request from scratch with its own perspective, which is exactly what a human escalation does.

**8.** No — it is more expensive per ticket: the baseline is one call (~660 first-call tokens) versus a router call plus a specialist call for the multi-agent run. What the extra call buys is **bounded per-participant context** (each specialist sees only its prompt + 2 tools), **specialised prompts** (a billing specialist never carries outage-handling instructions), and **failure isolation and modularity** (a broken tech tool can't crash billing; adding a department touches only the router). Those are structural properties no single prompt can replicate.

**9.** Add one entry to the map: `"route_security": "security"`. The supervisor node already returns `Command(goto=ROUTE_TO_NODE[call])`, so binding `route_security` to the router is the only other change — no `Command` change is needed. The router's tool call becomes `route_security`, and the map's new entry resolves it to the new node, exactly as the existing three routes do.
