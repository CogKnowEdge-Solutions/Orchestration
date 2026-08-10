# Lab 1 Assignment: Agents & Models

Test what you learned in **Lab 1: Agents & Models**. Try the exercises without re-running the notebook — use a scratch Python file for any code questions. Answers are at the bottom; check them after you've attempted everything.

---

## Exercises

**1. (Concept)** In your own words, what is the difference between a **model** and an **agent**? *(See Sections 1 and 7.)*

**2. (Concept)** An agent is built from three parts. Name all three and, in one short phrase each, what each part does. *(See Section 7.)*

**3. (Concept)** True or false, with a one-sentence explanation: *When the agent answers "What is 8 multiplied by 7?", your Python `multiply` function is executed by the model itself.*

**4. (Code)** Write the `multiply` tool exactly as you would in the lab (docstring and type hints included). Then say which two parts of the function LangChain reads to describe the tool to the model — and what, exactly, the model sees.

**5. (Applied)** Compare `agent = create_agent(model_1, tools=[multiply])` with `agent_2 = create_agent(model_2, tools=[multiply])`. What changed, what stayed the same, and why does the agent keep working after the swap? *(See Section 7, "Why model-swapping is free".)*

**6. (Applied)** In Step 6 the lab prints `result_1["messages"][-1].content` and calls it the final answer. Why is the *last* message in that list the answer? *(See Section 10, Step 6.)*

**7. (Applied)** The lab asks the agent two questions: "What is 8 multiplied by 7?" and "In one sentence, what is an AI agent?" Which one triggers a tool call, and why does the other one not? *(See Section 10, Steps 6 and 9.)*

---

## Answer Key

**1.** A **model** is the brain: you send it text, it returns text, but it has no hands — it cannot look things up, calculate reliably, or touch the outside world. An **agent** is the model plus **tools** (functions it's allowed to call) plus a **loop** that decides when to call them and feeds the results back. A model talks; an agent does.

**2.**
- **Model** — the brain: produces text and decides what to do next.
- **Tools** — the hands: functions the model is allowed to call.
- **Loop** — the schedule: machinery that executes tool calls and feeds results back until the model can answer directly.

**3.** False. The model never runs your code — it only *requests* a tool call ("call `multiply` with 8 and 7"), and the agent loop executes your function for real and hands the result back. That separation is the whole point of agents.

**4.**
```python
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return their product."""
    return a * b
```
LangChain reads the **docstring** (becomes the tool's `description`) and the **type hints** (become the tool's `parameters`). What the model sees is a JSON **schema** describing the tool's name, what it does, and what inputs it takes — never your Python code.

**5.** Only the model changed (`model_1` → `model_2`); the `multiply` tool and the `create_agent` structure are untouched. It works because LangChain talks to every model through one interface (`BaseChatModel`), so the agent code never mentions a provider — it just needs *a* model object. That's why swapping the brain is a one-line change.

**6.** The agent's conversation is stored in `result_1["messages"]`, and the loop keeps going until the model can answer without another tool call. The **last** message is therefore the model's final answer — the earlier messages are the tool requests and results that led up to it.

**7.** "What is 8 multiplied by 7?" triggers the `multiply` tool call, because arithmetic is something the model can't do reliably from memory. "In one sentence, what is an AI agent?" is answered directly from the model's training knowledge, so the loop decides "no tool needed" and the model just answers. The loop is a *decision*, not an automatic tool-call.
