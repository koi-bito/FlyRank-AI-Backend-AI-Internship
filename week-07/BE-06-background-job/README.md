# BE-06: Your First Background Job (Fast Doors & Eventual Consistency)

**Track:** Backend AI Engineering  
**Code:** BE-06  
**Author:** Kunal Aggarwal  
**Framework:** FastAPI / Python 3.13 / Uvicorn  
**Orchestration Engine:** Inngest (`inngest` Python SDK)  

---

## 1. The Core Architecture

| Work Type | Example Endpoint | Operating Mode |
|---|---|---|
| **Request / Response** | `GET /health` | Synchronous (<5ms). Client blocks and waits. |
| **Background Job** | `POST /reports` ➔ Inngest `make-report` | Asynchronous. Client receives `202 Accepted` in ~2ms. Heavy 8s compilation runs in background. |
| **Cron Job** | Inngest `heartbeat` (`* * * * *`) | Clock-driven. No client request; clock wakes up worker every minute. |

---

## 2. Quickstart (Two Commands)

### Command 1: Start the Backend API
From `week-07/BE-06-background-job/`:
```bash
python main.py
```
*API boots at `http://127.0.0.1:3000` with Inngest handler served at `/api/inngest`.*

### Command 2: Start the Inngest Dev Server
In a second terminal:
```bash
npx inngest-cli@latest dev -u http://localhost:3000/api/inngest
```
*Open interactive dashboard at `http://localhost:8288` to inspect execution trees, sleep steps, and retries.*

### Run the Automated Test Suite
```bash
python test_api.py
```

---

## 3. Endpoints & Inngest Functions Reference Table

| Type | Name / Route | Trigger | Behavior | Status Codes |
|---|---|---|---|:---:|
| **API** | `POST /reports` | HTTP POST `{ "topic": "..." }` | Validates input, saves pending state, emits event, returns immediately. | `202 Accepted` / `400 Bad Request` |
| **API** | `GET /reports/{id}` | HTTP GET | Polls current processing status (`pending` ➔ `done` or `failed`). | `200 OK` / `404 Not Found` |
| **Function** | `make-report` | Event: `report/requested` | Step 1: `step.sleep(8s)` ➔ Step 2: `step.run(build-report)`. Retries: 2 (3 attempts). | N/A (Background) |
| **Function** | `say-hello` | Event: `test/hello` | Step 1: `step.sleep(5s)` ➔ returns greeting. | N/A (Background) |
| **Function** | `heartbeat` | Cron: `* * * * *` | Every 60 seconds, logs total, pending, done, and failed counts. | N/A (Cron) |

---

## 4. Verified Proof: Fast Door & Eventual Consistency

### Step 1: Client Requests Report (Instant 202 in 2.2ms)
```bash
curl -i -X POST http://127.0.0.1:3000/reports \
  -H "Content-Type: application/json" \
  -d '{"topic": "quarterly-sales-audit"}'
```
**Response:**
```http
HTTP/1.1 202 Accepted
content-type: application/json

{"id":"rep_b3577ef8","status":"pending"}
```

### Step 2: Immediate Status Poll (Pending State)
```bash
curl -i -X GET http://127.0.0.1:3000/reports/rep_b3577ef8
```
**Response:**
```http
HTTP/1.1 200 OK
{"id":"rep_b3577ef8","topic":"quarterly-sales-audit","status":"pending","result":null}
```

### Step 3: Status Poll After 8 Seconds (Done State)
```bash
curl -i -X GET http://127.0.0.1:3000/reports/rep_b3577ef8
```
**Response:**
```http
HTTP/1.1 200 OK
{
  "id":"rep_b3577ef8",
  "topic":"quarterly-sales-audit",
  "status":"done",
  "result":"Comprehensive executive report on 'quarterly-sales-audit' successfully compiled.",
  "completed_at":1792294405.12
}
```

---

## 5. Architectural Discernment: Retries vs. Bad Input (Stage 3 & 4)

### The Boundary Rule on Retries:
> **"A wrong input is rejected at the door with HTTP 400 and never enqueued; only a wrong moment (transient network glitch, temporary database lock, or rate limit) deserves an automatic retry."**
> 
> *If a user submits `{}` without a topic, retrying 3 times with exponential backoff will never make the request succeed — it merely burns compute and clogs queue capacity. Conversely, if a downstream report compiler experiences a transient network timeout, retrying with exponential backoff allows the job to succeed once the remote service recovers.*

### Decoding Cron Expressions:
- **`0 8 * * *`**: *"At minute 0 of hour 8 (08:00 AM) every single day of the month."*
- **`0 22 * * 0`**: *"At minute 0 of hour 22 (10:00 PM) every Sunday (day 0 of the week)."*

---

## 6. Requirements Checklist

- [x] API + Inngest Dev Server start with documented commands.
- [x] `POST /reports` returns HTTP 202 + ID in <50ms; slow 8s compute runs in background.
- [x] `GET /reports/{id}` reports `pending` then transitions to `done` with output.
- [x] Unknown report ID returns 404; missing topic returns 400 without event dispatch.
- [x] `make-report` uses ≥2 discrete execution steps (`step.sleep`, `step.run`).
- [x] Topic `"fail"` triggers 3 retry attempts before marking state failed.
- [x] Cron function `heartbeat` runs on schedule and logs queue metrics.
- [x] Public GitHub repository with 6 progressive stage commits.
