# Lab 8 Assignment — MCP & Context Engineering

Test what you learned from `lab-mcp-context-engineering.md`. Doable from the lab alone; no need to re-run the notebook. Answers are in the key at the end — try the questions first.

---

**1. (Concept)** The lab connects to two servers with `"transport": "http"` (Coinfuty over HTTPS, your own over HTTP), while Lab 7 used stdio. What actually changes between a stdio server and a remote/hosted server, and why does none of your agent code change? *(See Section 7.)*

**2. (Concept)** Write out the "context budget" equation for one agent decision step, and say which of its terms are a fixed cost per request and which are variable. *(See Section 7.)*

**3. (Applied)** The context ledger showed a 570-character JSON schema costing roughly 150 tokens on *every* request, whether the tool runs or not. Which lever removes that cost when the server is external (Coinfuty), and which lever removes it when the server is yours? *(See Section 7 and Step 5.)*

**4. (Code)** Write the connection-dict entry that would add a third server named `"news"` at `https://news.example.com/api/mcp` to the `MultiServerMCPClient` from Step 4.

**5. (Concept)** In A/B 1 the pruned run's `calls[0]` was about 70% smaller than the full run's, yet both answers were correct. Why is the *first* LLM call's `prompt_tokens` the right measure of "decision-time context" rather than the run's total token count? *(See Steps 6–7.)*

**6. (Applied)** A/B 2 turned a ~14 KB tool result into ~6,500 input tokens on the follow-up call. Who controls that number when the server is external, who controls it when the server is yours, and what are the two concrete ways to shrink it? *(See Section 7 and Step 7.)*

**7. (Concept)** Why does a tool's *result* size only cost tokens on calls that come *after* the model already chose to call the tool — and why does the tool's *schema* cost tokens on the very first call? *(See Section 7.)*

**8. (Code)** `UsageCapture.on_llm_end` records `prompt_tokens`. Write the one-line change that would also record `completion_tokens` for every call. *(See Step 2.)*

**9. (Applied)** After the Optional Exercise (slim `digest_logs`'s description, add `max_events` to `digest_highlights`), which cells/rows of the Step 8 ledger should move, and in which direction? *(See Section 11.)*

---

## Answer Key

**1.** Only the transport and the connection dict change: stdio spawns the server as a subprocess and talks over pipes; a remote server exposes the same JSON-RPC over HTTP and you point at a URL. MCP keeps the message layer identical (`initialize`, `tools/list`, `tools/call`), so the adapter hands you the same LangChain tools and the agent loop never knows where they came from.

**2.** `context = system prompt + (name + description + JSON schema) × each bound tool + conversation history + last tool result(s)`. The system prompt, the per-tool triple, and the history prefix are paid on every request (fixed-ish); the tool result is variable and arrives after the model already decided to call the tool.

**3.** External server: **prune** — you cannot edit Coinfuty's schemas, only choose not to bind the tool. Your own server: **describe/shape** — you author the description (and the schema signature) in the server file, so you can slim them at the source.

**4.** `"news": {"transport": "http", "url": "https://news.example.com/api/mcp"}` inside the `MultiServerMCPClient` dict (with `tool_name_prefix` if its tool names could collide).

**5.** `calls[0]` is what the model saw *before* making its decision: system prompt + all bound schemas + the question. Total tokens also include tool results and the final answer generation, which depend on what happened *after* the decision — useful, but a different thing. Decision-time context is the part you control up front by choosing tools.

**6.** When the server is external, the **server author** controls the payload; you can only pick a different tool, prune the toolset, or (if it has one) pass a `limit`-style argument. When the server is yours, **you** control it by shaping the result server-side (e.g., `digest_highlights`), or truncating before returning. The two concrete ways: shape/truncate on the server, or ask for less (fewer rows/lines) in the tool call.

**7.** The result does not exist until the tool runs — the first call only carries schemas, so the result's cost lands on the follow-up call that includes it. The schema is metadata sent before any call, so it is billed on the first call and every one after while the tool stays bound.

**8.** `self.completion.append(usage.get("completion_tokens", 0))` alongside the `prompt_tokens` line (or `self.calls.append((usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)))` for a tuple per call).

**9.** Step 8's "prune: decision tokens" row stays put (that was the external server). The **first-call** numbers for the fat/lean runs in Step 7 should drop (smaller `digest_logs` description = smaller fixed cost). The lean run's result chars and post-result context should drop further when `max_events` caps the digest. Nothing in the external rows changes — you can't edit someone else's server.
