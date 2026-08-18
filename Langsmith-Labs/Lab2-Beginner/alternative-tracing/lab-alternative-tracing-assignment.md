# Lab 2: Alternative Ways to Trace & Conversational Threads — Assignment

## Exercises

Complete these exercises after finishing the lab. You should be able to answer them from the lab content alone, without re-running the notebook.

---

### Exercise 1: Concept Question (Tracing Mechanisms)

What are the three tracing mechanisms taught in this lab? For each one, give a one-sentence description of when you would use it.

---

### Exercise 2: Concept Question (wrap_openai)

How does `wrap_openai` differ from the `@traceable` decorator from Lab 1? What advantage does it offer when you're making many OpenAI API calls?

---

### Exercise 3: Concept Question (thread_id)

What is a `thread_id` and why would you use it? Describe a scenario where grouping runs by thread_id is useful.

---

### Exercise 4: Code Task (wrap_openai)

Write a Python script that uses `wrap_openai` to trace three different chat completion calls through the same wrapped client. Each call should ask a different question. Print each response.

---

### Exercise 5: Code Task (trace() Context Manager)

Write a function that uses the `trace()` context manager to wrap two sequential LLM calls — one that generates a fact and one that generates a question about that fact. Both calls should appear inside a single trace.

---

### Exercise 6: Code Task (LangChain Callbacks)

Using LangChain's `ChatOpenAI` and a custom `@tool`, create a simple chain that binds one tool and invokes it with a user message. The tool should accept a city name and return a hardcoded population string.

---

### Exercise 7: Applied Task (Thread Grouping)

Create a three-turn conversation using the `trace()` context manager, where all three turns share the same `thread_id`. The conversation should be: (1) user introduces themselves, (2) user asks a question, (3) user says goodbye. Print each response.

---

### Exercise 8: Concept Question (Choosing a Method)

You are building an application that uses the OpenAI SDK directly (no LangChain). Which tracing mechanism would you use and why? What if you later decide to switch to LangChain — how does your tracing approach change?

---

## Answer Key

---

### Exercise 1: Concept Question (Tracing Mechanisms)

**Answer:**
1. **`wrap_openai`** — Use when you're calling the OpenAI SDK directly and want all calls traced automatically without decorating each function.
2. **`trace()` context manager** — Use when you need manual control over which operations are grouped into a trace and want to add custom metadata.
3. **LangChain callbacks** — Use when you're building chains, agents, or retrievers with LangChain and want the full execution tree traced automatically.

---

### Exercise 2: Concept Question (wrap_openai)

**Answer:** The `@traceable` decorator traces a single function, while `wrap_openai` traces every API call made through the wrapped client. If you're making many OpenAI calls across different functions, `wrap_openai` is more convenient — you wrap the client once and all calls are traced, rather than decorating each function individually.

---

### Exercise 3: Concept Question (thread_id)

**Answer:** A `thread_id` is a metadata tag that groups related runs into a single conversation thread in LangSmith. It's useful for chat applications where you want to see the full multi-turn conversation as one unit rather than as separate, disconnected traces. For example, a customer support bot handling a conversation would tag each turn with the same `thread_id` so the agent can review the entire interaction.

---

### Exercise 4: Code Task (wrap_openai)

**Answer:**

```python
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = wrap_openai(OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
))

questions = [
    "What is the capital of Japan?",
    "What is 12 times 15?",
    "Name a programming language that starts with P."
]

for q in questions:
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[{"role": "user", "content": q}]
    )
    print(f"Q: {q}")
    print(f"A: {response.choices[0].message.content}\n")
```

---

### Exercise 5: Code Task (trace() Context Manager)

**Answer:**

```python
from langsmith import trace
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_fact_and_question(topic):
    with trace("fact_and_question") as ts:
        # Generate a fact
        fact_response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[{"role": "user", "content": f"Give me one interesting fact about {topic}."}]
        )
        fact = fact_response.choices[0].message.content

        # Generate a question about the fact
        question_response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[{"role": "user", "content": f"Based on this fact, generate a quiz question: {fact}"}]
        )
        question = question_response.choices[0].message.content

    return fact, question

fact, question = generate_fact_and_question("the ocean")
print(f"Fact: {fact}")
print(f"Question: {question}")
```

---

### Exercise 6: Code Task (LangChain Callbacks)

**Answer:**

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

@tool
def get_population(city: str) -> str:
    """Return the population of a given city."""
    populations = {
        "New York": "8.3 million",
        "London": "8.9 million",
        "Tokyo": "13.9 million",
    }
    return f"The population of {city} is approximately {populations.get(city, 'unknown')}."

llm = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

llm_with_tools = llm.bind_tools([get_population])
response = llm_with_tools.invoke([HumanMessage(content="What is the population of Tokyo?")])
print(f"Response: {response.content}")
```

---

### Exercise 7: Applied Task (Thread Grouping)

**Answer:**

```python
from langsmith import trace
from openai import OpenAI
from dotenv import load_dotenv
import os, uuid

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

thread_id = str(uuid.uuid4())
model = "nvidia/nemotron-3-super-120b-a12b:free"

# Turn 1: User introduces themselves
with trace("turn_1", metadata={"thread_id": thread_id}) as ts:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hi, my name is Bob."}
        ]
    )
    print(f"Turn 1: {response.choices[0].message.content}")

# Turn 2: User asks a question
with trace("turn_2", metadata={"thread_id": thread_id}) as ts:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hi, my name is Bob."},
            {"role": "assistant", "content": "Hello Bob! How can I help you today?"},
            {"role": "user", "content": "What's the weather like?"}
        ]
    )
    print(f"Turn 2: {response.choices[0].message.content}")

# Turn 3: User says goodbye
with trace("turn_3", metadata={"thread_id": thread_id}) as ts:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hi, my name is Bob."},
            {"role": "assistant", "content": "Hello Bob! How can I help you today?"},
            {"role": "user", "content": "What's the weather like?"},
            {"role": "assistant", "content": "I'm sorry, I don't have access to weather data."},
            {"role": "user", "content": "Thanks anyway, goodbye!"}
        ]
    )
    print(f"Turn 3: {response.choices[0].message.content}")
```

---

### Exercise 8: Concept Question (Choosing a Method)

**Answer:** If you're using the OpenAI SDK directly, use `wrap_openai` — it traces all calls through the client with zero per-function setup. If you later switch to LangChain, you'd move to LangChain's callback tracer (or `@traceable` on chain functions), which traces the full chain execution tree including tool calls and nested operations. The `trace()` context manager remains available for any manual grouping needs regardless of which SDK you use.

---

## Summary

This assignment tested your understanding of:
- The three tracing mechanisms: `wrap_openai`, `trace()` context manager, and LangChain callbacks
- When to use each mechanism based on your SDK and tracing needs
- How `thread_id` metadata groups related runs into conversation threads
- Practical application of each mechanism with code examples
