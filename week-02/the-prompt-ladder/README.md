# The Prompt Ladder: Disciplined Iteration on Real Backend Tasks

**Track:** General AI Fluency  
**Author:** Kunal Aggarwal  
**Task Domain:** Backend Engineering (Reliable Background Queue & Report Generation)  
**Date:** October 2026  
**Status:** Completed  

---

## 1. Overview

Most developers change five variables at once when prompting, obscuring what actually caused an improvement or a regression. The Prompt Ladder enforces scientific discipline: **add exactly one layer per iteration, run it, observe the output, and log what worked, what broke, and what to try next.**

---

## 2. The 6-Rung Ladder

### Rung 0: The Weak Baseline
> *"Write a background job for generating reports."*

#### Output 0:
> "Here is a Python script using Celery to generate reports. First, install Celery and Redis. Then create a Celery app, define a `@app.task` called `generate_report`, and use `time.sleep(5)` to simulate generating a PDF. Then call `generate_report.delay()`."

#### Notes on Output 0:
- **Prompt:** Bare 8-word instruction.
- **Output:** Generic, assumes Celery + Redis, no HTTP endpoints, no error handling, no persistence.
- **Still Failed:** Doesn't fit into our FastAPI/Inngest stack; no status tracking for the client.
- **Next Step:** Layer 1 — Define a specific, measurable goal.

---

### Rung 1: Layer 1 — Clearer Goal
> *"Write a background job that accepts a report request via an HTTP API, returns an immediate 202 Accepted response with a job ID, processes the report asynchronously over 8 seconds, and provides a status endpoint for polling progress."*

#### Output 1:
FastAPI code with a `POST /reports` route calling `BackgroundTasks.add_task(slow_report)`. Stores status in a global Python dictionary `{"status": "pending"}` and updates it to `{"status": "completed"}` after `time.sleep(8)`.

#### Notes on Output 1:
- **Prompt Change:** Added specific lifecycle requirements (202 immediate response, job ID, polling endpoint, 8s duration).
- **Output Improvement:** Architecture shifted from generic worker script to an asynchronous REST polling pattern.
- **Still Failed:** Uses FastAPI's naive in-process `BackgroundTasks`, which drops jobs if the server restarts or crashes mid-execution. Lacks retries and backoff.
- **Next Step:** Layer 2 — Define role and production standards.

---

### Rung 2: Layer 2 — Defined Role & Engineering Standards
> *[Goal from Rung 1] +*
> *"You are a Senior Infrastructure Architect who strictly adheres to distributed systems resilience principles. Do not use in-process background threads. Require an event-driven architecture that supports automatic retries with exponential backoff."*

#### Output 2:
The model introduced Inngest event dispatching: `inngest_client.send({"name": "report/requested", "data": {"job_id": ...}})`. Defined an Inngest function with `retries=3` and a 2-step pipeline (`step.sleep` and `step.run`).

#### Notes on Output 2:
- **Prompt Change:** Explicit role ("Senior Infrastructure Architect") and constraint against fragile in-process threads.
- **Output Improvement:** Code introduced proper durable execution steps and retry policies.
- **Still Failed:** Missed input validation at the door; if the client posts `{}` without a report topic, it still enqueues an Inngest event, wasting worker cycles.
- **Next Step:** Layer 3 — Provide real context and technology stack.

---

### Rung 3: Layer 3 — Real Context & Stack Constraints
> *[Goal and Role from Rung 2] +*
> *"Context: This is for a Node.js Express service running alongside the Inngest Dev Server on localhost. It must use the official `inngest` npm package, serve the Inngest handler at `/api/inngest`, and strictly separate client input validation from worker execution."*

#### Output 3:
Swapped to Express.js. Built Express routes for `POST /reports` and `GET /reports/:id`. Added an Inngest serve handler using `serve({ client: inngest, functions: [makeReport] })`.

#### Notes on Output 3:
- **Prompt Change:** Pinned the exact language (Node.js/Express) and library setup (`serve` handler at `/api/inngest`).
- **Output Improvement:** Code is now 100% plug-and-play for our specific project repository.
- **Still Failed:** The model generated unstructured console logs and mixed route handlers with database logic in a single file.
- **Next Step:** Layer 4 — Output format & schema constraints.

---

### Rung 4: Layer 4 — Output Format & Schema Constraints
> *[Goal, Role, Context from Rung 3] +*
> *"Output Format Requirements: Provide the solution in exactly two modular files:*
> *File 1: `src/inngest/client.js` exporting the configured Inngest client and functions.*
> *File 2: `src/routes/reports.js` containing the Express router with strict Zod validation schema for the request body.*
> *Every response must adhere to clean JSON `{ id, status, result, error }`."*

#### Output 4:
Generated two separated files with clean exports. `reports.js` had a Zod schema `z.object({ topic: z.string().min(1) })`.

#### Notes on Output 4:
- **Prompt Change:** Mandated file separation and Zod schema validation.
- **Output Improvement:** Modular code with boundary validation before event firing.
- **HONEST "THIS DIDN'T HELP / REGRESSION" MOMENT:**  
  *Adding Zod validation caused the model to over-complicate the Inngest step definition! It attempted to re-validate the Inngest event payload inside the worker step using the same Zod schema, throwing an unhandled exception because Inngest wraps event data under an `event.data` sub-object. This caused the worker to crash immediately on execution.*
- **Next Step:** Layer 5 — Verification requirements, error handling, and edge case rules.

---

### Rung 5: Layer 5 — Verification & Edge Case Defense
> *[Complete prompt from Rung 4] +*
> *"Edge Cases & Failure Rules:*
> *1. If the topic is 'fail', the worker must simulate an unrecoverable failure in the final step to trigger Inngest retries.*
> *2. Event payload in Inngest must be destructured safely as `event.data.topic`.*
> *3. Include a health-check cron function running on `* * * * *` that logs pending vs completed reports.*
> *4. Self-Verification: Before outputting, trace the payload from `req.body` -> `inngest.send` -> `event.data` to guarantee variable consistency."*

#### Output 5:
Flawless production code. Destructuring bug resolved. Added the intentional "fail" topic trigger to test retry backoff, and included the cron heartbeat job matching BE-06 requirements.

---

## 3. The Final Reusable Prompt Template

A stranger can use this clean template for any background worker implementation:

```markdown
Role: Senior Backend Infrastructure Architect specializing in durable execution.

Goal: Build an asynchronous background processing pipeline with an immediate HTTP 202 acceptance endpoint, durable queue execution, and polling status endpoints.

Stack & Context:
- Framework: [Node.js Express / Python FastAPI]
- Worker Engine: [Inngest / BullMQ]
- Runtime: Local development dev server

Execution Rules:
1. Fast Door: Reject invalid inputs at the API gateway with 400 Bad Request before enqueueing any work.
2. Durable Steps: Break slow operations (>5s) into discrete execution steps (`step.sleep`, `step.run`).
3. Retry Policy: Configure exactly 3 attempts with exponential backoff for transient failures.
4. Cron Health: Include a recurring scheduled function to monitor and report queue metrics.

Deliverable Structure:
- Provide separated files: (1) Worker function definitions, (2) API route handlers.
- Verify that event data keys match between API dispatch and worker destructuring.
```

---

## 4. Evaluation Checklist

- [x] 6 total runs documented (Baseline Rung 0 + 5 progressive rungs).
- [x] Exactly one layer added per iteration without bundling.
- [x] Notes detail output changes rather than just restating prompt modifications.
- [x] Honest failure/regression moment documented (Rung 4 Zod event wrapper collision).
- [x] Final reusable template works for any developer.
