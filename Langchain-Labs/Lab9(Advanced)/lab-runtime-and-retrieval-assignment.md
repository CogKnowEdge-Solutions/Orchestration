# Lab 9 Assignment — Runtime & Retrieval

Test what you learned from `lab-runtime-and-retrieval.md`. Doable from the lab alone; no need to re-run the notebook. Answers are in the key at the end — try the questions first.

---

**1. (Concept)** `interrupt_before=["tools"]` parks a run "between the model deciding to call a tool and the tool actually firing." What does the checkpointer + `thread_id` have to do with that pause? Why can't you park a run without it? *(See Section 7 and Step 4.)*

**2. (Concept)** `recursion_limit=8` was described as "roughly four decide→act cycles." Why do eight allowed nodes become only four tool calls, and what happens when the loop tries to go further? *(See Section 7 and Step 5.)*

**3. (Concept)** The lab claims baked-in context is a *fixed* cost and retrieval is a *variable* cost. Define both terms using the context-budget equation from Lab 8 (`system + Σ tool schemas + history + results`), and say which budget term each variant changes. *(See Section 7.)*

**4. (Applied)** In the closing ledger, baked-in paid ~490 tokens on call one for the whole 8-doc corpus; retrieval paid ~335 on call one and ~495 after retrieving 2 docs. Explain *why* the retrieval agent's second call (~495) is larger than its first (~335), and what that ~160-token delta represents. *(See Steps 8–9.)*

**5. (Code)** Write the `create_agent` call (model + tools + config) that produces a run which pauses *after* the tools execute rather than before. Name the parameter change and the one other piece that must be present for the pause to survive the invoke. *(See Step 4.)*

**6. (Concept)** The BM25 formula has three ingredients: term frequency, IDF, and length normalization. For each one, say in one sentence what it protects against or rewards. *(See Section 7 and Step 7.)*

**7. (Applied)** The lab's `kb_search` returns the top-2 documents verbatim. In Lab 8 you learned three context levers: prune, describe, and shape. Which of those levers is `kb_search`'s `[:2]` slice an example of, and who gets to pull it? *(See Section 7 and Lab 8 Section 7.)*

**8. (Code)** `get_price` returns a `503`-style retry invitation? No — `run_etl` does. Write the one-line change (a module-level counter + a condition) that makes `run_etl` succeed on its third call, and say what happens to the Step 5 run if you leave `recursion_limit=8` unchanged. *(See Step 5 and Section 11.)*

**9. (Concept)** The lab says retrieval "is what makes retrieval the scalable answer for large knowledge." Why does doubling the corpus to 16 docs barely change the retrieval agent's token ledger but roughly double the baked-in one? *(See Section 7.)*

---

## Answer Key

**1.** The interrupt only pauses the *execution*; the *state* (messages, tool results, node position) lives in the checkpointer, keyed by `thread_id`. Without a checkpointer, `invoke` returns only when a run finishes — there is nowhere for a parked run to live, so the pause cannot be resumed. The `thread_id` is the address of that parked state: `Command(resume=...)` with the same config finds it and continues.

**2.** `recursion_limit` counts *nodes* visited, not model calls or tool calls. Each cycle visits two nodes — `model` then `tools` — so 8 nodes ≈ 4 model calls + 4 tool executions. When the loop tries to visit node 9, the runtime raises `GraphRecursionError` instead of executing it; the run ends, and the state (including the error) stays inspectable via `get_state`.

**3.** Baked-in changes the **system prompt** term: the whole corpus is in the system prompt, so every request pays all of it regardless of what the question needs — that is a fixed cost. Retrieval changes the **tool results** term: the corpus is not in the context at all until the model calls `kb_search`, and only the returned documents are added — that is a variable cost, incurred after the model already chose to retrieve.

**4.** Call one carries only the small system prompt + the `kb_search` schema (~335 tokens): the agent's *decision* is cheap. The second call carries everything from call one *plus* the two retrieved documents returned by the tool (~495 tokens). The ~160-token delta is literally the cost of the knowledge the agent decided it needed — paid only because it chose to call the tool.

**5.** Change `interrupt_before=["tools"]` to `interrupt_after=["tools"]` (or `interrupt_before` to `interrupt_after`) and keep the checkpointer: `create_agent(model=model(), tools=[get_price], interrupt_after=["tools"], checkpointer=checkpointer)`. The checkpointer is required for the pause to survive the invoke — without it there is no parked state to resume.

**6.** **Term frequency** rewards documents that mention the query's terms more often. **IDF** rewards matches on rare, discriminating terms (a match on "kill-switch" is worth more than one on "trading"). **Length normalization** stops long documents from winning by volume — a 2,000-word doc must match more terms to score like a 50-word one.

**7.** It is **shape** — limiting *how much of the result* the model receives. `[:2]` caps the tool's return to two documents, the same lever the server author pulls when a digest tool truncates a 14 KB log firehose. Here the "server author" is you, because you wrote the tool.

**8.** Add a counter, e.g. `_etl_calls = {"n": 0}` at module level, and in `run_etl`: `_etl_calls["n"] += 1; if _etl_calls["n"] >= 3: return "Job j-1042 completed successfully."` With `recursion_limit=8` unchanged, the run now *completes* — the agent retries twice, gets the success payload on the third call, and reports the status instead of raising. The optional exercise shows you can then force the error again by dropping the limit to 4 (three retries need more nodes than 4 allows).

**9.** Baked-in pays the system prompt on every call, so the corpus size *is* the fixed cost: 16 docs ≈ 2× tokens. Retrieval's first call pays only the tool schema (unchanged by corpus size), and its second call pays for the same 2 retrieved documents (unchanged by corpus size, assuming the extra docs don't outrank them) — so the ledger barely moves. The variable cost scales with *what the question needs*, not with *how much knowledge exists*.
