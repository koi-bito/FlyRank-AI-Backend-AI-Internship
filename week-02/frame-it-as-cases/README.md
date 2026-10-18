# Frame It as Cases: Work That Speaks for Itself

**Track:** General AI Fluency  
**Author:** Kunal Aggarwal  
**Date:** October 2026  
**Status:** Completed  

---

## 1. The Voice Card

> **"Direct, plain, technically rigorous, zero buzzwords."**

*Standing Rule for Portfolio Copy:* If a sentence sounds like a recruiter marketing template ("results-driven passionate engineer leveraging synergistic paradigms"), delete it immediately. State what failed, what was built, what was decided, and what happened.

---

## 2. Before / After Copy Audit: Cutting the AI Slop

| Generic AI Draft (Discarded) | Edited Plain-Words Reality (Kept) | Why It Matters |
|-----------------------------|-----------------------------------|----------------|
| *"I leveraged state-of-the-art FastAPI paradigms and enterprise architectural patterns to build a robust, scalable task ecosystem that empowers seamless productivity."* | *"I built a REST API where every input is checked before touching memory. Missing titles return clean 400s with error messages, deleting a missing task returns 404, and every endpoint is testable via Swagger UI."* | Replaces meaningless adjectives with concrete HTTP contracts an engineering manager can verify. |
| *"Harnessing the transformative power of background queues, I architected a distributed event-driven framework to optimize user latency."* | *"I moved an 8-second report generator out of the HTTP thread and into Inngest. The API answers with HTTP 202 in 40ms, and retries failing jobs with exponential backoff."* | Cites real numbers (8s down to 40ms) and specific operational behavior (retries with backoff). |

---

## 3. The Framed Case Studies (The Three Beats)

### Case Study 1: The Resilient LLM Triage API (BE-07)
*Putting an AI Model Behind a Production Boundary*

- **Beat 1: The Problem**  
  Calling an LLM from an API route is dangerous: LLMs are slow, non-deterministic, cost money per token, and hallucinate malformed keys. If a model hangs for 60 seconds or returns invalid JSON, a standard backend server crashes or ties up HTTP worker threads until incoming requests queue up and drop.
- **Beat 2: What I Did & Decided**  
  I built an API endpoint that treats the LLM as an untrusted, failing remote service. I put Pydantic schema validation at the door (400 before touching the model), enforced a strict 30-second client timeout (rejecting the SDK's 10-minute default), implemented an automatic single-retry repair loop for schema errors, and routed persistent failures to a quarantine log with a clean 422 instead of crashing. A kill-switch env var disables the model during provider outages.
- **Beat 3: What Came of It**  
  The endpoint scored 8/8 on a rigorous evaluation test suite covering ambiguous inputs and prompt-injection edge cases. If an upstream outage occurs, the API returns a deterministic fallback in under 15ms without dropping requests.

---

### Case Study 2: Durable Background Processing with Inngest (BE-06)
*Fast Doors, Eventual Consistency, and Controlled Retries*

- **Beat 1: The Problem**  
  Heavy database aggregations and PDF rendering take 8 to 15 seconds. Making a client wait on an open HTTP connection leads to gateway timeouts (504s), connection drops on mobile, and server thread starvation.
- **Beat 2: What I Did & Decided**  
  I separated request acceptance from execution. The client receives an immediate `202 Accepted` response with a tracking ID in under 50ms. The heavy execution runs asynchronously through Inngest event steps. I configured 3 retry attempts with exponential backoff for transient failures, and designed a heartbeat cron worker to monitor queue health every minute.
- **Beat 3: What Came of It**  
  Clients never experience timeouts. An intentional failure test proved that bad inputs are rejected immediately at the door (400), while intermittent system errors retry up to 3 times with progressive backoff before cleanly logging a failure state.

---

### Case Study 3: Containerized Multi-Tenant Metering Engine (BE-04 & Capstone)
*Zero-Cost Persistence and Boundary-Strict Quotas*

- **Beat 1: The Problem**  
  Software-as-a-Service platforms lose revenue and crash when tenants exceed usage limits or send duplicate webhook requests that double-count billable actions.
- **Beat 2: What I Did & Decided**  
  I built an idempotent usage metering engine backed by PostgreSQL in Docker. I separated the database layer behind a strict repository interface, ensuring the domain logic and HTTP routes remained completely decoupled from the underlying storage engine. Every billable transaction requires an idempotency key to prevent double-billing.
- **Beat 3: What Came of It**  
  The entire multi-service stack boots with a single command (`docker compose up`). Repeated webhook replays are safely deduplicated, and tenants exceeding quotas receive deterministic 429/402 responses before any compute resources are allocated.

---

## 4. Bio & Conversion Copy

### Professional Bio (3 Bullets, No Fluff)
- **Role:** Backend AI Engineer focused on deterministic APIs, resilient queue architectures, and LLM orchestration.
- **Core Stack:** Python (FastAPI, Pydantic), Node.js (Express, TypeScript), PostgreSQL, Docker, SQLite, Inngest.
- **Current Work:** Completing the FlyRank Backend AI Engineering track; building production-ready API pipelines at Deccan AI.

### The Conversion CTA
> **"Ready to see how this code handles real traffic? Book a 20-minute technical walkthrough where I run live failure probes against my active endpoints."**  
> `[Book 20-Min Technical Walkthrough]` · `[Browse Source on GitHub]` · `[Connect on LinkedIn]`

---

## 5. Pass / Revise Self-Check

- [x] Voice card defined at top (5–7 words: "Direct, plain, technically rigorous, zero buzzwords").
- [x] All three core portfolio pieces drafted using the Three Beats (Problem → What I Did/Decided → What Came of It).
- [x] Before/After table demonstrates ruthless cutting of generic AI filler.
- [x] Bio and CTA point directly to the single target action (20-minute code walkthrough).
