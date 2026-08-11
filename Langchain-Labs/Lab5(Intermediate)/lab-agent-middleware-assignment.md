# Lab 5 Assignment: Agent Middleware

Test what you learned in **Lab 5: Agent Middleware**. Try the exercises without re-running the notebook — use a scratch Python file for any code questions. Answers are at the bottom; check them after you've attempted everything.

---

## Exercises

**1. (Concept)** The agent loop from Lab 2 is "model → tools → model → ... until done." Where exactly do `before_model` and `after_model` run relative to the model call, and how many times does each fire in a single run that makes one tool call? *(See Section 7.)*

**2. (Concept)** What is the difference between a *node-style* hook and a *wrap-style* hook, and what rule of thumb tells you which to use? *(See Section 7.)*

**3. (Code)** Write the one-line `create_agent` argument that attaches middleware, and show how you would combine two prebuilt middleware (`PIIMiddleware` and `ModelCallLimitMiddleware`) with a custom `LoggingMiddleware` in that slot. *(See Section 10, Steps 5–7 and the Optional Exercise.)*

**4. (Concept)** In Step 5, the user message is `"My email is john.smith@example.com. What is my email?"` and the model's reply references `[REDACTED_EMAIL]`. The raw email never reached the model. Which hook made that happen, and what does the returned state's `messages` list contain for that user turn? *(See Section 10, Step 5.)*

**5. (Concept)** `PIIMiddleware("email", strategy="block", apply_to_input=True)` raises `PIIDetectionError` when an email is detected. Roughly how many model calls were made before the exception fired, and why? *(See Section 10, Step 5.)*

**6. (Applied)** Step 6 ends with the message `Model call limits exceeded: run limit (1/1)` instead of a weather answer. Walk through how many model calls were *attempted*, how many *succeeded*, and which one was blocked. Why did the tool still run? *(See Section 10, Step 6.)*

**7. (Code)** A teammate asks for a custom middleware that logs the wall-clock time of each model call. Which hook would you implement — `before_model`/`after_model` or `wrap_model_call` — and why? Sketch the key two lines that time the call. *(See Section 10, Step 8.)*

**8. (Concept)** `@before_model` on a plain function and a `class X(AgentMiddleware)` with a `before_model` method produce the same kind of object. True or false, and what does that fact allow you to do in a single `middleware=[...]` list? *(See Sections 7 and 10, Step 9.)*

**9. (Applied)** You stack `LoggingMiddleware`, `PIIMiddleware`, and `ModelCallLimitMiddleware` on one agent. In what order do the `before_model` hooks print across one tool-calling run, and which state does the PII hook edit before the model sees it? *(See the Optional Exercise.)*

---

## Answer Key

**1.** `before_model` runs immediately before each model call; `after_model` runs immediately after each model response. In a run that calls the model once, produces a tool call, and then calls the model again for the final answer, each hook fires **twice** — once per model call, including the call that requested the tool.

**2.** Node-style hooks (`before_model`, `after_model`, `before_agent`, `after_agent`) run *between* steps of the loop: they see the current state and can update it (log, redact, count). Wrap-style hooks (`wrap_model_call`, `wrap_tool_call`) *surround the call itself*: they receive a `handler` and decide whether to call it zero, one, or many times. Rule of thumb: node-style for sequential logic (logging, validation, redaction); wrap-style for control flow (retry, fallback, caching, timing).

**3.** The argument is `middleware=[...]`:
```python
agent = create_agent(
    model=model,
    middleware=[
        LoggingMiddleware(),
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        ModelCallLimitMiddleware(run_limit=1),
    ],
)
```
All three are `AgentMiddleware` instances, so they mix freely in the same list.

**4.** The `before_model` hook of `PIIMiddleware` scanned the newest human message, replaced the detected address with `[REDACTED_EMAIL]`, and returned a state update. In the returned state, that user turn is a `HumanMessage` whose content is `"My email is [REDACTED_EMAIL]. What is my email?"` — the sanitized version, which is what the model was actually given.

**5.** **Zero.** `block` raises `PIIDetectionError` from inside `before_model`, which runs before the model is invoked. The run is refused before any request reaches the API — which is why a blocking guardrail costs nothing on your quota.

**6.** Two model calls were attempted and **one succeeded**. The first call (budget 0 → 0 of 1 used) returned a tool request, and the tool ran. When the loop tried the second model call — the one that would write the final answer — `before_model` saw `run_model_call_count == 1` (already at the limit) and jumped the run to the end with the limit message instead of calling the API. The tool still ran because it executes *after* the first model call and before the second is refused.

**7.** `wrap_model_call`, because the timing must surround the call itself — node-style hooks run *between* loop steps and can't time the call. The two key lines:
```python
start = time.perf_counter()
response = handler(request)          # the actual model call
print(f"took {time.perf_counter() - start:.2f}s")
```

**8.** **True.** `@before_model` on a function returns an `AgentMiddleware` instance, the same kind of object a subclass produces. Because every style yields the same type, one `middleware=[...]` list can freely mix class-based custom middleware, decorator-based custom middleware, and prebuilt middleware.

**9.** Hooks run first-to-last for `before_*`: `LoggingMiddleware.before_model` prints first, then `PIIMiddleware.before_model` edits the state — replacing the email in the newest human message with `[REDACTED_EMAIL]` — then `ModelCallLimitMiddleware.before_model` checks the call count. So the model's input always contains the redacted address, and across a tool-calling run you'd see the before/after log lines around each model call, with the second one ending in `Model call limits exceeded: run limit (1/1)`.
