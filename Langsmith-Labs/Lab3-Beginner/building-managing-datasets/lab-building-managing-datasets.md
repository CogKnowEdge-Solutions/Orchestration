# Lab 3: Building & Managing Datasets

## Difficulty: Beginner | ~40 min | Requires LangChain Lab 3 (Structured Output)

Learn how LangSmith datasets are structured (input/output example pairs), and the different ways to create them: manually through the UI, programmatically via the SDK, by converting existing traces into examples, or by importing a CSV. Cover dataset versioning and organizing examples into splits (e.g., train/test).

---

## 2. Problem Statement / Use Case Overview

When you evaluate an LLM-powered system, you need a collection of known inputs and expected outputs — a **dataset**. Without one, you're eyeballing responses. With one, you can systematically measure whether your system gets better or worse over time.

LangSmith datasets store these input/output example pairs and let you version them, split them into train/test subsets, and use them in automated evaluation runs. This lab shows you how to build a dataset from scratch: first by creating examples manually via the SDK, then by converting traces you already captured, and finally by importing a CSV file. By the end, you'll have a 15–20 example dataset organized into two splits, ready for evaluation in later labs.

---

## 3. Input Data

- **15–20 product review texts** — short, varied reviews that you'll feed into the structured-output agent from LangChain Lab 3
- **Structured output schema** — the `ProductReview` Pydantic model (product, rating, sentiment) from LangChain Lab 3
- **No external files required** — all review texts are defined inline in the notebook
- **CSV import demo** — a small synthetic CSV file created in-notebook to demonstrate the import path

---

## 4. Processing

1. **Generate structured outputs** — Run the structured-output agent across 15–20 varied review inputs to produce typed `ProductReview` objects
2. **Create examples from traces** — Query LangSmith for the traces generated in step 1, then convert each trace's input/output into a LangSmith example
3. **Create examples manually** — Build example objects directly in Python using the SDK's `create_examples()` method
4. **Import from CSV** — Write a CSV file with input/output columns and import it as a new dataset
5. **Organize into splits** — Tag examples with split metadata (e.g., "train" or "test") for structured evaluation later

---

## 5. Output

After completing this lab, you will have:

- A LangSmith dataset named `product-reviews` containing 13 examples
- Each example has an input (review text) and output (structured `ProductReview` dict with product, rating, sentiment)
- A second dataset (`product-reviews-from-traces`) created by converting traces
- A third dataset (`product-reviews-csv`) created by importing a CSV file, with train/test splits
- All three datasets visible in the LangSmith UI under the **Datasets** tab

### What to Expect in LangSmith UI

| Dataset | Examples | Source | Splits |
|---------|----------|--------|--------|
| `product-reviews` | 13 | SDK (10 generated + 3 manual) | None |
| `product-reviews-from-traces` | varies | Converted from LLM traces | None |
| `product-reviews-csv` | 3 | CSV import | train, test |

---

## 6. Tech Stack

- **langsmith** `>=0.1.0` — SDK for dataset creation, management, and trace conversion
- **langchain** `1.2.15` — framework providing `with_structured_output()`
- **langchain-core** `1.2.28` — shared foundation
- **langchain-openai** `1.1.12` — `ChatOpenAI` wrapper for OpenRouter
- **python-dotenv** `1.2.2` — loads `.env` files
- **pydantic** `2.13.4` — schema classes (`BaseModel`, `Field`)
- **pandas** `>=2.0.0` — CSV handling for the import demo
- **OpenRouter API** — free tier, model `nvidia/nemotron-3-super-120b-a12b:free`
- **LangSmith** — hosted service for tracing and datasets

---

## 7. Underlying Concepts

### What is a LangSmith Dataset?

A LangSmith **dataset** is a named collection of **examples**. Each example is an input/output pair:

- **input** — the text, dict, or object you send to your system
- **output** — the expected or ground-truth response

Datasets live in your LangSmith workspace and are versioned: every change creates a new snapshot, so you can roll back or compare across versions.

### The Example Lifecycle

```mermaid
graph LR
    A["Create Examples"] --> B["Store in Dataset"]
    B --> C["Version Dataset"]
    C --> D["Split into Train/Test"]
    D --> E["Use in Evaluation"]
    
    style A fill:#1565c0,color:#fff
    style B fill:#bf360c,color:#fff
    style C fill:#2e7d32,color:#fff
    style D fill:#6a1b9a,color:#fff
    style E fill:#c62828,color:#fff
```

### Four Ways to Create Examples

1. **Programmatic (SDK)** — Use `client.create_examples()` to add examples directly in Python
2. **From Traces** — Query existing traces in LangSmith and convert their inputs/outputs into dataset examples
3. **CSV Import** — Upload a CSV file with input/output columns
4. **Manual (UI)** — Create examples through the LangSmith web interface (not covered in this lab)

### Splits

Datasets can be organized into **splits** — named subsets like `train` and `test`. When you run an evaluation, you can target a specific split, keeping your training data separate from your test data. Each example carries a `split` metadata field.

### Why Datasets Matter for Evaluation

Without datasets, evaluating an LLM is subjective ("this response looks good"). With datasets, evaluation becomes systematic: you can measure accuracy, consistency, and regression across known inputs/outputs. This lab builds the dataset that later evaluation labs will consume.

---

## 8. Prerequisites

- **LangChain Lab 3** (Structured Output) — the structured-output agent pattern is reused here
- **LangSmith Lab 1** (Tracing Basics) — understanding traces and the `@traceable` decorator
- A **LangSmith account** with an API key (free tier works)
- An **OpenRouter API key** (free tier works)
- Python 3.11+

---

## 9. Environment / Dependencies Setup

1. Create a fresh virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -qU "langsmith>=0.1.0" "langchain==1.2.15" "langchain-core==1.2.28" "langchain-openai==1.1.12" "python-dotenv==1.2.2" "pydantic==2.13.4" "pandas>=2.0.0"
   ```

3. Create a `.env` file with your keys:
   ```
   OPENROUTER_API_KEY=your_openrouter_key_here
   LANGSMITH_API_KEY=your_langsmith_key_here
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=lab-3-datasets
   ```

4. Verify the setup by running the first cell of the notebook.

---

## 10. Step-wise Development Instructions

### Step 1: Install dependencies

```python
# Install all required packages at pinned versions for reproducibility
!pip install -qU "langsmith>=0.1.0" "langchain==1.2.15" "langchain-core==1.2.28" "langchain-openai==1.1.12" "python-dotenv==1.2.2" "pydantic==2.13.4" "pandas>=2.0.0"
```

This installs the exact versions of every library used in this lab.

---

### Step 2: Load environment variables

```python
import os
from dotenv import load_dotenv
from langsmith import Client

# Load API keys from .env file
load_dotenv()

# Verify required keys are present — fail early with a clear message
assert os.getenv("OPENROUTER_API_KEY"), "Missing OPENROUTER_API_KEY in .env"
assert os.getenv("LANGSMITH_API_KEY"), "Missing LANGSMITH_API_KEY in .env"

# Initialize the LangSmith client (talks to LangSmith's servers)
ls_client = Client()
print("Environment loaded and LangSmith client initialized")
```

Loads API keys from `.env` and initializes the LangSmith client — this is what talks to LangSmith's servers for dataset operations.

---

### Step 3: Set up the structured-output agent

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Create the LLM client pointing to OpenRouter (free tier)
model = ChatOpenAI(
    model="nvidia/nemotron-3.5-lightning:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,  # Deterministic output for consistent dataset entries
)

# Schema that defines what structured data we want from each review
class ProductReview(BaseModel):
    product: str = Field(description="The exact product being reviewed")
    rating: int = Field(description="The star rating, from 1 to 5")
    sentiment: str = Field(description="positive, negative, or neutral")
```

This sets up the structured-output agent from LangChain Lab 3. The `ProductReview` schema defines the shape we want for each example in our dataset.

---

### Step 4: Generate structured outputs from review texts

```python
# 10 varied product reviews covering different ratings and sentiments
review_texts = [
    "I bought the 'AeroPress Coffee Maker' two weeks ago. Best coffee ever. Five stars.",
    "The 'Ergonomic Office Chair' arrived broken. Customer service never replied. One star.",
    "My 'Wireless Noise-Cancelling Headphones' are great value. Four stars.",
    "The 'Smart Fitness Tracker' stopped working after three days. Two stars.",
    "Love the 'Portable Bluetooth Speaker' — loud, clear, waterproof. Five stars.",
    "The 'Organic Green Tea' tastes stale. Box was damaged. Two stars.",
    "My 'Mechanical Keyboard' is a dream to type on. Five stars.",
    "The 'Bamboo Cutting Board' cracked after one week. One star.",
    "Great 'LED Desk Lamp' — adjustable brightness, USB port. Four stars.",
    "My 'Running Shoes' are lightweight and supportive. Five stars.",
]

# Bind the Pydantic schema to the model so it returns ProductReview objects
structured_model = model.with_structured_output(ProductReview)

# Run the structured-output agent on each review to extract fields
parsed_reviews = []
for review_text in review_texts:
    parsed = structured_model.invoke(review_text)
    parsed_reviews.append(parsed)

# Preview the first 5 parsed results
for p in parsed_reviews[:5]:
    print(f"{p.product} | rating {p.rating}/5 | {p.sentiment}")
print(f"\nParsed {len(parsed_reviews)} reviews into structured objects")
```

These 10 reviews cover a range of products, ratings (1-5), and sentiments. Running the structured-output agent on each produces typed `ProductReview` objects — the ground-truth data for our dataset.

---

### Step 5: Create a dataset and add examples from the structured outputs

```python
# Clean up any existing datasets with these names (idempotent re-runs)
for ds_name in ["product-reviews", "product-reviews-from-traces", "product-reviews-csv"]:
    try:
        existing = ls_client.read_dataset(dataset_name=ds_name)
        ls_client.delete_dataset(dataset_id=existing.id)
        print(f"  Deleted existing dataset: {ds_name}")
    except Exception:
        pass  # Dataset doesn't exist yet, nothing to delete

# Create a new empty dataset in LangSmith
dataset = ls_client.create_dataset(
    dataset_name="product-reviews",
    description="Product reviews with structured output (product, rating, sentiment)"
)

# Batch-add all examples at once: inputs and outputs are lists of dicts
ls_client.create_examples(
    dataset_id=dataset.id,
    inputs=[{"review_text": rt} for rt in review_texts],      # raw review as input
    outputs=[p.model_dump() for p in parsed_reviews],          # structured output as expected answer
)

print(f"Created dataset '{dataset.name}' with {len(parsed_reviews)} examples")
```

This creates an empty dataset in LangSmith, then adds each review as an example: the raw review text as input, the structured output as the expected answer. This input/output pairing is the foundation for evaluation.

---

### Step 6: Create examples manually via the SDK

```python
# Manually defined inputs and expected outputs (no LLM needed)
manual_inputs = [
    {"review_text": "The 'Premium Blender' is fantastic. Five stars."},
    {"review_text": "My 'Laptop Stand' wobbles constantly. Two stars."},
    {"review_text": "The 'Ceramic Mug Set' looks nice but one arrived chipped. Three stars."},
]
manual_outputs = [
    {"product": "Premium Blender", "rating": 5, "sentiment": "positive"},
    {"product": "Laptop Stand", "rating": 2, "sentiment": "negative"},
    {"product": "Ceramic Mug Set", "rating": 3, "sentiment": "neutral"},
]

# Add them to the same dataset using create_examples()
ls_client.create_examples(
    dataset_id=dataset.id,
    inputs=manual_inputs,
    outputs=manual_outputs,
)
print(f"Added {len(manual_inputs)} manual examples. Total: {len(parsed_reviews) + len(manual_inputs)}")
```

This is the manual approach: you write the inputs and expected outputs yourself. Useful when you have existing ground-truth data or want to add specific edge cases.

---

### Step 7: Convert traces into examples

```python
# Query existing LLM traces from LangSmith (these were captured during Step 4)
traces = list(ls_client.list_runs(
    project_name=os.getenv("LANGSMITH_PROJECT"), run_type="llm", limit=20
))

# Create a separate dataset for the trace-based examples
trace_dataset = ls_client.create_dataset(
    dataset_name="product-reviews-from-traces",
    description="Dataset created by converting LangSmith traces into examples"
)

# Filter to only traces that have both inputs and outputs (skip incomplete ones)
valid_traces = [t for t in traces if t.inputs and t.outputs]
if valid_traces:
    ls_client.create_examples(
        dataset_id=trace_dataset.id,
        inputs=[t.inputs for t in valid_traces],    # trace inputs become example inputs
        outputs=[t.outputs for t in valid_traces],   # trace outputs become expected outputs
    )

print(f"Converted {len(valid_traces)} traces into '{trace_dataset.name}'")
```

This is the trace-to-dataset pattern: query your traces, then map their inputs and outputs into examples. This is the most common way datasets are built in practice.

---

### Step 8: Import examples from a CSV file

```python
import pandas as pd
import ast

# Build a small DataFrame with input/output columns (simulates a real export)
csv_data = pd.DataFrame({
    "input": [
        {"review_text": "The 'Standing Desk' is sturdy. Five stars."},
        {"review_text": "My 'Air Purifier' rattles. Two stars."},
        {"review_text": "The 'Travel Mug' keeps coffee hot. Four stars."},
    ],
    "output": [
        {"product": "Standing Desk", "rating": 5, "sentiment": "positive"},
        {"product": "Air Purifier", "rating": 2, "sentiment": "negative"},
        {"product": "Travel Mug", "rating": 4, "sentiment": "positive"},
    ],
})

# Write to CSV, then read it back (mimics importing from an external source)
csv_data.to_csv("reviews.csv", index=False)
csv_df = pd.read_csv("reviews.csv")

# Create a new dataset for the CSV-imported examples
csv_dataset = ls_client.create_dataset(
    dataset_name="product-reviews-csv",
    description="Dataset imported from a CSV file"
)

# Pandas stores dicts as strings in CSV — convert them back to actual dicts
csv_inputs = [ast.literal_eval(row["input"]) for _, row in csv_df.iterrows()]
csv_outputs = [ast.literal_eval(row["output"]) for _, row in csv_df.iterrows()]

# Import all rows as examples in one batch
ls_client.create_examples(
    dataset_id=csv_dataset.id,
    inputs=csv_inputs,
    outputs=csv_outputs,
)

print(f"Imported {len(csv_df)} examples from CSV into '{csv_dataset.name}'")
```

This writes a small CSV, reads it back, and imports each row as a dataset example. In practice, you'd export this from an existing system or spreadsheet.

---

### Step 9: Organize examples into splits

```python
# List all examples in the CSV dataset
all_examples = list(ls_client.list_examples(dataset_id=csv_dataset.id))

# Calculate 80/20 train/test split
split_idx = int(len(all_examples) * 0.8)

# Tag each example with its split using update_example()
for ex in all_examples[:split_idx]:
    ls_client.update_example(example_id=ex.id, split="train")
for ex in all_examples[split_idx:]:
    ls_client.update_example(example_id=ex.id, split="test")

print(f"Split {split_idx} into train, {len(all_examples) - split_idx} into test")
```

Splits let you organize examples into named subsets. When you run an evaluation, you can target a specific split (e.g., only run on test data).

---

### Step 10: Verify the dataset in LangSmith

```python
# Re-read the dataset to verify everything looks correct
csv_dataset = ls_client.read_dataset(dataset_name="product-reviews-csv")
all_examples = list(ls_client.list_examples(dataset_id=csv_dataset.id))

# Filter examples by their split metadata
train = [e for e in all_examples if e.metadata.get("dataset_split", ["base"])[0] == "train"]
test = [e for e in all_examples if e.metadata.get("dataset_split", ["base"])[0] == "test"]

print(f"Dataset: {csv_dataset.name}")
print(f"  Total examples: {len(all_examples)}")
print(f"  Train: {len(train)} | Test: {len(test)}")

# Show a sample to confirm inputs/outputs look right
sample = all_examples[0]
print(f"\nSample (ID: {sample.id}):")
print(f"  Input: {sample.inputs}")
print(f"  Output: {sample.outputs}")
print(f"  Split: {sample.metadata.get('dataset_split', ['base'])[0]}")
```

This prints a summary of your dataset: total examples, count per split, and a sample.

### Step 11: Verify in the LangSmith UI

Open [https://smith.langchain.com](https://smith.langchain.com) and check the following:

**Datasets tab** (left sidebar → Datasets):
- `product-reviews` — should show 13 examples (10 generated + 3 manual). Click into it to see each input/output pair.
- `product-reviews-from-traces` — examples converted from your LLM traces. The count depends on how many traces had both inputs and outputs.
- `product-reviews-csv` — should show 3 examples imported from CSV, with train/test split labels visible in the split column.

**Traces tab** (left sidebar → your project `lab-3-datasets`):
- You should see LLM traces from Step 4 (the structured-output agent runs on 10 reviews). Each trace shows the input review text and the structured output.

**What to click:**
1. Go to **Datasets** → click `product-reviews` → you'll see a table of all 13 examples with Input and Output columns
2. Click any example row to expand it — verify the input is review text and the output is a `{product, rating, sentiment}` dict
3. Go back to Datasets → click `product-reviews-csv` → check that the Split column shows "train" or "test" for each example
4. Go to **Traces** → find your project → click any LLM trace → you should see the review text as input and the model's structured response as output

If all three datasets appear with correct inputs/outputs, Lab 3 is complete. These datasets are consumed by Lab 5 (Writing Custom Evaluators) and Lab 6 (Running Experiments).

---

## 11. Optional Exercise

Create a third dataset by writing 10 movie descriptions (similar to the `Movie` schema from LangChain Lab 3) to a CSV file with columns `input` and `output`, then import it into LangSmith using the CSV import pattern from Step 9. Organize the examples into a `test` split and verify the dataset appears in your LangSmith workspace.

---

## 12. What We Learnt

- **Datasets are collections of input/output example pairs** — the foundation for systematic LLM evaluation
- **Four ways to create examples**: programmatically via SDK, from existing traces, from CSV files, or manually in the UI
- **The SDK pattern**: `client.create_dataset()` to create a dataset, `client.create_examples()` to add data to it
- **Trace-to-dataset conversion**: query traces with `client.list_runs()` and map their inputs/outputs to examples
- **CSV import**: read a structured file with pandas and upload it via the SDK
- **Splits organize data** into train/test subsets for targeted evaluation
- **Versioning is automatic**: every change to a dataset creates a new snapshot
- **Datasets bridge development and evaluation** — you build them during development, consume them during evaluation
