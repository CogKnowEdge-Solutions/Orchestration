# Lab 2 Assignment: Messages & Tools

Test what you learned in **Lab 2: Messages & Tools**. Try the exercises without re-running the notebook — use a scratch Python file for any code questions. Answers are at the bottom; check them after you've attempted everything.

---

## Exercises

**1. (Concept)** Which message type would you use to tell the model "Answer only in French, and keep every reply to one sentence"? Why does it belong at the top of the list? *(See Section 7.)*

**2. (Concept)** Name the four message types and, in one short phrase each, who or what each one represents.

**3. (Concept)** True or false, with a one-sentence explanation: *The model reads your tool's Python code to decide whether to call it.*

**4. (Code)** Write a `subtract(a: float, b: float) -> float` tool with a docstring, exactly as you would for the agent. Then say which part of your function becomes the tool's `description` and which part becomes its `parameters`.

**5. (Applied)** You run an agent and print its message types. You get `human, ai, tool, ai`. In plain words, what happened at each of the four steps?

**6. (Concept)** A `ToolMessage` carries a `tool_call_id`. What is that field for? *(See Section 7 and Section 10, Step 3.)*

**7. (Applied / Code)** You want the model to remember an earlier turn in a chat. Given this history:

```python
history = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="My favorite color is blue."),
]
```

How would you add a second question and keep the model's memory of the first? Write the code that builds the extended list.

---

## Answer Key

**1.** A `SystemMessage`. It sets the rules for the whole conversation, so it belongs first, at the top of the message list — the model reads it before anything else and treats it as standing instructions.

**2.**
- `SystemMessage` — the rules / instructions for the conversation.
- `HumanMessage` — your words.
- `AIMessage` — the model's words (or, with empty content, a tool request).
- `ToolMessage` — the result returned by a tool call.

**3.** False. The model never sees your code — it sees a JSON **schema** that LangChain builds from your function's docstring (which becomes the description) and type hints (which become the parameters). That's why the docstring must clearly say what the tool does.

**4.**

```python
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first and return the result."""
    return a - b
```

The docstring becomes the tool's `description`; the type hints (`a: float, b: float`) become its `parameters` — two `number` inputs, both required.

**5.** `human`: you asked a question. `ai`: the model replied with a tool request (empty text plus a tool call). `tool`: the agent ran the tool for real and its result came back as a message. `ai`: the model read the result and produced the final answer.

**6.** It links the tool's result back to the specific tool call the model requested, so the loop knows which call this result belongs to (important when several tools are in flight).

**7.**

```python
history = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="My favorite color is blue."),
    AIMessage(content="Got it — blue is your favorite color."),
    HumanMessage(content="What color did I say I liked?"),
]
```

The earlier exchange is just more messages in the list; the model reads the whole list top to bottom, so the second question is answered with the first one in context.
