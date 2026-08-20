# Lab 5: Writing Custom Evaluators — Assignment

## Exercises

Complete these exercises after finishing the lab. You should be able to answer them from the lab content alone, without re-running the notebook.

---

### Exercise 1: Concept Question (Evaluator Categories)

Name the three categories of evaluators in LangSmith. For each one, describe how it produces a score and give one example use case from this lab.

---

### Exercise 2: Concept Question (Evaluator Signature)

What is the required function signature for a LangSmith evaluator? What two arguments does it receive, and what must it return?

---

### Exercise 3: Code Task (Schema Validator)

Write a Pydantic model called `MovieReview` with fields `title` (str), `year` (int), and `rating` (1-5). Then write a schema validator evaluator that checks whether a run's output parses against this model. Return `{"key": "movie_schema_valid", "score": True/False}`.

---

### Exercise 4: Code Task (LLM-as-Judge)

Write an LLM-as-judge evaluator called `clarity_judge` that receives a run and example, then asks an LLM to score the output's clarity on a 1-5 scale. The prompt should include the original input, the agent's output, and a reference answer. Return `{"key": "clarity", "score": <int>, "comment": "<reason>"}`.

---

### Exercise 5: Concept Question (Heuristic vs LLM-as-Judge)

Why would you use a heuristic evaluator instead of an LLM-as-judge for schema validation? List three advantages of heuristic evaluators over LLM-as-judge evaluators.

---

### Exercise 6: Code Task (Guardrail Evaluator)

Write a guardrail evaluator that checks whether an agent's output meets these three policies:
1. The output must not exceed 500 characters
2. The output must contain at least one complete sentence (ends with a period, question mark, or exclamation point)
3. The output must not contain the word "sorry"

Return a boolean score with a comment listing any violations.

---

### Exercise 7: Concept Question (evaluate() API)

When you call `evaluate()` with multiple evaluators, what happens internally? Describe the flow from dataset loading to score collection in 3-4 sentences.

---

### Exercise 8: Applied Task (Evaluation Pipeline)

You're building a customer support chatbot. Design an evaluation pipeline with exactly four evaluators:
1. One heuristic evaluator
2. One LLM-as-judge evaluator
3. One guardrail evaluator
4. One custom evaluator of your choice

For each evaluator, describe: what it checks, how it produces a score, and why that category is the right fit for this particular check.

---

## Answer Key

---

### Exercise 1: Concept Question (Evaluator Categories)

**Answer:**
1. **Heuristic (rule-based)** — Uses pure logic, no LLM calls. Checks structural properties like schema validity, value ranges, or required fields. Example: the `schema_validator` checks if output parses against `ProductReview` Pydantic model.
2. **LLM-as-judge** — Calls a separate LLM to score output quality. Useful for subjective metrics. Example: the `helpfulness_judge` asks an LLM to score extraction quality from 1-5.
3. **Custom function** — Combines arbitrary Python logic, external calls, or domain rules. Example: the `guardrail_checker` enforces sentiment, rating, and product policies through conditional logic.

---

### Exercise 2: Concept Question (Evaluator Signature)

**Answer:** The signature is `def evaluator(run, example) -> dict`. It receives:
- `run` — contains the target function's output (`run.outputs`)
- `example` — contains the dataset's input (`example.inputs`) and expected output (`example.outputs`)

It must return a dict with:
- `key` (required) — metric name string
- `score` (required) — the score value (bool, int, or float)
- `comment` (optional) — human-readable explanation

---

### Exercise 3: Code Task (Schema Validator)

**Answer:**

```python
from pydantic import BaseModel, Field, ValidationError

class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    year: int = Field(description="Release year")
    rating: int = Field(description="Rating from 1 to 5")

def movie_schema_validator(run, example) -> dict:
    output = run.outputs
    try:
        MovieReview(**output)
        return {"key": "movie_schema_valid", "score": True}
    except ValidationError as e:
        return {"key": "movie_schema_valid", "score": False, "comment": str(e)}
```

---

### Exercise 4: Code Task (LLM-as-Judge)

**Answer:**

```python
def clarity_judge(run, example) -> dict:
    input_text = example.inputs
    output = run.outputs
    reference = example.outputs

    prompt = f"""Score the following output on a 1-5 clarity scale.
Input: {input_text}
Output: {output}
Reference: {reference}
Return ONLY a JSON object: {{"score": <int>, "reason": "<brief explanation>"}}"""

    response = judge_client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    import json
    result = json.loads(response.choices[0].message.content)
    return {"key": "clarity", "score": result["score"], "comment": result["reason"]}
```

---

### Exercise 5: Concept Question (Heuristic vs LLM-as-Judge)

**Answer:** Three advantages of heuristic evaluators:
1. **Speed** — Heuristic checks run in microseconds; LLM-as-judge requires a network call that takes seconds.
2. **Cost** — Heuristic evaluators are free; LLM-as-judge incurs API costs for every example evaluated.
3. **Determinism** — Heuristic evaluators always return the same result for the same input; LLM-as-judge can produce different scores across runs due to model variance.

---

### Exercise 6: Code Task (Guardrail Evaluator)

**Answer:**

```python
def content_guardrails(run, example) -> dict:
    output = run.outputs.get("content", str(run.outputs))
    violations = []

    if len(output) > 500:
        violations.append(f"Exceeds 500 characters ({len(output)} chars)")
    if not output.rstrip().endswith((".", "!", "?")):
        violations.append("Missing complete sentence ending")
    if "sorry" in output.lower():
        violations.append("Contains forbidden word 'sorry'")

    return {
        "key": "content_guardrails",
        "score": len(violations) == 0,
        "comment": "; ".join(violations) if violations else "All guardrails passed"
    }
```

---

### Exercise 7: Concept Question (evaluate() API)

**Answer:** Internally, `evaluate()` does the following:
1. Loads all examples from the specified dataset
2. For each example, calls the target function with the example's input, creating a run
3. For each run, passes it along with the original example to every evaluator function
4. Collects all evaluator scores, groups them by example, and logs the results to LangSmith as an experiment

---

### Exercise 8: Applied Task (Evaluation Pipeline)

**Answer:**
1. **Heuristic: response_length** — Checks that the response is between 50 and 2000 characters. Heuristic is right because length is a measurable numeric property with no ambiguity.
2. **LLM-as-judge: empathy_score** — Asks an LLM to rate how empathetic and understanding the response sounds on a 1-5 scale. LLM-as-judge is right because empathy is subjective and requires understanding tone and emotional context.
3. **Guardrail: no_refusal_without_reason** — Checks that if the bot declines a request, it provides an explanation. Guardrail is right because this is a hard business policy that must always be enforced.
4. **Custom: SLA_compliance** — Checks that the response was generated within the configured SLA time window by comparing timestamps. Custom is right because it requires external time data and business logic that doesn't fit neatly into other categories.

---

## Summary

This assignment tested your understanding of:
- The three evaluator categories (heuristic, LLM-as-judge, custom)
- The evaluator function signature and return format
- Schema validation with Pydantic
- LLM-as-judge prompt design
- Guardrail policy enforcement
- The `evaluate()` API orchestration flow
- Matching evaluator categories to use cases
