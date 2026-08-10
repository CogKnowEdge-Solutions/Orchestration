# Lab 4 Assignment: Short-Term Memory & Streaming

Test what you learned in **Lab 4: Short-Term Memory & Streaming**. Try the exercises without re-running the notebook — use a scratch Python file for any code questions. Answers are at the bottom; check them after you've attempted everything.

---

## Exercises

**1. (Concept)** Why is a chat model inherently unable to remember previous turns on its own, and where does conversational memory actually live? *(See Section 7.)*

**2. (Concept)** `RunnableWithMessageHistory` performs the same sequence on every call. Name the steps, in order. *(See Section 7.)*

**3. (Code)** Write the single line that adds a history slot to a `ChatPromptTemplate`, and state what other piece of the setup must use the same name. *(See Section 10, Steps 4–5.)*

**4. (Concept)** Two users both call the same `chat` object. What keeps user A's facts from leaking into user B's conversation? *(See Sections 7 and 10, Step 7.)*

**5. (Code)** Given `store = {}` and the callback `return store.setdefault(session_id, InMemoryChatMessageHistory())`, what does the call `get_session_history("ada")` return the *first* time, and what does a *second* call return? *(See Section 10, Step 4.)*

**6. (Concept)** What is an `AIMessageChunk`, and why do `end=""` and `flush=True` in the print produce a "typing" effect? *(See Sections 7 and 10, Step 8.)*

**7. (Applied)** In Step 9 the model streams the word "Ada" even though "Ada" appears nowhere in the current input `"In one word, what is my name?"`. Where does that word come from? *(See Section 10, Steps 6–9.)*

**8. (Concept)** Why does an unbounded history become a problem as a conversation grows, and what does `trim_messages` in the optional exercise do about it? *(See Section 7 and Section 11.)*

**9. (Applied)** Predict the output: you run Step 6's two calls with `session_id="ada"`, then run `print(len(store["ada"].messages))`. What number prints, and why? *(See Section 10, Step 6.)*

---

## Answer Key

**1.** A chat model is a function from text to text with no state between calls — each request is independent and the model keeps nothing from the previous one. Conversational memory therefore lives in *your program*: a store (here a per-session `ChatMessageHistory`) that replays past turns into each new prompt.

**2.** Load the session's history via `get_session_history`; inject it into the prompt's `history` slot; call the model; then append the new user turn and the model's reply back to the store. (Load → inject → call → append.)

**3.** `MessagesPlaceholder("history")` — and the wrapper in Step 5 must use the same name in `history_messages_key="history"` so it knows which prompt variable to fill with the replayed conversation.

**4.** The `session_id` in each call's config. The wrapper looks up history by that ID, so user A and user B get different histories from the same store — memory is scoped per conversation, not shared globally.

**5.** The first call creates, stores, and returns a new empty `InMemoryChatMessageHistory`. The second call returns the *same* object (now containing the earlier turn's messages). `setdefault` returns the existing value when the key is present.

**6.** An `AIMessageChunk` is a piece of the response carrying the tokens generated since the previous chunk, yielded one at a time by `model.stream()`. Printing each chunk's `.content` with `end=""` keeps everything on one line, and `flush=True` pushes each chunk to the display immediately instead of buffering — together they render text as it arrives, which looks like live typing.

**7.** From the `ada` session's stored history, replayed into the prompt by `RunnableWithMessageHistory`. "Ada" was introduced in Step 6's first turn; by the time Step 9 streams, the wrapper has loaded that conversation and injected it, so the model can answer from context.

**8.** Every call replays the entire history as prompt tokens, so a long conversation means a longer prompt: more latency, more tokens, and more cost on paid models. `trim_messages` caps the window — it keeps only the most recent messages within a token/word budget, so older turns fall out of what the model sees (even though the store still holds them).

**9.** `4`. Two turns produce four stored messages — each turn adds one `HumanMessage` (the input) and one `AIMessage` (the reply) — and Step 6's print confirms exactly `History stored for 'ada': 4 messages`.
