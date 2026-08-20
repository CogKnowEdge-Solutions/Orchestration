# Lab 6: Running Experiments — Assignment

## Exercises

Complete these exercises after finishing the lab. You should be able to answer them from the lab content alone, without re-running the notebook.

---

### Exercise 1: Concept Question (What is an Experiment)

In your own words, what does `evaluate()` do when called with a dataset name and a list of evaluators? Describe the flow from dataset loading to score collection in 3-4 sentences.

---

### Exercise 2: Concept Question (Experiment Metadata)

What is the purpose of the `experiment_prefix` and `metadata` parameters in `evaluate()`? Give one example of a metadata dict you might attach to an experiment comparing two different LLM models.

---

### Exercise 3: Code Task (Middleware Target Function)

Write a target function called `target_with_lowercase_middleware` that converts the entire review text to lowercase before passing it to the structured model. The function should take `inputs` dict and return the parsed `ProductReview` as a dict. Assume `structured_model` is already defined.

---

### Exercise 4: Concept Question (Controlled Comparison)

Why is it important to change only *one* variable between two experiments? What goes wrong if you change the model *and* the middleware between experiments and the scores differ?

---

### Exercise 5: Code Task (Fourth Evaluator)

Write a heuristic evaluator called `product_not_empty` that checks whether the `product` field in the output is a non-empty string (not just whitespace). Return `{"key": "product_not_empty", "score": True/False}`. Then show how you'd attach it to an `evaluate()` call.

---

### Exercise 6: Applied Task (RAG Experiment Design)

You're comparing a RAG pipeline with and without a query-rewriting step. Describe:
1. The two target functions (what each does)
2. Three evaluators you'd use and why each category (heuristic, LLM-as-judge, custom) fits
3. The metadata dict you'd attach to each experiment

---

### Exercise 7: Concept Question (Finding Experiments in LangSmith)

After running two experiments, how would you find and compare them in the LangSmith UI? What role does `experiment_prefix` play in this process?

---

### Exercise 8: Applied Task (Interpreting Results)

You run two experiments — with and without middleware — and find that helpfulness scores are identical (4.2/5 both) but the guardrail pass rate drops from 100% to 85% without middleware. What does this tell you about the middleware's effect? What would you investigate next?

---

## Answer Key

---

### Exercise 1: Concept Question (What is an Experiment)

**Answer:** When you call `evaluate()` with a dataset name, LangSmith loads all examples from that dataset. For each example, it calls your target function with the example's input, creating a run. It then passes each run + example pair to every evaluator function. Finally, it groups all scores under a single named experiment and logs the results to LangSmith, giving you a complete quality snapshot of one configuration across the entire dataset.

---

### Exercise 2: Concept Question (Experiment Metadata)

**Answer:**
- `experiment_prefix` provides a human-readable name prefix for the experiment in LangSmith's UI, making it easy to find and identify later.
- `metadata` is an arbitrary dict of key-value pairs attached to the experiment for filtering and comparison.

**Example metadata dict comparing two models:**
```python
metadata={
    "model_a": "nvidia/nemotron-3.5-lightning:free",
    "model_b": "nvidia/nemotron-3-super-120b-a12b:free",
    "comparison_type": "model-swap",
    "temperature": 0
}
```

---

### Exercise 3: Code Task (Middleware Target Function)

**Answer:**

```python
def target_with_lowercase_middleware(inputs: dict) -> dict:
    """Target with lowercase middleware applied first."""
    lowercased = inputs["review_text"].lower()
    parsed = structured_model.invoke(lowercased)
    return parsed.model_dump()
```

---

### Exercise 4: Concept Question (Controlled Comparison)

**Answer:** Changing only one variable lets you attribute any score difference to that specific change. If you change both the model and the middleware, and scores improve, you can't tell which change caused the improvement — it could be the model, the middleware, or their interaction. This is a confounding variable problem. To know what caused the difference, you need to isolate each variable in separate experiments.

---

### Exercise 5: Code Task (Fourth Evaluator)

**Answer:**

```python
def product_not_empty(run, example) -> dict:
    """Check that the product field is a non-empty string."""
    product = run.outputs.get("product", "")
    return {"key": "product_not_empty", "score": bool(product.strip())}

# Attach to evaluate():
results = evaluate(
    target_with_middleware,
    data="product-reviews",
    evaluators=[schema_validator, helpfulness_judge, guardrail_checker, product_not_empty],
    experiment_prefix="lab6-with-four-evaluators",
)
```

---

### Exercise 6: Applied Task (RAG Experiment Design)

**Answer:**

1. **Target functions:**
   - `target_with_rewriting(inputs)` — rewrites the user query using an LLM to expand abbreviations and add context, then retrieves documents and generates an answer
   - `target_without_rewriting(inputs)` — takes the raw user query directly to retrieval and generation, no rewriting step

2. **Evaluators:**
   - **Heuristic: `answer_length`** — checks that the answer is between 50 and 2000 characters. Heuristic fits because length is a measurable numeric property with no ambiguity.
   - **LLM-as-judge: `relevance_score`** — asks an LLM to rate how relevant the answer is to the original question on a 1-5 scale. LLM-as-judge fits because relevance requires understanding semantic meaning.
   - **Custom: `citation_check`** — verifies that the answer includes at least one source reference from the retrieved documents. Custom fits because it requires checking external data (the retrieved docs) against the output.

3. **Metadata dicts:**
   - Experiment A: `{"query_rewrite": "enabled", "variant": "with"}`
   - Experiment B: `{"query_rewrite": "disabled", "variant": "without"}`

---

### Exercise 7: Concept Question (Finding Experiments in LangSmith)

**Answer:** In the LangSmith UI, navigate to the Experiments tab. Experiments are listed with their names (derived from `experiment_prefix`). You can filter experiments by metadata keys, sort by creation date, and select multiple experiments to compare their aggregate scores side by side. The `experiment_prefix` is what lets you quickly locate a specific experiment — without it, experiments are harder to find among many runs.

---

### Exercise 8: Applied Task (Interpreting Results)

**Answer:** This tells you the middleware has a meaningful effect on guardrail compliance — the text normalization step helps the model produce outputs that pass guardrails more consistently. The identical helpfulness scores suggest the middleware doesn't affect output quality in terms of extraction accuracy, but it does improve structural compliance.

**Next steps:**
- Examine the specific examples that failed guardrails without middleware to understand what pattern caused failures
- Check whether the failures are in sentiment prediction, rating extraction, or product name extraction
- Test whether a more aggressive middleware (e.g., also normalizing special characters) improves guardrail pass rate further
- Run both experiments again with `temperature > 0` to see if the middleware effect is consistent across multiple runs

---

## Summary

This assignment tested your understanding of:
- What `evaluate()` does at scale (full-dataset experiments)
- Experiment metadata and naming for comparison
- The controlled comparison methodology
- How to write middleware target functions
- How to extend evaluator sets
- Designing experiments for real-world scenarios
- Interpreting comparison results
