# BE-09: Visual AI Decision Flow Engine

**Track:** Backend AI Engineering  
**Assignment Code:** BE-09  
**Stack:** FastAPI, Inngest Python SDK, React Flow Canvas Architecture (`reactflow` + Shadcn UI), OpenAI SDK (OpenRouter / Deterministic Fallback)

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
- FastAPI application serving both REST API endpoints and the React Flow studio.
- Inngest client (`id: decision-flow-service`) mounted at `/api/inngest` via `inngest.fast_api.serve`.
- Pydantic models for graph definition (`Node`, `Edge`, `WorkflowGraph`, `ExecutionRequest`).

### Phase 2: Interactive React Flow Canvas & Shadcn UI
- Production React SPA (`frontend/`) built with Vite, utilizing the official **`reactflow`** library and **Shadcn UI** components.
- Custom node types:
  - `start`: Flow trigger boundary.
  - `decision`: AI triage node with dual handles (`YES` in emerald green `#10B981` at bottom-left, `NO` in rose red `#F43F5E` at bottom-right) and editable evaluation prompts.
  - `outcome`: Terminal operational action.
- Custom edge types (`YesNoEdge`):
  - Renders smooth bezier paths with dynamic branch label pills (`YES` / `NO`).

### Phase 3: Core Step Orchestration & Binary AI Evaluation
- AI Decision Engine (`engine.py`):
  - Injects few-shot prompt instructions forcing strict `YES` / `NO` binary answers.
  - Supports OpenRouter free tier (`meta-llama/llama-3-8b-instruct:free`), local Ollama, or deterministic $0-budget zero-friction fallback.
- Inngest background function (`run-ai-decision-flow`):
  - Traverses the graph step-by-step using `step.run` for durability and observability in the Inngest Dev Server dashboard.

### Phase 4: Polish Features
- **Visual Execution State:** As the workflow executes, traversed nodes and edges illuminate in real-time.
- **Workflow Inspector Panel:** Allows editing selected node labels and AI triage prompts.
- **Live Inngest Execution Logs Panel:** Chronological audit displaying step index, node prompt, decision (`YES` / `NO`), rationale, model, and execution latency.
- **Pre-Loaded Sample Flows:**
  1. *Customer Support Incident Triage*
  2. *Pull Request Security & Defect Gate*

---

## 3. How to Run

### Step 1: Install Backend Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies: `fastapi`, `uvicorn`, `inngest`, `openai`, `pydantic`, `pytest`, `httpx`)*

### Step 2: Start the FastAPI Backend
```bash
uvicorn main:app --reload --port 8000
```
Backend API will be live at `http://127.0.0.1:8000` with Swagger docs at `http://127.0.0.1:8000/docs`.

### Step 3: Install & Start the React Flow Frontend
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** to access the React Flow studio with instant hot reloading and backend proxying.

> **Production Deployment:**
> You can also run `npm run build` inside `frontend/`. Once built to `frontend/dist/`, the FastAPI backend automatically serves the compiled React Flow application directly from `http://127.0.0.1:8000/`.

### Step 4: (Optional) Start Inngest Dev Server
```bash
npx inngest-cli@latest dev -u http://localhost:8000/api/inngest
```
View execution steps at `http://localhost:8288`.

### Step 5: Run Automated Verification Suite
```bash
python test_flow.py
# Output: All BE-09 AI Decision Flow Tests Passed Successfully!
```

---

## 4. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Visual Flow Studio Web App (React Flow) |
| `GET` | `/health` | Health and Inngest connectivity probe |
| `GET` | `/api/sample-flows` | Retrieve pre-configured binary decision graphs |
| `POST` | `/api/run` | Execute decision flow synchronously against AI engine |
| `GET` | `/api/runs/{run_id}` | Retrieve historical execution run status and trace |
| `POST / GET` | `/api/inngest` | Inngest event streaming & durable step function endpoint |
