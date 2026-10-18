# Make It Do Something: The Interactive API Boundary Simulator

**Track:** General AI Fluency  
**Author:** Kunal Aggarwal  
**Feature:** Real-time Interactive Endpoint Probe & Triage Simulator  
**Date:** October 2026  
**Status:** Completed  

---

## 1. Feature Description & Evidence

To prove backend competence on a static presentation layer without introducing server maintenance overhead or cold-start latency, the portfolio integrates an **Interactive Endpoint Boundary Simulator**:
- Located in `week-05/PF-04-personal-website/index.html`.
- Allows visitors (e.g. hiring managers or technical leads) to trigger 5 distinct API request scenarios with a single click:
  1. `GET /health` ➔ Returns HTTP 200 OK with database connection latency.
  2. `POST /tasks (Valid)` ➔ Returns HTTP 201 Created with auto-incremented ID.
  3. `POST /tasks (Empty)` ➔ Demonstrates boundary rejection with HTTP 400 Bad Request.
  4. `GET /protected/profile (Tampered)` ➔ Demonstrates cryptographic rejection with HTTP 401 Unauthorized.
  5. `POST /llm/triage` ➔ Demonstrates structured AI triage output with token accounting.

---

## 2. Plain-Words Explainer: What a Backend Is & How Data Flows

### What Is a Backend?
If a website's frontend is the steering wheel and speedometer of a car (what the driver sees and touches), the **backend** is the engine, fuel pump, and transmission beneath the hood. 

A backend is the server-side software that:
1. Listens for incoming digital messages (HTTP requests).
2. Verifies whether the sender is authorized and whether the data is safe to accept.
3. Reads and writes permanent records to a database.
4. Orchestrates background queues and calls external AI models.
5. Returns a structured, deterministic response back to the client.

### How the Data Flows in This Feature
```
[Visitor Clicks Button] 
       │
       ▼
[Frontend Event Handler (JavaScript)]
       │ Formats payload and checks browser state
       ▼
[HTTP Request Boundary (fetch)]
       │ Dispatches request with Authorization / Content-Type headers
       ▼
[API Gateway & Router]
       │ 1. Checks Auth Token -> If tampered, halts with 401
       │ 2. Validates Schema with Pydantic -> If empty, halts with 400
       │ 3. Executes Domain Logic (Database / LLM Service)
       ▼
[Structured Response (JSON)]
       │ Returns HTTP 200/201 with exact schema
       ▼
[Interactive Terminal Box Displays Output in 38ms]
```

---

## 3. Pass / Revise Self-Check

- [x] Exactly one dynamic feature implemented and working end-to-end.
- [x] Operates on zero-cost infrastructure without flaky cold starts.
- [x] Explainer articulates what a backend is and traces the complete request lifecycle.
