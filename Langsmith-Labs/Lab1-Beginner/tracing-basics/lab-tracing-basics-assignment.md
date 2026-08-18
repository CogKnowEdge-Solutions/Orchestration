# Lab 1: Tracing Basics & Types of Runs — Assignment

## Exercises

Complete these exercises after finishing the lab. You should be able to answer them from the lab content alone, without re-running the notebook.

---

### Exercise 1: Concept Question (Run Types)

What are the seven run types that LangSmith recognizes? List them and give a one-sentence description of when each one appears.

---

### Exercise 2: Concept Question (Run Tree)

In the run tree hierarchy, what is the relationship between a `chain` run and an `llm` run? Which one is the parent and which is the child? How can you see this relationship in the LangSmith UI?

---

### Exercise 3: Code Task (Environment Variables)

Write a Python script that loads the required environment variables for LangSmith tracing and prints an error message if any are missing. Your script should check for:
- `OPENROUTER_API_KEY`
- `LANGSMITH_API_KEY`
- `LANGSMITH_TRACING` (should be `"true"`)
- `LANGSMITH_PROJECT`

---

### Exercise 4: Code Task (Adding @traceable)

Write a function that calls a chat model via OpenRouter with a custom system message. Decorate it with `@traceable` and set the `run_type` to `"llm"`. Your function should accept two parameters: `system_message` and `user_message`.

---

### Exercise 5: Applied Task (Extending the Chain)

The lab created a `question_answerer` chain that wraps a single LLM call. Extend this pattern by creating a new chain that:
1. Takes a topic as input
2. Calls a function that generates a joke about that topic (using OpenRouter)
3. Calls a function that explains why the joke is funny (using OpenRouter)
4. Returns both the joke and the explanation

Your chain should have three runs: one `chain` parent and two `llm` children.

---

### Exercise 6: Concept Question (Tracing Configuration)

What does the `LANGSMITH_TRACING=true` environment variable do? What happens if you set it to `false` or omit it entirely?

---

### Exercise 7: Code Task (Querying Traces)

Write a Python function that queries LangSmith for all traces in your project and prints a summary showing:
- Total number of traces
- For each trace: name, run type, status, and latency

---

## Answer Key

---

### Exercise 1: Concept Question (Run Types)

**Answer:**
1. **`llm`** — A single model call (e.g., OpenAI chat completion via OpenRouter)
2. **`chain`** — A wrapping operation that contains child runs (e.g., a RAG pipeline)
3. **`tool`** — A tool execution (e.g., a custom calculator function)
4. **`retriever`** — Document retrieval operations (e.g., vector similarity search)
5. **`embedding`** — Embedding generation (e.g., converting text to vectors)
6. **`prompt`** — Prompt formatting and template rendering
7. **`parser`** — Output parsing (e.g., JSON extraction, format conversion)

---

### Exercise 2: Concept Question (Run Tree)

**Answer:** The `chain` run is the **parent** and the `llm` run is the **child**. In the LangSmith UI, you see this as a nested hierarchy: the chain run appears at the top level, and the LLM run appears indented beneath it. This shows that the LLM call was executed as part of the chain's operation.

---

### Exercise 3: Code Task (Environment Variables)

**Answer:**

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check each required variable
missing = []
if not os.getenv("OPENROUTER_API_KEY"):
    missing.append("OPENROUTER_API_KEY")
if not os.getenv("LANGSMITH_API_KEY"):
    missing.append("LANGSMITH_API_KEY")
if os.getenv("LANGSMITH_TRACING") != "true":
    missing.append("LANGSMITH_TRACING (should be 'true')")
if not os.getenv("LANGSMITH_PROJECT"):
    missing.append("LANGSMITH_PROJECT")

# Print results
if missing:
    print("✗ Missing environment variables:")
    for var in missing:
        print(f"  - {var}")
else:
    print("✓ All environment variables loaded successfully")
```

---

### Exercise 4: Code Task (Adding @traceable)

**Answer:**

```python
from langsmith import traceable
from openai import OpenAI
import os

# Initialize OpenRouter client
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@traceable(run_type="llm", name="custom_chat")
def custom_chat(system_message: str, user_message: str) -> str:
    """Call chat model via OpenRouter with a system message and user message."""
    response = openai_client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content
```

---

### Exercise 5: Applied Task (Extending the Chain)

**Answer:**

```python
@traceable(run_type="llm", name="generate_joke")
def generate_joke(topic: str) -> str:
    """Generate a joke about the given topic."""
    response = openai_client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "You are a comedian. Tell short, clean jokes."},
            {"role": "user", "content": f"Tell me a joke about {topic}"}
        ]
    )
    return response.choices[0].message.content

@traceable(run_type="llm", name="explain_joke")
def explain_joke(joke: str) -> str:
    """Explain why the joke is funny."""
    response = openai_client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "You explain why jokes are funny in a concise way."},
            {"role": "user", "content": f"Why is this joke funny: {joke}"}
        ]
    )
    return response.choices[0].message.content

@traceable(run_type="chain", name="joke_chain")
def joke_chain(topic: str) -> dict:
    """Generate a joke and explain why it's funny."""
    joke = generate_joke(topic)
    explanation = explain_joke(joke)
    return {"joke": joke, "explanation": explanation}
```

---

### Exercise 6: Concept Question (Tracing Configuration)

**Answer:** The `LANGSMITH_TRACING=true` environment variable tells the LangSmith SDK to send traces to LangSmith's servers. If you set it to `false` or omit it, the SDK will not send any traces — your code will still run, but you won't see any data in the LangSmith UI. This is useful for production environments where you might want to disable tracing for performance or cost reasons.

---

### Exercise 7: Code Task (Querying Traces)

**Answer:**

```python
from langsmith import Client
import os

def print_trace_summary():
    """Query LangSmith and print a summary of recent traces."""
    client = Client()
    
    # Get traces from the current project
    traces = list(client.list_runs(
        project_name=os.getenv("LANGSMITH_PROJECT"),
        is_root=True,
        limit=20
    ))
    
    print(f"Total traces: {len(traces)}")
    print("-" * 60)
    
    for trace in traces:
        print(f"Name: {trace.name}")
        print(f"  Type: {trace.run_type}")
        print(f"  Status: {trace.status}")
        print(f"  Latency: {trace.total_tokens or 'N/A'} tokens")
        print()
```

---

## Summary

This assignment tested your understanding of:
- LangSmith's seven run types (llm, chain, tool, retriever, embedding, prompt, parser)
- The run tree hierarchy and parent-child relationships
- Environment variable configuration for LangSmith
- The `@traceable` decorator and its parameters
- Extending chains with multiple child runs
- Querying traces programmatically
- OpenRouter's free models for zero-cost experimentation
