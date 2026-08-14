# Lab 12: Capstone Project — Assignment & Evaluation Framework

**Format:** Applied Research  
**Academic Level:** Graduate  
**Total Duration:** 2 weeks (proposal + milestones + implementation + submission)  
**Instructor Sign-off Required:** Yes (proposal stage)

---

## Part 1: Objective Sheet & Academic Standards

### Expected Format

Your capstone is an **Applied Research** project, meaning:

- **Problem:** Real-world financial advisory challenge with measurable scope
- **Solution:** Multi-agent AI system integrating Labs 1–11
- **Validation:** Code runs, tests pass, compliance logging works, output is auditable
- **Deliverables:** Working notebook + documented implementation + compliance audit trail

**NOT** a theoretical research paper, exploratory prototype, or creative fiction. This is **production-shaped code** with compliance requirements.

### Minimum Academic Standards (Graduate Level)

| Criterion | Minimum Standard |
|-----------|-----------------|
| **Code Quality** | ≥95% test pass rate; all 11 labs visibly integrated; no copy-paste from labs |
| **Scope** | 10–12 cells, ≤200 lines; tight, focused implementation |
| **Documentation** | 12-section markdown with diagrams; compliance audit trail working |
| **Novelty** | At least one extension beyond basic routing/memory (Risk Manager, custom advisors, real API integration) |
| **Reproducibility** | Fresh environment runs notebook end-to-end; all dependencies pinned |
| **Compliance** | Every recommendation logged with timestamp, client ID, data sources; audit trail immutable |

---

## Part 2: Proposal Stage (Week 1, Days 1–3)

**Deliverable:** Signed topic proposal (1–2 pages)

### Required Content

1. **Problem Statement** (1–2 paragraphs)
   - What real-world financial advisory problem does your system solve?
   - Why can't one model handle it? (justify multi-agent approach)
   - What impact would this have? (e.g., "reduces advisor workload by 40%", "auditable recommendations for compliance")

2. **Proposed Solution** (1 paragraph)
   - Which Labs 1–11 will you integrate?
   - How will you extend the basic routing/memory system?
   - What makes your implementation unique?

3. **Timeline & Milestones** (1 table)
   - Days 1–3: Proposal (this)
   - Days 4–6: Routing + agents (Labs 1, 5, 6, 10)
   - Days 7–9: Memory + retrieval (Labs 3–4, 11)
   - Days 10–11: Tools, compliance logging, tests
   - Day 12: Documentation, optional exercise, final ledger
   - Day 13–14: Code review, fixes, final submission

4. **Resource Requirements** (1 paragraph)
   - OpenRouter API key (required; free tier sufficient)
   - Market data mock (provided in lab; no real API calls required)
   - Tax rules KB (provided; 10 documents)
   - Client profiles (provided; three synthetic clients)

5. **Signature Section**
   ```
   Student Name: _________________________
   Date: _________________________________
   Instructor: ____________________________   Date: _____________
   (Instructor approval required before proceeding to implementation)
   ```

### Proposal Submission Checklist

- [ ] Problem statement is specific and measurable
- [ ] Solution describes which labs you'll integrate
- [ ] Timeline has realistic milestones with dates
- [ ] Resource requirements are listed
- [ ] Proposal is 1–2 pages (concise, focused)
- [ ] Signed by student and approved by instructor

**Deadline:** Day 3 (48 hours from start)

---

## Part 3: Resource Validation (Week 1, Day 4)

**Checklist:** Before you write code, verify access to:

| Resource | Status | Notes |
|----------|--------|-------|
| **Environment** | ✓ | Python 3.11+, venv, pinned packages |
| **OpenRouter API** | ✓ | Key in .env, free tier (50 calls/day) |
| **Knowledge Base** | ✓ | 10 tax/investment rule documents (provided) |
| **Client Data** | ✓ | Three synthetic profiles (provided) |
| **Market Data Mock** | ✓ | Stock prices, fund returns (provided) |
| **Labs 1–11 Reference** | ✓ | All labs cloned/accessible |
| **Tests** | ✓ | test_lab12.py ready (20+ tests) |
| **Compliance Logger** | ✓ | log_recommendation tool template (provided) |

**Validation Task:** Run one cell from each dependency:

```bash
# Test OpenRouter connection
python3 -c "from langchain_openai import ChatOpenAI; m = ChatOpenAI(model_name='nvidia/nemotron-3-super-120b-a12b:free'); print('✓ API ready')"

# Test graph imports
python3 -c "from langgraph.graph import StateGraph, START, END; print('✓ LangGraph ready')"

# Test test suite
python3 -m pytest test_lab12.py::TestNotebookArtifact -v
```

**Sign-off:** If all resources are accessible, you're cleared to proceed to implementation.

---

## Part 4: Milestone Check-ins (Days 4–12)

**Format:** Brief progress reports (1 paragraph each, 5 min to write)

| Milestone | Due | Report Topics |
|-----------|-----|---------------|
| **Routing & Agents** | Day 6 | Supervisor routing works? Three advisors respond? Routes logged? |
| **Memory & Retrieval** | Day 9 | Client profile loads? KB retrieval ranks documents? Top-2 injected into prompt? |
| **Tools & Compliance** | Day 11 | Market API mock works? Compliance log records advisor calls? Token counting accurate? |
| **Tests & Docs** | Day 12 | ≥20 tests passing? 12-section markdown complete? Diagrams clear? |

**Submission:** One email per milestone to instructor with:
- What you completed this period
- What blockers you hit (if any)
- What's next

This keeps you on track and catches problems early.

---

## Part 5: Grading Rubric (100 Points)

### Category 1: Implementation (60 points)

| Feature | Points | Criteria |
|---------|--------|----------|
| **Routing System** | 10 | Supervisor routes to 3+ advisors; routes logged; uses Command |
| **Long-Term Memory** | 10 | load_memory works; client profile loads; write tool persists facts |
| **Knowledge Base** | 8 | 10+ docs; retrieval ranks by overlap; top-2 injected in prompt |
| **Advisor Tools** | 8 | ≥6 tools; market API mock; portfolio snapshot; tax bracket check |
| **Handoff Escalation** | 8 | transfer_to_* tools; budget guard; one handoff per query verified |
| **Token Budgeting** | 8 | UsageCapture callback; per-advisor budgets; ledger accurate |
| **Compliance Logging** | 8 | Every recommendation logged; timestamp + client ID + sources + tokens |

### Category 2: Documentation (15 points)

| Deliverable | Points | Criteria |
|-------------|--------|----------|
| **12-Section Markdown** | 8 | All sections present; covers Labs 1–11 integration; clear examples |
| **Mermaid Diagrams** | 4 | ≥2 diagrams; one shows routing, one shows data flow |
| **Compliance Checklist** | 3 | Audit trail explained; disclosure of mock vs real APIs |

### Category 3: Tests & Code Quality (15 points)

| Criterion | Points | Criteria |
|-----------|--------|----------|
| **Test Suite** | 8 | ≥20 tests; >95% pass rate; covers all mandatory features |
| **Code Structure** | 4 | 10–12 cells; ≤200 lines; pinned versions; no copy-paste |
| **Integration** | 3 | All 11 labs visibly used; no redundant abstractions |

### Category 4: Novelty & Extensions (10 points)

| Extension | Points | Criteria |
|-----------|--------|----------|
| **Risk Manager Advisor** | 5 | Fourth advisor added; integrates with existing routing; works correctly |
| **Real API Integration** | 5 | Integrates actual market data (Alpha Vantage, IEX) or tax API (TaxJar) |
| **Custom Advisor Specialization** | 3 | Advisor tuned for specific use case (e.g., ESG investing, tax-loss harvesting) |

**Note:** Choose ONE extension (5 pts) OR combine two minor ones (5 pts total). Not required for passing, but required for ≥90%.

---

## Part 6: Evaluation Criteria by Submission Stage

### Code Submission (Day 13)

Instructor will run:

```bash
cd Lab12(Capstone)
python3 -m pytest test_lab12.py -v          # Tests (15 points)
# Then manually review:
#  - Notebook execution top-to-bottom (8 points)
#  - Compliance log output (8 points)
#  - Markdown completeness (8 points)
#  - Extension novelty (10 points)
```

### Code Review Feedback (Day 13–14)

Instructor provides:
- Test results + scores
- Code quality observations (clarity, integration, conciseness)
- Documentation feedback (clarity, diagrams, compliance)
- Extension scoring

### Final Submission (Day 14)

Student addresses feedback (if any) and submits final version. Grade is finalized.

---

## Part 7: Success Criteria Checklist

Before submitting, verify:

### Code & Execution
- [ ] Notebook runs end-to-end without errors (fresh environment)
- [ ] All 10–12 cells execute in sequence
- [ ] Three advisors (Tax, Investment, Retirement) route correctly
- [ ] One cross-advisor handoff works (e.g., Retirement → Tax)
- [ ] Client memory loads and persists facts
- [ ] Knowledge base retrieval returns top-2 documents
- [ ] Compliance log records every recommendation

### Tests
- [ ] ≥20 tests pass (run `pytest test_lab12.py -v`)
- [ ] >95% pass rate
- [ ] All mandatory features have test coverage

### Documentation
- [ ] 12-section markdown complete (Sections 1–12)
- [ ] ≥2 mermaid diagrams (routing, data flow, or compliance pipeline)
- [ ] Cost disclosure included (~25 OpenRouter calls)
- [ ] Compliance checklist in Appendix B

### Integration
- [ ] Labs 1–11 visibly integrated (list which labs in which cells)
- [ ] No copy-paste from labs (code is adapted, not duplicated)
- [ ] ≤200 code lines (tight, focused)

### Compliance
- [ ] Compliance log output shows ≥3 recommendations with full metadata
- [ ] Each log entry has: timestamp, client ID, recommendation, sources, tokens
- [ ] Audit trail is immutable (append-only; no deletions)

### Extension (if included)
- [ ] Risk Manager advisor integrated + tested OR
- [ ] Real API (market data or tax) working OR
- [ ] Custom advisor specialization documented

---

## Part 8: Submission Format

**Due Date:** Day 14 of project (2 weeks from proposal acceptance)

**Submit via GitHub (or email zip) with:**

```
Lab12(Capstone)/
├── lab-capstone-project.ipynb      (your notebook, ≥3 cells executed showing outputs)
├── lab-capstone-project.md         (provided; update if you extended the scope)
├── test_lab12.py                   (provided; run this)
├── COMPLIANCE_LOG.txt              (sample output from your notebook, ≥3 recommendations)
├── PROJECT_SUMMARY.md              (NEW: 1 page summary of what you built + key learnings)
├── PROPOSAL_SIGNED.txt             (your signed proposal from Week 1)
└── README.md                       (quickstart for future readers)
```

**PROJECT_SUMMARY.md template:**

```markdown
# Project Summary: [Your Title]

## Problem Solved
[One sentence describing the financial problem your system addresses]

## Labs Integrated
- Lab 1: [how you used it]
- Lab 5: [how you used it]
- ... (all 11 labs)

## Key Extension
[Risk Manager / Real API / Custom Advisor / other]

## Compliance Highlights
- Total recommendations logged: [number]
- Test coverage: [%]
- Token cost per recommendation: [average]

## Key Learnings
[3–5 bullets]
```

---

## Part 9: FAQ & Resources

**Q: Can I extend the scope (more advisors, real data APIs)?**
A: Yes! That's encouraged. Just ensure mandatory features work first.

**Q: What if my proposal gets rejected?**
A: Instructor provides feedback. Revise and resubmit (24-hour turnaround).

**Q: Can I work with a partner?**
A: Yes, with instructor approval. Both must understand and be able to explain all code. Grade is shared.

**Q: Real market data APIs cost money. Can I use mocks?**
A: Yes. Mocks are fine for the lab. If you use a real API, use free-tier (Alpha Vantage, IEX Cloud free, TaxJar test mode).

**Q: What if I finish early?**
A: Great! Tackle the extension (Risk Manager / real API). You can also help classmates debug or write additional documentation.

**Q: Compliance logging sounds hard. How do I start?**
A: Template provided in Step 9. Just call `log_recommendation(client_id, advice, sources, tokens)` after each advisor decides. It appends to a ledger.

---

## Part 10: Resource Links

| Resource | Link | Purpose |
|----------|------|---------|
| **OpenRouter** | https://openrouter.ai | Free model API (50 calls/day) |
| **LangChain Docs** | https://python.langchain.com | Prompts, chains, agents |
| **LangGraph Docs** | https://langchain-ai.github.io/langgraph | Graphs, routing, Command |
| **IRS Rules (KB)** | Provided in lab-capstone-project.md | Tax knowledge base |
| **Labs 1–11** | This repo | Reference implementations |
| **Alpha Vantage** | https://www.alphavantage.co | Real stock data (free tier) |

---

## Rubric Summary (Quick Reference)

| Category | Points |
|----------|--------|
| Implementation (routing, memory, tools, compliance) | 60 |
| Documentation (12 sections, diagrams, checklist) | 15 |
| Tests (≥20 passing) | 15 |
| **Extension (Risk Manager, Real API, Custom Advisor)** | **10** |
| **TOTAL** | **100** |

**Passing:** ≥70 (mandatory features only)  
**Excellent:** ≥90 (includes extension)

Good luck! 🚀
