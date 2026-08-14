# Langchain-Labs

A comprehensive series of 11 labs covering LangChain, LangGraph, and multi-agent systems — from agents & models (beginner) through token budgets and long-term memory (advanced).

---

## Quick Start: Running Tests

Each lab has a test suite (`test_labN.py`) that validates the notebook code and structure. Run tests from the lab directory:

### Setup (first time only)

```bash
cd Lab1\(Beginner\)  # or any other lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or use the pinned versions from the notebook's first cell
```

### Run Tests for a Single Lab

```bash
cd Lab1\(Beginner\)
python3 -m pytest test_lab1.py -v
```

### Run All Tests in a Lab (with summary)

```bash
cd Lab5\(Intermediate\)
python3 -m pytest test_lab5.py -v --tb=short
```

### Run a Specific Test

```bash
cd Lab10\(Advanced\)
python3 -m pytest test_lab10.py::TestTools::test_get_invoice -v
```

### Run Tests for All Labs (from repository root)

```bash
for i in {1..11}; do
  echo "Testing Lab $i..."
  lab_dir=$(ls -d Lab${i}\(* 2>/dev/null | head -1)
  if [ -n "$lab_dir" ]; then
    cd "$lab_dir"
    python3 -m pytest test_lab${i}.py -q
    cd ..
  fi
done
```

---

## Lab Breakdown

| Lab | Level | Topic | Test Count | Time |
|-----|-------|-------|-----------|------|
| Lab 1 | Beginner | Agents & Models | 18 | ~30 min |
| Lab 2 | Beginner | Prompts & Chains | 16 | ~30 min |
| Lab 3 | Beginner | Vectors & Retrieval | 9 | ~30 min |
| Lab 4 | Intermediate | RAG Pipeline | 10 | ~40 min |
| Lab 5 | Intermediate | Agent Loop | 17 | ~45 min |
| Lab 6 | Intermediate | Tools & Callbacks | 20 | ~45 min |
| Lab 7 | Intermediate | Multi-Step Agents | 15 | ~45 min |
| Lab 8 | Advanced | Token Budget | 18 | ~45 min |
| Lab 9 | Advanced | Runtime & Retrieval | 19 | ~45 min |
| Lab 10 | Advanced | Multi-Agent Coordination | 26 | ~45 min |
| Lab 11 | Advanced | Long-Term Memory | 21 | ~45 min |
| **Lab 12** | **Capstone** | **Integrated Project** | **25+** | **~90 min** |

---

## Test Result Files

Each lab includes an Excel workbook (`lab N-test-case-results.xlsx`) with:
- **Test Cases sheet** — all test rows mapped from the pytest definitions
- **Five Gates sheet** — gates 1-5 with pass/fail/pending status
- **Summary sheet** — total counts and generation timestamp

Example: `Lab10(Advanced)/lab10-test-case-results.xlsx`

---

## What Each Test Validates

Tests verify:
1. **Notebook structure** — pinned versions, code line count, companion files
2. **Model factory** — correct API endpoint and model selection
3. **Core functionality** — tools, routing, memory, state management
4. **Documentation** — all 12 required sections, diagrams, cost disclosure
5. **Optional exercises** — advanced features documented and available

See each lab's `test_labN.py` for the complete test suite.

---

## Environment Variables

Each lab requires `.env` with:
```
OPENROUTER_API_KEY=sk-or-v1-...
```

Copy `.env.example` to `.env` and paste your OpenRouter API key (free tier available).

---

## Documentation

- `AGENTS.md` — Agent implementation guidelines
- `CONSTITUTION.md` — Constitutional AI principles
- `GUIDELINES.md` — LangChain lab design principles
- `TEST.md` — Testing framework and requirements

Each lab folder also contains:
- `lab-*.md` — Complete lab walkthrough
- `lab-*-assignment.md` — Post-lab assignment (optional)
- `lab-*.ipynb` — Executable notebook