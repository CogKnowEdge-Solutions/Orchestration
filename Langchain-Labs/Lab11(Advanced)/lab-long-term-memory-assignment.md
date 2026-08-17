# Lab 11 Assignment — Long-Term Memory

Test what you learned from `lab-long-term-memory.md`. Doable from the lab alone; no need to re-run the notebook. Answers are in the key at the end — try the questions first.

---

**1. (Concept)** The lab builds three separate memory mechanisms. Name all three, say which one survives a new `thread_id`, and what happens to the *conversation* of evening 1 when Cog returns in evening 2. *(See Section 7 and Steps 7–8.)*

**2. (Code)** Decode this call: `store.put(("guests", "cog", "facts"), "fact-2", {"content": "Cog loves tiramisu."})`. What are the namespace, the key, and the value? Write the one-liner that reads back **every** fact stored for Cog, and the one-liner that would read Node's instead. *(See Section 7 and Step 3.)*

**3. (Concept)** Why can't Node's evening ever show Cog's facts, even though both guests share one `InMemoryStore`? What is the mechanism, and how does the same idea keep multi-tenant SaaS memory safe? *(See Section 7 and Step 9.)*

**4. (Code)** `make_remember` returns a tool that closes over `(store, guest_id)`. Why is the closure necessary — why can't the `remember` tool just read `guest_id` from its own arguments? And why is putting the write behind a *tool* (instead of a plain node or a global list) the pattern real systems use? *(See Section 7 and Step 3.)*

**5. (Concept)** `load_memory` injects memory as a `SystemMessage` rebuilt every turn. Why does memory have to be *context* rather than something the model "just knows"? What specifically happens to the model call's token count between run 1 (empty store) and run 2 (dossier loaded), and why does that make "inject the whole store" a bad long-term strategy? *(See Section 7 and Steps 5, 10.)*

**6. (Code)** `recall_score(query, fact)` counts overlapping words longer than two characters. A guest asks *"What did you make for my birthday last year?"*; the store holds the fact *"Cog's birthday is October 14."* Walk through the score computation and say which fact is surfaced in the recall line. What would you swap the scorer for in a production system, and what does `store.search(..., query=...)` require to do that? *(See Section 7 and Step 5.)*

**7. (Concept)** The chef's `remember` tool is invoked by the model, not by a separate extraction node. What makes the model a good *fact extractor* here, and what risk does that create — i.e., how could a hallucinated or private fact end up in the store, and what guard would you add? *(See Section 7 and Step 3.)*

**8. (Applied)** The graph is compiled with `checkpointer=MemorySaver()` **and** `store=store`. If you removed the checkpointer, what still works and what breaks? If you removed the store instead, what breaks? Name one scenario each that a production system would hit. *(See Steps 6–9.)*

**9. (Code)** The optional exercise adds a `("guests", guest_id, "drinks")` namespace. Write the `remember_drink` factory call that mirrors `make_remember` (same shape, new namespace) and the single line to add to `load_memory` so both namespaces join the dossier. *(See Section 7 and Section 11.)*

---

## Answer Key

**1.** The three mechanisms are (a) thread-scoped short-term memory — the checkpointer (`MemorySaver`) persisting the conversation per `thread_id`; (b) long-term memory — the `InMemoryStore` surviving across threads; (c) recall — retrieval/ranking over the store. Only the store survives a new `thread_id`. Evening 1's conversation is gone in evening 2 (a different thread, so the checkpointer has no history for it); what survives is what `remember` wrote to the store, which `load_memory` rebuilds into the dossier.

**2.** Namespace: `("guests", "cog", "facts")`. Key: `"fact-2"`. Value: `{"content": "Cog loves tiramisu."}`. Read Cog's facts: `store.search(("guests", "cog", "facts"))`; Node's: `store.search(("guests", "node", "facts"))`. `search` is prefix-based, so the first tuple element tells the store *which guest's* branch to walk.

**3.** Namespacing. The store is a tree keyed by tuple prefixes; Cog lives under `("guests", "cog", ...)` and Node under `("guests", "node", ...)`. `search(("guests", "cog", "facts"))` only walks Cog's branch, so Node's context never receives Cog's items. In multi-tenant systems the tenant id becomes the namespace root — `("tenant_42", "users", ...)` — and every read is naturally scoped to one tenant with no shared-state bugs.

**4.** The guest is not known when the tool is defined — the tool is bound to the chef at node-build time, but the guest arrives per-run in `runtime.context`. The closure injects the right `guest_id` (and the store object) into the tool's behavior so the model only supplies the *fact*. Putting the write behind a tool keeps the persistence boundary in the audit trail (every `store.put` is a tool call), keeps the store/namespace API hidden from the model, and mirrors LangGraph's canonical memory pattern — the model extracts, the tool persists.

**5.** The model is stateless; it only sees the tokens you hand it. A fact in the store is invisible until `load_memory` turns it into a `SystemMessage`. Run 2's chef call carries the full dossier, so its input-token count is visibly higher than run 1's (empty store) — that is the price of memory on every call in the thread. Injecting the whole store would bloat every request and, across many guests, grow without bound; production systems summarize, rank, TTL-stamp, and retrieve narrowly instead.

**6.** Tokens > 2 chars: query → `{"what", "make", "birthday", "year"}` (after lowercasing and dropping `you`, `for`, `me`, `my`, `did`, `last`); fact → `{"cog's", "birthday", "october"}` (after dropping `is`). Overlap = `{"birthday"}` → score 1; any fact with score > 0 lands in the top-2 recall line, so the birthday fact is surfaced. In production you'd swap the scorer for an embedding index so `store.search(..., query=...)` can rank semantically — that requires configuring `InMemoryStore(index={"dims": ..., "embed": ...})` with an embedding function (an extra API, which the lab deliberately avoids).

**7.** The model reads the conversation, understands intent, and decides which statements are durable facts — that is exactly the extraction task an LLM is good at. The risk: the same model can hallucinate or over-extract, so a wrong, private, or redundant fact lands in the store and poisons every future session. Guards: human-in-the-loop review before persistence, an allow-list of fact categories, deduplication on write, and TTL so stale facts expire.

**8.** Without the checkpointer: long-term memory still works (facts survive threads), but the *conversation* resets on every turn — a multi-turn conversation in one thread loses context, and interleave/human-in-the-loop (Lab 6/9-style) checkpoint-dependent features break. Without the store: threads keep their conversation but every new thread starts with an empty dossier — the maître d' forgets returning guests entirely, and nothing survives a process restart (since the checkpointer is in-memory too). In production: removing the checkpointer breaks any chat app that needs turn history; removing the store breaks any personalization/customer memory feature.

**9.** `remember_drink = make_remember(store, guest_id)` doesn't directly apply because the namespace is baked into the factory — so write a parallel factory (or parameterize `make_remember(store, guest_id, category)`) that calls `store.put(("guests", guest_id, "drinks"), f"drink-{n+1}", {"content": choice})`. In `load_memory`, add: `drinks = runtime.store.search(("guests", guest, "drinks"))` and join its contents into the same `dossier` string so both namespaces reach the chef in one prompt.
