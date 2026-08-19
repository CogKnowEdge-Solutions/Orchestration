# Lab 3: Building & Managing Datasets — Assignment

## Exercises

Complete these exercises after finishing the lab. You should be able to answer them from the lab content alone, without re-running the notebook.

---

### Exercise 1: Concept Question (Dataset Structure)

What are the three core components of a LangSmith dataset? Describe each one and give an example of what it contains in the context of this lab's product review data.

---

### Exercise 2: Concept Question (Four Creation Methods)

List the four ways to create examples in a LangSmith dataset. For each method, describe when you would use it and give a one-sentence example.

---

### Exercise 3: Code Task (Create Dataset)

Write Python code that creates a new LangSmith dataset called `movie-reviews` with a description "Movie reviews with structured output". Then add two examples: one input with a movie review and one output with the structured `Movie` schema (title, director, year).

---

### Exercise 4: Code Task (Add Examples from Structured Output)

Write Python code that takes a list of 3 review texts, runs the structured-output agent on each one, and adds them as examples to an existing dataset. Each example should have `review_text` as input and the structured output as the expected answer.

---

### Exercise 5: Concept Question (Trace-to-Dataset)

Why is converting traces into examples considered the "most common real-world workflow" for building datasets? What advantage does this approach have over manually writing examples?

---

### Exercise 6: Code Task (CSV Import)

Write Python code that:
1. Creates a CSV file with 2 rows of movie review data (columns: `input`, `output`)
2. Reads the CSV back
3. Imports each row as an example into a new LangSmith dataset called `movie-reviews-csv`

---

### Exercise 7: Concept Question (Splits)

What are splits in a LangSmith dataset? Why would you organize examples into splits like `train` and `test`? How does this affect evaluation runs?

---

### Exercise 8: Applied Task (Dataset Versioning)

If you add 5 new examples to an existing dataset, what happens to the previous version of the dataset? Can you roll back to the previous version? Explain how LangSmith handles dataset versioning.

---

## Answer Key

---

### Exercise 1: Concept Question (Dataset Structure)

**Answer:**
1. **Dataset** — A named collection of examples (e.g., `product-reviews`). It has a name, description, and unique ID.
2. **Example** — A single input/output pair (e.g., one review text and its structured `ProductReview` output). Examples are the atomic units of a dataset.
3. **Split** — A named subset of examples (e.g., `train`, `test`). Examples are tagged with split metadata so evaluations can target specific subsets.

---

### Exercise 2: Concept Question (Four Creation Methods)

**Answer:**
1. **Programmatic (SDK)** — Use `client.create_examples()` to add examples directly in Python. Best when you have structured data already in code.
2. **From Traces** — Query existing traces with `client.list_runs()` and convert their inputs/outputs. Best for capturing real system behavior.
3. **CSV Import** — Upload a CSV file with input/output columns. Best for sharing datasets with non-technical team members or importing from spreadsheets.
4. **Manual (UI)** — Create examples through the LangSmith web interface. Best for quick, one-off additions without writing code.

---

### Exercise 3: Code Task (Create Dataset)

**Answer:**

```python
from langsmith import Client

ls_client = Client()

# Create the dataset
dataset = ls_client.create_dataset(
    dataset_name="movie-reviews",
    description="Movie reviews with structured output"
)

# Add examples
ls_client.create_examples(
    dataset_id=dataset.id,
    inputs={"review_text": "Inception is a mind-bending masterpiece. Five stars."},
    outputs={"title": "Inception", "director": "Christopher Nolan", "year": 2010},
)

ls_client.create_examples(
    dataset_id=dataset.id,
    inputs={"review_text": "The Dark Knight is the best superhero movie ever. Five stars."},
    outputs={"title": "The Dark Knight", "director": "Christopher Nolan", "year": 2008},
)
```

---

### Exercise 4: Code Task (Add Examples from Structured Output)

**Answer:**

```python
review_texts = [
    "The 'Premium Blender' is fantastic. Five stars.",
    "My 'Laptop Stand' wobbles constantly. Two stars.",
    "The 'Ceramic Mug Set' looks nice but one arrived chipped. Three stars.",
]

structured_model = model.with_structured_output(ProductReview)

parsed_reviews = []
for review_text in review_texts:
    parsed = structured_model.invoke(review_text)
    parsed_reviews.append(parsed)

for review_text, parsed in zip(review_texts, parsed_reviews):
    ls_client.create_examples(
        dataset_id=dataset.id,
        inputs={"review_text": review_text},
        outputs=parsed.model_dump(),
    )
```

---

### Exercise 5: Concept Question (Trace-to-Dataset)

**Answer:** Converting traces is the most common workflow because it captures real system behavior, not idealized inputs. When you run your system in production or testing, the traces contain the actual inputs your system received and the actual outputs it produced. This gives you ground-truth data that reflects real usage patterns, edge cases, and failure modes — something manually written examples often miss.

---

### Exercise 6: Code Task (CSV Import)

**Answer:**

```python
import pandas as pd
import ast

# Create CSV
csv_data = pd.DataFrame({
    "input": [
        {"review_text": "Inception is a masterpiece. Five stars."},
        {"review_text": "The Dark Knight is incredible. Five stars."},
    ],
    "output": [
        {"title": "Inception", "director": "Christopher Nolan", "year": 2010},
        {"title": "The Dark Knight", "director": "Christopher Nolan", "year": 2008},
    ],
})
csv_data.to_csv("movie_reviews.csv", index=False)

# Import into LangSmith
csv_df = pd.read_csv("movie_reviews.csv")
csv_dataset = ls_client.create_dataset(
    dataset_name="movie-reviews-csv",
    description="Movie reviews imported from CSV"
)

for _, row in csv_df.iterrows():
    ls_client.create_examples(
        dataset_id=csv_dataset.id,
        inputs=ast.literal_eval(row["input"]),
        outputs=ast.literal_eval(row["output"]),
    )
```

---

### Exercise 7: Concept Question (Splits)

**Answer:** Splits are named subsets of examples within a dataset (e.g., `train`, `test`). You organize examples into splits so you can run evaluations on specific subsets — for example, evaluating your system only on the `test` split to measure generalization. This keeps your training data separate from your evaluation data, preventing data leakage and giving you more accurate performance metrics.

---

### Exercise 8: Applied Task (Dataset Versioning)

**Answer:** When you add new examples to an existing dataset, LangSmith creates a new version of the dataset. The previous version is preserved as a snapshot. You can roll back to any previous version through the LangSmith UI or SDK. This versioning is automatic — every change (adding, updating, or deleting examples) creates a new snapshot. This means you can compare evaluation results across dataset versions and track how your system's performance changes over time.

---

## Summary

This assignment tested your understanding of:
- LangSmith dataset structure (datasets, examples, splits)
- The four ways to create examples (SDK, traces, CSV, UI)
- Programmatic dataset creation with the SDK
- Converting traces into dataset examples
- CSV import workflow
- Split organization for evaluation
- Dataset versioning
