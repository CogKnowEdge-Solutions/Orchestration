# Lab 12 Capstone Project Assignment

**Due:** Self-paced (completion recommended after Labs 1–11)  
**Deliverables:** Jupyter notebook, 12-section markdown, test suite, and closed ledger  
**Time estimate:** 90 minutes  

---

## Assignment Overview

Build an **Intelligent Customer Support Platform** that integrates every concept from Labs 1–11:

- **Lab 1 (Agents & Models)** — model factory & API key management
- **Lab 2 (Prompts & Chains)** — system prompts for router & specialists
- **Lab 3–4 (Retrieval & RAG)** — knowledge base lookup via overlap scoring
- **Lab 5 (Agent Loop)** — specialist agents that call tools in a loop
- **Lab 6 (Tools & Callbacks)** — department tools and UsageCapture instrumentation
- **Lab 7 (Multi-Step)** — reasoning chains within specialists
- **Lab 8 (Token Budget)** — per-specialist budgets and cumulative ledger
- **Lab 9 (Runtime)** — Runtime[Guest] context injection
- **Lab 10 (Routing & Handoff)** — supervisor routing with Command and peer escalation
- **Lab 11 (Memory)** — long-term customer facts across sessions

---

## Project Requirements

### Mandatory

1. **Multi-agent routing** (Lab 10)
   - A supervisor that reads a ticket and routes to the right department via Command
   - Four departments: Billing, Tech, Account, Security
   - Each department is a separate specialist agent with its own tools and prompt

2. **Long-term customer memory** (Lab 11)
   - Load customer dossier from store at the start (load_memory)
   - Write facts to store after resolving a ticket (remember tool)
   - Two customer profiles with different histories

3. **Knowledge base retrieval** (Labs 3–4)
   - 10+ synthetic documents covering common issues
   - Retrieval tool that ranks by overlap (no embeddings)
   - Inject top-2 docs into specialist prompt

4. **Tool use across departments** (Lab 5)
   - Billing: get_invoice, process_refund
   - Tech: check_service_status, search_kb
   - Account: get_plan, set_seats
   - Security: review_account_access, check_mfa_status

5. **Handoff escalation** (Lab 10)
   - transfer_to_* tools that return Command(goto=..., graph=Command.PARENT)
   - One handoff per ticket via budget guard
   - Support at least one cross-department ticket flow

6. **Token budgeting & ledger** (Labs 6, 8)
   - UsageCapture to record tokens at each decision point
   - Per-specialist budgets
   - Closed ledger showing total tokens per ticket and average cost

7. **Notebook structure** (all labs)
   - Pinned pip install in first cell (langchain==1.3.15, langgraph==1.2.11, etc.)
   - ≤200 code lines total (tight, focused implementation)
   - 10–12 code cells, each cell a logical step

8. **Documentation** (all labs)
   - 12-section markdown guide (matching labs 1–11 format)
   - 2+ mermaid diagrams (system architecture, sequence flow)
   - Cost disclosure (~25 OpenRouter calls)

### Optional

9. **Sentiment analysis escalation** (extending Lab 10)
   - Fifth department: Escalation
   - assess_sentiment() tool that scores 0–1
   - If sentiment < 0.3, pre-route to Escalation before specialist
   - Handoff to specialist marked **PRIORITY**

---

## Deliverables

### Notebook

`lab-capstone-project.ipynb` — 10–12 code cells:

```
1. Install & imports
2. Knowledge base (10 synthetic docs)
3. Retrieval tool (overlap scorer)
4. Customer data & memory store
5. Support tools (6 tools, 4 depts)
6. Router & specialist agents
7. Handoff tools & budget guard
8. Token counter (UsageCapture)
9. Graph & runtime (StateGraph + Runtime[Guest])
10. Billing ticket run (dossier load, retrieve, route, resolve)
11. Memory write (remember customer fact)
12. Cross-dept ticket run (account → security escalation)
+ Bonus: Ledger & diagram
```

### Markdown

`lab-capstone-project.md` — 12 sections:

1. Lab Title
2. Problem Statement
3. Input Data
4. Processing
5. Output
6. Tech Stack
7. Underlying Concepts
8. Prerequisites
9. Environment Setup
10. Step-wise Instructions
11. Optional Exercise
12. What We Learnt

### Tests

`test_lab12.py` — 20+ tests covering:

- Notebook artifact (pinned versions, line count, structure)
- Model factory and API key
- Knowledge base retrieval accuracy
- Tool definitions and routing
- Memory store operations
- Multi-agent graph wiring
- Handoff mechanics
- Token ledger correctness
- Documentation completeness

### Test Results

`lab12-test-case-results.xlsx` — standard format:
- Test Cases sheet (20+ rows)
- Five Gates sheet
- Summary sheet

---

## Grading Rubric

| Criterion | Points | Notes |
|-----------|--------|-------|
| **Mandatory features** | 60 | Routing, memory, retrieval, tools, handoff, budgets, notebook structure |
| **Documentation** | 15 | 12 sections, diagrams, cost disclosure, clarity |
| **Tests** | 15 | All mandatory features tested, ≥20 tests, >95% pass rate |
| **Integration** | 10 | All 11 labs visibly integrated, no copy-paste from labs |

Total: **100 points**

---

## Hints & Tips

1. **Reuse, don't copy** — adapt patterns from Labs 1–11, don't paste code. The capstone is about composition, not duplication.

2. **Start with routing** — get Lab 10's supervisor pattern working first, then layer in memory, retrieval, and tools.

3. **Test early** — write test_lab12.py as you build; it helps catch integration bugs.

4. **Keep the ledger honest** — track tokens at every decision point and sum them at the end. If a ticket costs 2,000 tokens, know why.

5. **The optional exercise is hard** — sentiment analysis requires plumbing the assessment result into the routing logic. Do mandatory features first.

6. **No real databases** — everything is in-memory (InMemoryStore). If you want to persist, that's a future project.

---

## Success Criteria

- ✅ Notebook runs end-to-end without errors
- ✅ Two support tickets (billing + cross-dept) are routed and resolved
- ✅ Memory dossier loads and writes work
- ✅ Retrieval returns top-2 documents ranked by overlap
- ✅ Handoff happens exactly once (budget guard verified)
- ✅ Token count per ticket is logged and summed
- ✅ ≥20 tests pass (>95% pass rate)
- ✅ 12-section markdown with diagrams
- ✅ All 11 labs' concepts are visibly integrated

---

## Timeline

1. **Days 1–2**: Build core agents (Labs 1, 5, 6) and routing (Lab 10)
2. **Days 3–4**: Add memory (Lab 11) and retrieval (Labs 3–4)
3. **Days 5–6**: Integrate token budgets (Lab 8) and write tests
4. **Day 7**: Documentation, optional exercise, final ledger
5. **Optional**: Code review, sentiment analysis, deploy

---

## Resources

- **AGENTS.md** — Agent implementation guidelines
- **GUIDELINES.md** — Lab design principles
- **TEST.md** — Testing framework
- **Labs 1–11** — Reference implementations for each concept
