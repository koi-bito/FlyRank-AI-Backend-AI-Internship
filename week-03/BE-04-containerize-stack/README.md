# BE-04: Containerize Your Stack (FastAPI + PostgreSQL in Docker)

**Track:** Backend AI Engineering  
**Code:** BE-04  
**Author:** Kunal Aggarwal  
**Database:** PostgreSQL 16 (Dockerized) with SQLite Fallback  
**Orchestration:** Docker Compose (`docker compose up`)  

---

## 1. Overview & Architectural Decoupling

In **BE-02**, our API was coupled directly to SQLite queries. In **BE-04**, we introduce a clean **Repository Pattern** (`TaskRepository`). 

The domain logic and FastAPI HTTP routes depend strictly on the abstract `TaskRepository` interface:
- When running in Docker with a `DATABASE_URL`, `PostgresTaskRepository` connects to the containerized PostgreSQL engine.
- When running locally without Docker, `SQLiteTaskRepository` acts as a zero-dependency local store.
- **Critical Proof:** Service and HTTP route definitions in `main.py` did not change a single line of business logic when swapping database engines.

```
       ┌────────────────────────┐
       │   FastAPI App (HTTP)   │
       │   Routes & Validation  │
       └───────────┬────────────┘
                   │ Depends on Interface
       ┌───────────▼────────────┐
       │     TaskRepository     │ (Abstract Contract)
       └─────┬────────────┬─────┘
             │            │
  ┌──────────▼─────┐┌─────▼──────────┐
  │ Postgres Repo  ││  SQLite Repo   │
  │ (Docker Stack) ││ (Local Dev)    │
  └────────────────┘└────────────────┘
```

---

## 2. Docker Compose Architecture

The entire production stack runs with a single command:
```bash
docker compose up --build
```

### Services Defined:
1. **`db` (PostgreSQL 16 Alpine):**
   - Runs on internal Docker network and exposes `5432:5432`.
   - Persists data to named Docker volume `postgres_data`.
   - Executes `init.sql` automatically on first launch via `/docker-entrypoint-initdb.d/init.sql`.
   - Healthcheck: runs `pg_isready -U postgres -d taskdb` every 5 seconds.
2. **`app` (FastAPI + Uvicorn):**
   - Built from multi-stage Python 3.11 slim `Dockerfile`.
   - Connects to Postgres via `DATABASE_URL=postgresql://postgres:postgres@db:5432/taskdb`.
   - Declares `depends_on: db: condition: service_healthy` to guarantee the database is fully accepting connections before starting HTTP workers.

---

## 3. Environment Variables (`.env.example`)

Copy `.env.example` to `.env` to customize credentials:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=taskdb
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskdb
PORT=8000
```
*Note: `.env` is excluded by root `.gitignore` and never committed.*

---

## 4. Proving Persistence Across Restarts

1. **Launch Stack:** Run `docker compose up -d`.
2. **Insert Task:** Post a new task via curl:
   ```bash
   curl -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Verify Docker Volume Persistence"}'
   ```
3. **Restart the Entire Container Stack:**
   ```bash
   docker compose restart
   ```
4. **Query Records:**
   ```bash
   curl http://localhost:8000/tasks
   ```
5. **Result:** The created task persists intact because the PostgreSQL cluster writes to the managed Docker volume `postgres_data`, surviving container stops, restarts, and image updates.

---

## 5. Local Verification (Without Docker)

You can run the repository contract tests and the API test suite locally on your host machine:

```bash
# Test the abstract repository contract
python test_repository.py

# Test the FastAPI HTTP endpoints over the active repository
python test_api.py
```

---

## 6. Requirements Checklist

- [x] PostgreSQL runs in Docker with a named persistent volume (`postgres_data`).
- [x] Whole stack starts with a single command: `docker compose up`.
- [x] Connection strings managed via `.env` (gitignored) with committed `.env.example`.
- [x] A Postgres repository replaced SQLite/in-memory store — service and routes unchanged.
- [x] Persistence proven across container stops and restarts.
- [x] Public GitHub repository updated with clean architecture documentation and Dockerfile.
