# FL-01: AI Workflow Audit & Tool Setup

**Intern:** Kunal Aggarwal  
**Track:** General AI Fluency & Backend AI Engineering  
**Submission Date:** October 2026  
**Status:** Completed  

---

## 1. Executive Summary

This workflow audit establishes a systematic baseline for integrating AI into my daily engineering routine across coursework, the FlyRank AI Backend Internship, freelance/Deccan AI engineering projects, and independent software development. Following Ethan Mollick's task-classification framework ("On-boarding your AI Intern"), recurring weekly tasks are classified into four distinct operational buckets:

1. **Just Me** (Preserve human judgment, core learning, critical ethics, or proprietary boundary)
2. **Delegate to AI with Review** (AI drafts first pass; human verifies against strict criteria)
3. **Collaborate with AI** (Iterative pair-programming and thinking-partner brainstorming)
4. **Fully Automate** (Deterministic or pipeline-driven repeatable execution)

---

## 2. Weekly Task Audit (14 Recurring Tasks)

| # | Recurring Task | Operational Bucket | One-Line Rationale |
|---|----------------|-------------------|-------------------|
| 1 | **Designing core API schemas & domain contracts** | **Collaborate with AI** | Exploring edge cases and OpenAPI typing together leads to faster, more robust interface definitions. |
| 2 | **Writing boilerplate CRUD endpoints & data models** | **Delegate to AI with review** | Express/FastAPI boilerplate is predictable, but requires strict boundary checks for error codes and validations. |
| 3 | **Database migration reviews & indexing strategies** | **Just Me** | Unvetted AI schema alters can cause silent performance regressions or accidental table locks in production. |
| 4 | **Refactoring synchronous loops to background queues (Inngest/BullMQ)** | **Collaborate with AI** | Requires co-designing state machines, backoff retry policies, and idempotency guarantees. |
| 5 | **Writing unit & integration test suites** | **Delegate to AI with review** | AI generates comprehensive happy and edge-case test fixtures from route specs, requiring human verification of mocks. |
| 6 | **Debugging strange runtime stack traces & memory leaks** | **Collaborate with AI** | Sharing structured logs with LLMs accelerates hypothesis generation while I verify behavior in the debugger. |
| 7 | **Reviewing peer pull requests & team code quality** | **Just Me** | High-level architectural empathy, mentorship, and security accountability cannot be offloaded to an algorithm. |
| 8 | **Summarizing upstream API documentation & changelogs** | **Delegate to AI with review** | Extracts breaking changes and auth updates quickly; requires checking against real endpoints. |
| 9 | **Formatting commit messages & semantic changelog drafting** | **Fully Automate** | Git diffs can be piped through conventional commit scripts to produce standardized release notes deterministically. |
| 10 | **Technical documentation & README generation** | **Delegate to AI with review** | AI turns working code and comments into clean documentation tables, verified by running each curl command. |
| 11 | **Job search outreach & personalized cold emails** | **Delegate to AI with review** | AI drafts targeted pitch emails based on company pain points, polished by human tone and portfolio references. |
| 12 | **GitHub repository architecture analysis & code exploration** | **Collaborate with AI** | Ingesting repo structure and asking targeted questions clarifies component relationships rapidly. |
| 13 | **Formatting & verifying database seed data** | **Fully Automate** | Synthetic data generation scripts produce realistic test records reliably without manual data entry. |
| 14 | **Final security & credentials audit before pushing** | **Just Me** | Human accountability must verify that `.env`, tokens, and secrets are excluded from repository history. |

---

## 3. Toolkit Setup & Proof of Enrollment

The following zero-cost, enterprise-grade AI toolkit has been configured for the duration of this program:

- **Anthropic Claude (Free Tier):** Primary thinking partner, complex reasoning, and code refactoring.
- **Anthropic Academy:** Enrolled in **AI Fluency: Framework & Foundations** (Account ID: Kunal Aggarwal). Completed Module 1: *Mental Models for Modern AI Systems*.
- **OpenAI ChatGPT (Free Tier):** Cross-model benchmark for prompt engineering, syntax comparison, and reasoning validation.
- **Google Gemini & AI Studio (Free Tier):** Fast multimodal analysis, long-context reference searching, and zero-cost prototyping.
- **Perplexity AI (Free Tier):** Real-time web ground-truthing, dependency compatibility research, and technical API reference verification.

---

## 4. Claude Project Configuration

A dedicated **Claude Project** was initialized to serve as a continuous engineering co-pilot and mentor throughout the 8-week program.

### Custom Instructions Configured:

```markdown
Role & Persona:
You are a Staff Backend AI Systems Architect mentoring Kunal Aggarwal, a backend engineer specializing in Node.js, Python, resilient API architectures, and LLM orchestration. 

About Kunal:
- Building production-ready backend systems: Node.js/Express, Python/FastAPI, PostgreSQL/SQLite, Docker, and Inngest.
- Completing the FlyRank Backend AI Engineering & AI Fluency tracks.
- Focused on deterministic boundaries, zero-cost architectures, and graceful degradation.

Tone & Interaction Rules:
- Direct, warm, concise, and technically rigorous. Zero corporate fluff or generic AI hype.
- Never write entire monolithic code dumps when a surgical diff or architectural explanation is better.
- Push back on lazy design decisions (e.g. unbounded queues, unhandled timeouts, missing schema validations).
- Treat LLMs as untrusted remote HTTP services that can fail, timeout, or hallucinate.
- Maintain consistency with the defined Identity Kit and Proof Statement.
```

---

## 5. Three Target Tasks for FL-02 through FL-04

To ground the subsequent prompt engineering and automation assignments in authentic engineering work, three recurring tasks from the audit have been selected:

### Target Task 1: GitHub Repository Understanding Assistant
- **Reused in:** FL-02 (Prompt Engineering) & Capstone ideation.
- **Input:** Any public GitHub repository URL or file tree + architecture query.
- **Measurable "Done Well" Definition:** 
  1. Produces a 3-paragraph architecture breakdown (Data Layer, Business Logic, HTTP/API Layer).
  2. Generates an accurate Mermaid component diagram without syntax errors.
  3. Correctly identifies where state and configuration are managed.
  4. Answers 3 specific technical questions about edge cases without hallucinating non-existent files.

### Target Task 2: Targeted Cold Outreach & Internship Application Engine
- **Reused in:** FL-02 (Prompt Ladder) & FL-03.
- **Input:** Target company engineering blog / job post + Kunal's specific portfolio projects.
- **Measurable "Done Well" Definition:**
  1. Under 150 words total; readable in 45 seconds on mobile.
  2. References one specific engineering challenge the company solved or faces.
  3. Bridges directly to one relevant proof artifact (e.g. BE-06 background job or capstone meter).
  4. Contains exactly one frictionless call to action (e.g. "Open to a 15-minute code walk-through next Tuesday?").
  5. Completely free of AI cliches ("I was thrilled to see", "synergistic", "passionate engineer").

### Target Task 3: Production Technical README & API Specification
- **Reused in:** FL-02, BE-01 through BE-08 documentation standards.
- **Input:** Raw source code files, route definitions, and test runs.
- **Measurable "Done Well" Definition:**
  1. Includes a single copy-paste setup command that works on a fresh machine.
  2. Complete endpoint reference table with HTTP methods, route paths, auth requirements, and status codes.
  3. Includes exact verified `curl` request and response JSON snippets.
  4. Features an honest "Known Limitations & Failure Modes" section describing how the system degrades when dependencies fail.

---

## 6. Self-Evaluation Checklist

- [x] 10+ real personal tasks classified with one-line rationale (14 total).
- [x] At least 2 tasks honestly marked "Just Me" with defensible reasons (Tasks 3, 7, and 14).
- [x] 3 target tasks explicitly defined with measurable pass/fail success criteria.
- [x] Free AI toolkit verified and Anthropic Academy enrollment documented.
- [x] Claude Project custom instructions created and verified.
