# BE-01: In-Memory CRUD Task API

**Track:** Backend AI Engineering  
**Code:** BE-01  
**Author:** Kunal Aggarwal  
**Framework:** Python 3.13 / FastAPI / Uvicorn / Pydantic  

---

## 1. Overview

This service implements a production-grade, in-memory RESTful Task Management API. It fulfills the core CRUD lifecycle (Create, Read, Update, Delete) with explicit input validation, deterministic HTTP status codes (200, 201, 204, 400, 404), automatic OpenAPI / Swagger UI interactive documentation at `/docs`, search/filtering query parameters, and aggregate statistics.

---

## 2. Quickstart (One Command)

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Dependencies: `pip install fastapi uvicorn pydantic httpx`

### Run the Server
From the `week-02/BE-01-crud-api/` directory:
```bash
python main.py
```
*The server will start at `http://127.0.0.1:8000` with interactive Swagger UI at `http://127.0.0.1:8000/docs`.*

### Run the Automated Test Suite
```bash
python test_api.py
```

---

## 3. API Reference Table

| Method | Endpoint | Description | Auth Required | Expected Status |
|--------|----------|-------------|:-------------:|:---------------:|
| `GET` | `/` | API metadata and available endpoints | No | `200 OK` |
| `GET` | `/health` | Lightweight service health probe | No | `200 OK` |
| `GET` | `/tasks` | List all tasks (supports `?done=true` & `?search=term`) | No | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve single task by integer ID | No | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create task with auto-assigned ID (`done=false`) | No | `201 Created` / `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update title and/or boolean status | No | `200 OK` / `400 Bad Request` / `404` |
| `DELETE` | `/tasks/{id}` | Remove task from collection | No | `204 No Content` / `404 Not Found` |
| `GET` | `/stats` | Aggregate summary (`total`, `done`, `open`) | No | `200 OK` |
| `POST` | `/reset` | Re-seed in-memory collection to initial 3 tasks | No | `200 OK` |

---

## 4. Verified cURL Proofs

### Check Health Probe
```bash
curl -i -X GET http://127.0.0.1:8000/health
```
**Response:**
```http
HTTP/1.1 200 OK
content-length: 15
content-type: application/json

{"status":"ok"}
```

### Create a New Task (Success Path — 201 Created)
```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Implement SQLite database for BE-02"}'
```
**Response:**
```http
HTTP/1.1 201 Created
content-length: 83
content-type: application/json

{"id":4,"title":"Implement SQLite database for BE-02","done":false}
```

### Create a Task with Missing Title (Validation Failure — 400 Bad Request)
```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{}'
```
**Response:**
```http
HTTP/1.1 400 Bad Request
content-length: 31
content-type: application/json

{"error":"Title is required"}
```

### Request Non-Existent Task (404 Not Found)
```bash
curl -i -X GET http://127.0.0.1:8000/tasks/99
```
**Response:**
```http
HTTP/1.1 404 Not Found
content-length: 30
content-type: application/json

{"error":"Task 99 not found"}
```

### Delete Task (204 No Content)
```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/4
```
**Response:**
```http
HTTP/1.1 204 No Content
```

---

## 5. Swagger UI Documentation

Interactive OpenAPI documentation is served natively at `/docs`. Every endpoint includes:
- Clear one-line summaries and operation tags (`General`, `Tasks`).
- Input parameter constraints (query strings, path parameters, JSON bodies).
- Explicit response models for both 200/201 successes and 400/404 error objects.
- Full interactive "Try it out" execution directly from the browser without needing curl.

---

## 6. The Mortality Experiment

1. **Test Procedure:** Created task `#4` ("Buy almond milk"), confirmed it appeared in `GET /tasks`.
2. **Server Restart:** Terminated the Uvicorn process (`Ctrl+C`) and restarted `python main.py`.
3. **Observation:** Calling `GET /tasks` returned only the initial 3 seed tasks; task `#4` was permanently lost.
4. **Conclusion:** In-memory state lives solely in process RAM. Any deployment, process crash, worker scale-down, or server restart destroys state. This proves why durable database persistence (SQLite in BE-02 and Postgres in BE-04) is indispensable for production systems.

---

## 7. Bonus: AI Rematch Analysis ("AI vs Me")

I tested a naive memory-spec prompt with an LLM:
> *"Write a FastAPI task manager with CRUD endpoints, in-memory list, 404 on missing tasks, and 400 on empty titles."*

The resulting code was saved to `ai-version/ai_main.py` and benchmarked against our test suite.

### Findings:
1. **What AI Did Well:** Fast scaffolding of Pydantic models and standard route decorators.
2. **Where AI Failed Silently:**
   - **Status Code Mismatch:** When given an invalid JSON body, default FastAPI Pydantic parsing returns HTTP `422 Unprocessable Entity` rather than HTTP `400 Bad Request` required by the REST specification.
   - **Whitespace Bypass:** Posting `{"title": "   "}` bypassed the AI's validation because a whitespace string has length > 0. Our implementation explicitly runs `.strip()`.
   - **ID Collision Bug:** The AI used `len(tasks) + 1` to assign IDs. If task #1 is deleted and a new task is added, duplicate IDs are created. Our code uses `max(ids) + 1`.
3. **Rematch Prompt v2:**
   > *"Write a FastAPI CRUD API with Pydantic. Ensure missing or whitespace-only titles return status 400 with a custom JSON error, ID generation uses max(id)+1, and DELETE returns 204 with an empty body."*
   With these explicit constraints, the AI output matched the required specification.

---

## 8. Requirements Checklist

- [x] Server starts with one documented command (`python main.py`).
- [x] Full CRUD on in-memory list; all 5 endpoints work.
- [x] Correct status codes everywhere (200, 201, 204, 400, 404) with JSON error messages.
- [x] POST/PUT strictly validate input (handles empty payload and whitespace strings).
- [x] Swagger UI at `/docs`; full CRUD cycle verified via "Try it out".
- [x] Public GitHub repo with ≥6 commits documenting each progressive stage.
- [x] Comprehensive README with curl outputs, Swagger guide, mortality experiment, and AI rematch.
