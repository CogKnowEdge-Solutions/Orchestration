# Lab 4: Prompt Playground & Prompt Hub — Assignment

## Exercises

Complete these exercises after finishing the lab. You should be able to answer them from the lab content alone, without re-running the notebook.

---

### Exercise 1: Concept Question (Playground vs Hub)

What is the difference between the LangSmith Playground and Prompt Hub? Describe when you would use each one.

---

### Exercise 2: Concept Question (Versioning)

What happens when you push a prompt to Hub with the same name twice? How do you pull a specific version instead of the latest? Why is version pinning important in production code?

---

### Exercise 3: Code Task (Push a Prompt)

Write Python code that creates a `ChatPromptTemplate` with a system message ("You are a movie critic. Rate movies from 1-5 stars with a brief review.") and a user message ("Review this movie: {title}"). Push it to Prompt Hub with the name `movie-critic`.

---

### Exercise 4: Code Task (Pull and Invoke)

Write Python code that pulls the `movie-critic` prompt from Hub, invokes it with `title="Inception"`, and prints the formatted messages.

---

### Exercise 5: Applied Task (Prompt Iteration)

You pushed version 1 of a `tool-selector` prompt. Describe the steps you would take to refine it based on an LLM response that wasn't structured correctly. What SDK methods would you use, and in what order?

---

### Exercise 6: Concept Question (Few-Shot Prompts)

What is a few-shot prompt? How does adding example input/output pairs change the LLM's behavior compared to a zero-shot prompt (no examples)?

---

### Exercise 7: Code Task (List and Compare)

Write Python code that lists all prompts in your workspace and prints each prompt's `repo_handle`. Then pull the first prompt in the list and print its number of messages.

---

## Answer Key

---

### Exercise 1: Concept Question (Playground vs Hub)

**Answer:**
- **Playground** is a web UI for interactively testing prompts — you type prompts, adjust parameters (temperature, max tokens, model), and see responses in real time without writing code. Use it when you're iterating on a prompt and want fast visual feedback.
- **Prompt Hub** is a version-controlled registry for stored prompts — you push prompts via the SDK, pull them programmatically, and share them with your team. Use it when you want to persist, version, and deploy prompts across your codebase.

---

### Exercise 2: Concept Question (Versioning)

**Answer:** When you push a prompt with the same name twice, LangSmith creates a new version (version 2) instead of overwriting version 1. Both versions are preserved. To pull a specific version, use `client.pull_prompt("name:2")` where `:2` is the version number (or a commit hash). Version pinning is important in production because pulling without a version returns the latest — if a teammate pushes a new version, your production code silently gets a different prompt and may break.

---

### Exercise 3: Code Task (Push a Prompt)

**Answer:**

```python
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate

client = Client()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a movie critic. Rate movies from 1-5 stars with a brief review."),
    ("user", "Review this movie: {title}")
])

url = client.push_prompt("movie-critic", object=prompt)
print(f"Pushed to Hub: {url}")
```

---

### Exercise 4: Code Task (Pull and Invoke)

**Answer:**

```python
from langsmith import Client

client = Client()
pulled = client.pull_prompt("movie-critic")
formatted = pulled.invoke({"title": "Inception"})

for msg in formatted.messages:
    print(f"{msg.type}: {msg.content}")
```

---

### Exercise 5: Applied Task (Prompt Iteration)

**Answer:**
1. **Analyze the LLM response** — identify what went wrong (e.g., the model didn't follow the format)
2. **Refine the prompt** — add clearer instructions, adjust the format specification, or add few-shot examples
3. **Push the refined prompt** — use `client.push_prompt("tool-selector", object=refined_prompt)` to create version 2
4. **Test the new version** — pull it with `client.pull_prompt("tool-selector:2")`, invoke it, and send to an LLM
5. **Compare results** — pull both versions side by side with `pull_prompt("tool-selector:1")` and `pull_prompt("tool-selector:2")` to see the improvement
6. **If needed, repeat** — iterate until the output is consistently structured

---

### Exercise 6: Concept Question (Few-Shot Prompts)

**Answer:** A few-shot prompt includes example input/output pairs before the actual question. This teaches the model the exact format and behavior you want by demonstration. Compared to a zero-shot prompt (which relies on instructions alone), few-shot prompts produce more consistent, correctly-formatted output because the model learns the pattern from examples rather than just reading text instructions.

---

### Exercise 7: Code Task (List and Compare)

**Answer:**

```python
from langsmith import Client

client = Client()
prompts = list(client.list_prompts(limit=10))

print(f"Found {len(prompts)} prompts:")
for p in prompts:
    print(f"  - {p.repo_handle}")

# Pull the first prompt and check its structure
if prompts:
    first = client.pull_prompt(prompts[0].repo_handle)
    print(f"\nFirst prompt has {len(first.messages)} messages")
```

---

## Summary

This assignment tested your understanding of:
- The difference between LangSmith Playground (web UI) and Prompt Hub (SDK registry)
- Prompt versioning and version pinning
- Pushing, pulling, and listing prompts with the SDK
- Prompt iteration and refinement workflow
- Few-shot prompts and their advantage over zero-shot prompts
- Programmatic prompt management with the LangSmith SDK
