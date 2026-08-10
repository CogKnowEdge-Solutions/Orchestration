# Lab 3 Assignment: Structured Output

Test what you learned in **Lab 3: Structured Output**. Try the exercises without re-running the notebook — use a scratch Python file for any code questions. Answers are at the bottom; check them after you've attempted everything.

---

## Exercises

**1. (Concept)** In your own words, why is "ask the model for JSON, then parse it" a fragile approach? Name two things that can go wrong with the model's free-form reply. *(See Section 7.)*

**2. (Concept)** What is a **schema** in the context of this lab, and what two pieces of information does each field in the schema give the model? *(See Sections 1 and 7.)*

**3. (Concept)** True or false, with a one-sentence explanation: *`model.with_structured_output(Movie)` changes which model is being used.*

**4. (Code)** Write a Pydantic schema named `Song` with fields `title` (str), `artist` (str), and `duration_seconds` (int), each with a `Field(description=...)` — exactly as you would define it in the lab.

**5. (Concept)** What is the type of the object returned by `structured_model.invoke(...)` after wrapping with `with_structured_output(Movie)` — and how does it differ from the reply in Step 4? *(See Section 10, Steps 4 and 6.)*

**6. (Applied)** Given a `review` object of type `ProductReview` with `rating` set to 5, which is the integer you can compute with directly. Rewrite this free-form model reply — `"Five stars, great product."` — as the `model_dump()` of a `ProductReview` that captures the same meaning. *(See Section 10, Steps 8–9.)*

**7. (Applied)** In Step 9 the lab computes an average rating. Why is that arithmetic only possible because of structured output — what would you have to do if Step 9's replies were plain strings?

**8. (Concept)** The lab says structured output and agent tool-calling are "the same discipline." Explain in one or two sentences what they share. *(See Section 7.)*

---

## Answer Key

**1.** Because the model decides its own format. It may wrap the JSON in markdown code fences (```json ... ```), add commentary around it, or leave out a field — so your parser has to hunt for the JSON, strip the fences, and hope every field is present. Any change in the model's wording can break the parse.

**2.** A schema is a typed contract describing the exact shape the model's answer must take. Each field gives the model two pieces of information: its **type** (`str`, `int`, `list[str]`, ...) and a **description** of what belongs in that slot (the `Field(description=...)`).

**3.** False. It wraps the *same* model so its output must match the schema; the model is unchanged. `with_structured_output(Movie)` makes every reply get parsed and validated into a `Movie` object instead of text.

**4.**

```python
class Song(BaseModel):
    title: str = Field(description="The song's title")
    artist: str = Field(description="The artist or band name")
    duration_seconds: int = Field(description="The song length in whole seconds")
```

**5.** A `Movie` object (an instance of the schema class). The Step 4 reply was a single `str` containing prose plus fenced JSON; the structured reply is a typed object whose fields you can read by name (`movie.title`, `movie.year`) — already validated.

**6.**

```python
review.model_dump()
# {'product': 'AeroPress Coffee Maker', 'rating': 5, 'sentiment': 'positive'}
```

The rating is the integer `5` — converted from the words "Five stars" — which is what makes later arithmetic like `sum(r.rating for r in reviews)` possible.

**7.** Because each reply is a `ProductReview` object with a real integer `rating`, the sum and division are ordinary Python on numbers. With plain strings you'd have to parse every reply — find the number, convert it, handle missing values — for each review, and any odd phrasing would break the calculation.

**8.** Both constrain the model to produce a structured, schema-shaped reply and then parse and validate it. A tool call ("call `multiply` with 8 and 7") is a name plus typed arguments; structured output is fields of a defined type. In both cases the framework turns the model's constrained reply into real, typed data.
