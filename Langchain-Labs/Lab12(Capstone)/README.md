# Lab 12: Capstone Project

**Intelligent Customer Support Platform — Full Integration of Labs 1–11**

---

## File Structure

```
Lab12(Capstone)/
├── lab-capstone-project.md              # 12-section guide (instructions & theory)
├── lab-capstone-project-assignment.md   # Deliverables, rubric, grading
├── lab-capstone-project.ipynb           # YOUR NOTEBOOK (10-12 cells, ≤200 lines)
├── test_lab12.py                        # Test suite (20+ tests)
├── lab12_cases.py                       # Test case data (auto-generated)
├── lab12-test-case-results.xlsx         # Test results (auto-generated)
├── .env.example                         # Environment template
├── .env                                 # Your API key (not committed)
└── README.md                            # This file
```

---

## What You Build

A **customer support AI system** that combines every concept from Labs 1–11:

| Concept | Lab | Integration |
|---------|-----|-----------|
| Agents & Models | Lab 1 | Model factory for all LLM calls |
| Prompts & Chains | Lab 2 | System prompts for router & specialists |
| Vectors & Retrieval | Labs 3–4 | Knowledge base lookup (overlap scoring) |
| Agent Loop | Lab 5 | Specialists loop over tool calls |
| Tools & Callbacks | Lab 6 | Department tools + UsageCapture |
| Multi-Step Agents | Lab 7 | Reasoning chains inside specialists |
| Token Budget | Lab 8 | Per-specialist budgets + ledger |
| Runtime | Lab 9 | Runtime[Guest] context injection |
| Routing & Handoff | Lab 10 | Supervisor routing + escalation |
| Long-Term Memory | Lab 11 | Customer dossier + fact storage |

---

## How to Start

### 1. Setup Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install langchain==1.3.15 langchain-core==1.5.4 langchain-openai==1.4.3 \
    langgraph==1.2.11 python-dotenv==1.2.2
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and paste your OpenRouter API key
```

### 3. Create Your Notebook

Create `lab-capstone-project.ipynb` with 10–12 code cells following the structure in `lab-capstone-project.md`, Section 10.

### 4. Run Tests

```bash
python3 -m pytest test_lab12.py -v
```

---

## Mandatory Features (All Required)

1. **Multi-agent routing** — supervisor + 4 departments (Billing, Tech, Account, Security)
2. **Long-term memory** — load dossier, write facts, two customer profiles
3. **Knowledge base** — 10+ docs, retrieval by overlap, top-2 injection
4. **Tools** — 6+ tools across departments
5. **Handoff escalation** — transfer_to_* tools with budget guard
6. **Token ledger** — UsageCapture + cumulative cost tracking
7. **Notebook structure** — pinned pip, ≤200 lines, 10–12 cells
8. **Documentation** — 12 sections, 2+ diagrams, cost disclosure

---

## Optional Features (Extra Credit)

- **Sentiment analysis** — assess_sentiment() tool, pre-route if angry
- **Priority escalation** — mark handoffs as PRIORITY based on sentiment
- **Extended memory** — multiple namespaces (facts, drinks, preferences)
- **Custom tools** — domain-specific business logic beyond basics

---

## Test Suite

Run `test_lab12.py` to validate:

- Notebook artifact (structure, line count, pinned versions)
- Model factory and API configuration
- Knowledge base and retrieval
- Multi-agent routing logic
- Memory store operations
- Tool definitions
- Token counting
- Documentation completeness

**Goal:** ≥20 tests passing, >95% pass rate.

---

## Deliverables Checklist

- [ ] `lab-capstone-project.ipynb` (10–12 cells, ≤200 lines)
- [ ] Notebook runs end-to-end without errors
- [ ] Two support tickets route and resolve correctly
- [ ] Memory dossier loads and writes work
- [ ] Retrieval returns top-2 documents
- [ ] Handoff happens exactly once per ticket
- [ ] Token ledger is complete and honest
- [ ] ≥20 tests pass
- [ ] `lab-capstone-project.md` covers all 12 sections
- [ ] 2+ mermaid diagrams in markdown
- [ ] Cost disclosure included

---

## Success Criteria

- ✅ Notebook runs without errors
- ✅ All 4 departments have working specialists
- ✅ Memory load and write confirmed
- ✅ Retrieval top-2 ranked by overlap
- ✅ Handoff guard verified (exactly 1 transfer per ticket)
- ✅ Token counts logged per decision point
- ✅ ≥20 tests pass (>95%)
- ✅ All 11 labs' concepts visibly integrated
- ✅ Clear, complete documentation

---

## Resources

- **lab-capstone-project.md** — Full instructions & theory (read first)
- **lab-capstone-project-assignment.md** — Deliverables & rubric
- **Labs 1–11** — Reference implementations for each concept
- **AGENTS.md, GUIDELINES.md, TEST.md** — Project-wide resources

---

## Tips

1. **Reuse, don't copy** — Adapt patterns from Labs 1–11; don't paste code verbatim.
2. **Test early** — Write `test_lab12.py` as you build, catch integration bugs early.
3. **Start with routing** — Get Lab 10's supervisor pattern working first.
4. **Keep the ledger honest** — Track tokens at every decision point.
5. **Optional is hard** — Finish mandatory features first, then tackle sentiment analysis.

---

## Timeline

**Estimated 90 minutes** for mandatory features:

- Days 1–2: Routing & agents (Labs 1, 5, 6, 10)
- Days 3–4: Memory & retrieval (Labs 3–4, 11)
- Days 5–6: Tools, budgets, tests (Labs 5, 8)
- Day 7: Documentation & optional exercise

---

## Questions?

Refer to:
- Lab-specific markdown files (Lab1–11) for detailed explanations
- TEST.md for testing patterns
- AGENTS.md for implementation guidelines

Good luck! 🚀
