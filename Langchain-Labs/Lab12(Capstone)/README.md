# Lab 12: Capstone Project — Intelligent Financial Advisory Platform

**Applied Research | Graduate Level | 2-Week Timeline**

A comprehensive capstone project that integrates all 11 prior labs into a production-grade multi-agent financial advisory system with proposal-stage approval, milestone check-ins, and structured evaluation.

---

## File Structure

```
Lab12(Capstone)/
├── lab-capstone-project.md              # 12-section guide (finance domain, concept integration)
├── lab-capstone-project-assignment.md   # Complete evaluation framework
├── test_lab12.py                        # Test suite (20+ tests for validation)
├── lab-capstone-project.ipynb           # YOUR NOTEBOOK (10-12 cells, ≤200 lines)
├── PROPOSAL_SIGNED.txt                  # Your signed proposal (Week 1, Days 1-3)
├── COMPLIANCE_LOG.txt                   # Sample compliance log from your notebook (Week 2)
├── PROJECT_SUMMARY.md                   # Your final summary (Week 2, Day 14)
├── .env.example                         # Environment template
├── .env                                 # Your API key (not committed)
└── README.md                            # This file
```

---

## What You Build

**Intelligent Financial Advisory Platform** — A multi-agent AI system that:

- **Routes client questions** to specialist advisors (Tax Advisor, Investment Strategist, Retirement Planner)
- **Remembers client profiles** across sessions (income, age, goals, preferences)
- **Retrieves from knowledge bases** (IRS tax rules, investment strategies, retirement planning)
- **Calls market data APIs** (mocked; stock prices, fund returns, inflation rates)
- **Reasons through complex problems** (tax optimization, asset allocation, retirement readiness)
- **Logs every recommendation** to compliance audit trail (timestamp, client ID, sources, tokens)
- **Manages advisor capacity** via token budgets

Integrates every concept from Labs 1–11:

| Lab | Integration |
|-----|-----------|
| Lab 1–2 | Model factory, system prompts for advisors |
| Lab 3–4 | KB retrieval by overlap scoring |
| Lab 5 | Agent loop for tool usage |
| Lab 6 | Tools (market data, portfolio checks, tax rules) + UsageCapture |
| Lab 7 | Multi-step reasoning chains |
| Lab 8 | Token budgets per advisor |
| Lab 9 | Runtime[Client] context injection |
| Lab 10 | Supervisor routing + handoff escalation |
| Lab 11 | Client memory store + long-term facts |

---

## Evaluation Framework (2-Week Timeline)

### Week 1: Proposal & Planning

**Days 1–3:** Submit signed topic proposal
- Problem statement (why multi-agent advisory?)
- Proposed solution (which labs you'll integrate)
- Timeline with milestones
- Resource validation checklist
- **Requires instructor approval before proceeding**

**Day 4:** Resource validation
- Verify OpenRouter API access
- Confirm KB, client data, market mock available
- Test lab imports

### Week 2: Implementation & Evaluation

**Days 5–6:** Routing & agents (Labs 1, 5, 6, 10)  
**Milestone 1:** Supervisor routes to ≥3 advisors; routes logged

**Days 7–9:** Memory & retrieval (Labs 3–4, 11)  
**Milestone 2:** Client profile loads; KB retrieval ranks documents; top-2 injected

**Days 10–11:** Tools, budgets, compliance (Labs 5, 8)  
**Milestone 3:** Tools work; token counting accurate; compliance log records advisors

**Days 12–13:** Documentation & tests  
**Milestone 4:** ≥20 tests pass; 12-section markdown; diagrams; compliance audit trail

**Day 14:** Final submission & grading
- Code runs end-to-end
- All tests pass (>95%)
- Compliance log working
- Notebook + markdown + PROJECT_SUMMARY.md submitted

---

## Grading Rubric at a Glance

| Category | Points | Evaluated By |
|----------|--------|---|
| **Implementation** | 60 | Code runs; routing/memory/tools/handoff work; compliance logging accurate |
| **Documentation** | 15 | 12-section markdown; ≥2 diagrams; compliance checklist; cost disclosure |
| **Tests** | 15 | ≥20 tests passing; >95% pass rate; all mandatory features covered |
| **Extension** | 10 | Risk Manager advisor OR Real API integration OR Custom advisor specialization |
| **TOTAL** | **100** | Instructor review + automated tests |

**Passing:** ≥70  
**Excellent:** ≥90

---

## How to Start

### 1. Write Your Proposal (Days 1–3)

**Template:**

```markdown
# Capstone Proposal: [Your Project Title]

## Problem Statement
[Why is multi-agent financial advisory needed?]

## Proposed Solution
[Which labs will you integrate? What's your extension?]

## Timeline
- Days 5–6: Routing & agents
- Days 7–9: Memory & retrieval
- Days 10–11: Tools & compliance
- Days 12–14: Tests & documentation

## Resource Requirements
- OpenRouter API key ✓
- Knowledge base (provided) ✓
- Client data (provided) ✓
- Market API mock (provided) ✓

## Signature
Student: ________________________  Date: _________
Instructor Approval: _____________  Date: _________
```

### 2. Setup Environment (Day 4)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install langchain==1.3.15 langchain-core==1.5.4 langchain-openai==1.4.3 \
    langgraph==1.2.11 python-dotenv==1.2.2

cp .env.example .env
# Paste your OpenRouter API key
```

### 3. Build Your Notebook (Days 5–13)

Create `lab-capstone-project.ipynb` with 10–12 cells:

1. Install & imports
2. Knowledge base (10+ financial docs)
3. Retrieval tool (overlap scoring)
4. Client data & memory store
5. Market data mock & tools
6. Supervisor & three advisors
7. Handoff tools + budget guard
8. Compliance logging tool
9. Graph & runtime
10. Tax advisor run
11. Investment advisor run
12. Retirement advisor run (with potential handoff)

### 4. Test & Document (Days 12–14)

```bash
# Run test suite
python3 -m pytest test_lab12.py -v

# Verify compliance log output
# (Run your notebook and save advisor recommendations)

# Create PROJECT_SUMMARY.md describing:
#  - Problem you solved
#  - Labs integrated
#  - Key extension
#  - Compliance highlights
#  - Learnings
```

### 5. Submit (Day 14)

Email instructor with:
- `lab-capstone-project.ipynb` (executed, showing outputs)
- `lab-capstone-project.md` (updated if you extended scope)
- `COMPLIANCE_LOG.txt` (sample output showing ≥3 recommendations logged)
- `PROJECT_SUMMARY.md` (1 page: what you built + learnings)
- `PROPOSAL_SIGNED.txt` (your signed proposal from Week 1)

---

## Mandatory Features (≥70 to pass)

- ✅ Routing: Supervisor + 3+ advisors (Billing, Tech, Account OR Tax, Investment, Retirement)
- ✅ Memory: load_memory + remember tool + persistent store
- ✅ Retrieval: 10+ docs, overlap-ranked, top-2 injected
- ✅ Tools: ≥6 tools working (API calls, data lookups)
- ✅ Handoff: transfer_to_* with budget guard
- ✅ Compliance: Every recommendation logged with timestamp, client ID, sources, tokens
- ✅ Tests: ≥20 tests passing (>95%)
- ✅ Documentation: 12 sections, ≥2 diagrams

---

## Optional Extensions (add 10 points each, required for ≥90)

Choose **one:**

1. **Risk Manager Advisor** — Fourth advisor that flags concentration risk, tax-loss harvesting, correlation risks
2. **Real API Integration** — Connect to Alpha Vantage (stocks), TaxJar (tax), or IEX Cloud (fund data)
3. **Custom Advisor Specialization** — Tune one advisor for specific domain (ESG investing, retirement income optimization, etc.)

---

## Key Differences from Labs 1–11

| Aspect | Labs 1–11 | Lab 12 Capstone |
|--------|-----------|-----------------|
| **Scope** | Single concept | Integration of all 11 |
| **Approval** | None | Proposal must be signed |
| **Checkpoints** | None | 4 milestones tracked |
| **Documentation** | 12 sections (structured) | 12 sections + compliance checklist |
| **Grading** | Pass/Fail on tests | Rubric-based (0–100 points) |
| **Compliance** | Not required | Audit trail mandatory |
| **Extension** | Optional exercise | Required for ≥90 |

---

## Success Criteria

Before submitting, verify:

- [ ] Notebook runs end-to-end (fresh environment, no errors)
- [ ] ≥20 tests pass (`pytest test_lab12.py -v`)
- [ ] Compliance log shows ≥3 advisor recommendations with full metadata
- [ ] Client memory loads on first run, persists facts for next session
- [ ] One handoff scenario works (advisor A calls transfer_to_B)
- [ ] Knowledge base retrieval returns top-2 docs ranked by overlap
- [ ] 12-section markdown complete with ≥2 diagrams
- [ ] Project summary (1 page) submitted
- [ ] All 11 labs visibly integrated in code

---

## Timeline Checklist

| Week | Days | Milestone | Status |
|------|------|-----------|--------|
| **1** | 1–3 | ✓ Signed proposal submitted | ___ |
| **1** | 4 | ✓ Resources validated | ___ |
| **2** | 5–6 | ✓ Routing + agents working | ___ |
| **2** | 7–9 | ✓ Memory + retrieval working | ___ |
| **2** | 10–11 | ✓ Tools + compliance logging working | ___ |
| **2** | 12–13 | ✓ Tests passing (>95%); docs complete | ___ |
| **2** | 14 | ✓ Final submission (code + summary) | ___ |

---

## Resources

**In Lab12(Capstone) folder:**
- `lab-capstone-project.md` — Full guide (read first)
- `lab-capstone-project-assignment.md` — Complete evaluation framework
- `test_lab12.py` — Test suite (20+ tests)

**Project-wide:**
- `AGENTS.md` — Agent implementation guidelines
- `GUIDELINES.md` — Lab design principles
- `TEST.md` — Testing framework
- Labs 1–11 — Reference implementations

**External (optional, for real API extension):**
- Alpha Vantage: https://www.alphavantage.co (free stock data)
- IEX Cloud: https://iexcloud.io (free fund data)
- TaxJar: https://www.taxjar.com (test mode)

---

## Tips for Success

1. **Start with proposal** — Get it approved before coding. Saves 3+ hours of misdirection.
2. **Test early, test often** — Run `pytest test_lab12.py -v` after each cell.
3. **Log compliance first** — Compliance is not an afterthought. Build it into every advisor response.
4. **Reuse, don't copy** — Adapt patterns from Labs 1–11; don't paste code.
5. **Timeline matters** — Follow the 2-week schedule. Milestones catch problems early.
6. **Extension is the grade booster** — Mandatory features get ≥70; extension gets you to ≥90.

---

## Questions?

Refer to:
- `lab-capstone-project-assignment.md` (Part 9: FAQ)
- Milestone check-in with instructor (each week)
- Labs 1–11 for reference implementations

Good luck! 🚀

---

*Last updated: 2026-08-14*
