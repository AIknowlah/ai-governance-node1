\---



\## 📦 Project Status: Proof of Concept (Intentional)



\*\*Current State\*\*: Node 1 complete and production-ready  

\*\*Full System\*\*: Nodes 2-5 planned but not yet implemented



\### Why Stop at Node 1?



This project intentionally focuses on \*\*Node 1 as a proof-of-concept\*\* for three strategic reasons:



\#### 1. Validate the Pattern First

Before building a full 5-node system, I needed to prove:

\- ✅ The "governance-first" approach works in practice

\- ✅ NRIC redaction can achieve 78.6% adversarial resistance

\- ✅ BigQuery audit trails meet PDPA Section 9 (Accountability)

\- ✅ The pattern is documentable and testable



\*\*Result\*\*: Pattern validated. Ready to replicate across Nodes 2-5.



\#### 2. Create a Replicable Template

By fully documenting Node 1:

\- ✅ Code → `src/nodes/node\_1\_input\_sanitizer.py`

\- ✅ Tests → `tests/test\_node1.py`, `tests/redteam\_node1.py`

\- ✅ Governance docs → `docs/node1\_governance\_mapping.md`

\- ✅ Vulnerability register → `docs/node1\_vulnerability\_register.md`



Other engineers can use this as a \*\*template\*\* for building their own governance controls, without needing to see Nodes 2-5.



\#### 3. Demonstrate Methodology Over Completeness

For portfolio purposes, \*\*demonstrating the approach matters more than building all 5 nodes\*\*.



Node 1 shows:

\- ✅ Problem identification (PDPA compliance risk)

\- ✅ Solution design (gatekeeper pattern)

\- ✅ Implementation (Python + LangGraph + BigQuery)

\- ✅ Testing (unit tests + red-team)

\- ✅ Documentation (audit-ready)

\- ✅ Honest vulnerability disclosure



Building Nodes 2-5 would show the same skills — just applied to different problems (routing, API calls, labeling, rate limiting).



\*\*The methodology is proven. Scaling it is execution.\*\*



\---



\### What's Next?



When this pattern needs to scale:

1\. \*\*Fix VUL-001 and VUL-002\*\* (spaced/hyphenated NRICs)

2\. \*\*Build Node 2\*\* (Query Router) using the same template

3\. \*\*Integrate Nodes 1-2\*\* (test the connected flow)

4\. \*\*Repeat\*\* for Nodes 3-5



\*\*Timeline\*\*: Each node = \~1 day of work (pattern established)



\---

