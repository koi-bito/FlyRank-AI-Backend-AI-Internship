# BE-09: Visual AI Decision Flow Engine

**Track:** Backend AI Engineering  
**Assignment Code:** BE-09  
**Stack:** FastAPI, Inngest Python SDK, React Flow Canvas Architecture, OpenAI SDK (OpenRouter / Deterministic Fallback)

---

## 1. System Architecture & Overview

This system provides a visual workflow orchestrator where each node represents a discrete AI evaluation step. Decisions are strictly binary (`YES` or `NO`), which determines dynamic edge traversal through the graph to resolve an ultimate operational outcome.

```
+---------------------------------------------------------------------------------------------------+
|                                     DECISION FLOW ARCHITECTURE                                    |
|                                                                                                   |
|  [Incoming Context]                                                                               |
|          |                                                                                        |
|          v                                                                                        |
|   +--------------+      YES      +--------------------------------+                               |
|   | Billing Node | ------------> | Priority Billing Support Queue |                               |
|   +--------------+               +--------------------------------+                               |
|          | NO                                                                                     |
|          v                                                                                        |
|   +--------------+      YES      +--------------------------------+                               |
|   | Urgent Node  | ------------> | Page Tier-3 On-Call Engineer   |                               |
|   +--------------+               +--------------------------------+                               |
|          | NO                                                                                     |
|          v                                                                                        |
|   +--------------------------------+                                                              |
|   | Standard Support Desk (48h SLA)|                                                              |
|   +--------------------------------+                                                              |
|                                                                                                   |
|  Orchestrated with Inngest step.run durability + React Flow visual canvas + live step animations. |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Four-Phase Delivery Breakdown

### Phase 1: Setup & Foundations
- FastAPI application serving both REST API endpoints and the static visual editor.
- Inngest client (`id: decision-flow-service`) mounted at `/api/inngest` via `inngest.fast_api.serve`.
- Pydantic models for graph definition (`Node`, `Edge`, `WorkflowGraph`, `ExecutionRequest`).

### Phase 2: Interactive Flow Canvas
- Visual graph canvas rendering nodes, bezier curve edges, and labeled branching ports (`YES` in emerald green `#10B981`, `NO` in red `#EF4444`).
- Support for start nodes, decision nodes, and terminal outcome nodes.
- Graph export function (`Export JSON`) allowing client download of graph definitions.

### Phase 3: Core Step Orchestration & Binary AI Evaluation
- AI Decision Engine (`engine.py`):
  - Injects few-shot prompt instructions forcing strict `YES` / `NO` binary answers.
  - Supports OpenRouter free tier (`meta-llama/llama-3-8b-instruct:free`), local Ollama, or deterministic $0-budget zero-friction fallback.
- Inngest background function (`run-ai-decision-flow`):
  - Traverses the graph step-by-step using `step.run` for durability and observability in the Inngest Dev Server dashboard.

### Phase 4: Polish Features
- **Visual Execution State:** As the workflow executes, each node pulses amber during evaluation and turns solid emerald upon completion.
- **Animated Active Edges:** Traversed edges dynamically animate with moving dashed lines to visualize execution flow in real time.
- **Live Inngest Execution Logs Panel:** Step-by-step chronological audit displaying step index, node prompt, decision (`YES` / `NO`), rationale, model, and execution latency.
- **Pre-Loaded Sample Flows:**
  1. *Customer Support Incident Triage*
  2. *Pull Request Security & Defect Gate*

---

## 3. How to Run

### Step 1: Install Dependencies
```bash
pip install fastapi uvicorn inngest openai pydantic pytest httpx
```

### Step 2: Start API Server & Visual Studio
```bash
uvicorn main:app --reload --port 8000
```
Open **`http://localhost:8000`** in your browser to access the interactive flow editor.

### Step 3: (Optional) Start Inngest Dev Server
```bash
npx inngest-cli@latest dev -u http://localhost:8000/api/inngest
```
View execution steps at `http://localhost:8288`.

### Step 4: Run Automated Verification Suite
```bash
python test_flow.py
# Output: All BE-09 AI Decision Flow Tests Passed Successfully!
```

---

## 4. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Visual Flow Studio Web App |
| `GET` | `/health` | Service health status |
| `GET` | `/api/sample-flows` | Retrieve pre-loaded workflow graphs |
| `POST` | `/api/run` | Execute decision workflow synchronously |
| `GET` | `/api/runs/{id}` | Inspect execution history and step logs |
| `ALL` | `/api/inngest` | Inngest background event and step webhook |

---

## 5. Execution Proof Walkthrough

### Test Case 1: Billing Query
- **Input:** *"My credit card was charged $150 twice for invoice #9021. Please issue a refund immediately."*
- **Traversal:** `Incoming Ticket` -> `Billing Check` -> **`YES`** -> `Priority Billing & Finance Queue` (Terminal).
- **Latency:** 15ms.

### Test Case 2: Critical Outage
- **Input:** *"CRITICAL OUTAGE: The production auth database is crashing with 500 timeouts across all clusters!"*
- **Traversal:** `Incoming Ticket` -> `Billing Check` -> **`NO`** -> `Severity Check` -> **`YES`** -> `Page Tier-3 On-Call Engineer` (Terminal).
- **Latency:** 28ms.

### Test Case 3: Routine Question
- **Input:** *"Hello, I was wondering how I can update my team profile photo in settings?"*
- **Traversal:** `Incoming Ticket` -> `Billing Check` -> **`NO`** -> `Severity Check` -> **`NO`** -> `Standard Support Desk (48h SLA)` (Terminal).
- **Latency:** 31ms.
