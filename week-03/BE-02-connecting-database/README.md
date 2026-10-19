# BE-02: SQLite Database Persistence

**Track:** Backend AI Engineering  
**Code:** BE-02  
**Author:** Kunal Aggarwal  
**Database:** SQLite 3 (`tasks.db`)  
**Framework:** FastAPI / Python 3.13 / Uvicorn  

---

## 1. Overview & Architectural Progression

In **BE-01**, task state lived strictly in memory; whenever the process restarted, all created tasks evaporated. 
**BE-02** swaps the ephemeral in-memory storage array for a persistent, local **SQLite database** (`tasks.db`). The public REST API endpoints and HTTP status codes remain identical to BE-01, but data now survives server crashes, restarts, and reboots.

---

## 2. Why SQLite?

- **Zero-Server Footprint:** SQLite is an embedded, serverless, single-file database engine built directly into Python.
- **ACID Compliant:** Transactions guarantee data consistency without external daemon dependencies.
- **Seamless Local Development:** Perfect bridge between in-memory arrays and production client-server databases like PostgreSQL (which is containerized in **BE-04**).
- **Location:** The database file is located at `week-03/BE-02-connecting-database/tasks.db` (gitignored).

---

## 3. Database Schema

The database table `tasks` is auto-initialized on server startup:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Idempotent Seeding Rule
On startup, `init_db()` queries `SELECT COUNT(*) FROM tasks`. It only inserts the initial 3 seed tasks if the table is completely empty. Repeated server restarts never duplicate seed rows.

---

## 4. Quickstart

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the SQLite API
```bash
python main.py
```
*API runs at `http://127.0.0.1:8000` with Swagger UI at `http://127.0.0.1:8000/docs`.*

### Run the Verification Test Suite
```bash
python test_api.py
```

### Run the SQL Exploration Script
```bash
python explore_sql.py
```

---

## 5. SQL Exploration Log (Stage 4)

Below are the verified SQL queries executed against `tasks.db` via `explore_sql.py`:

```sql
-- 1. Read all tasks
SELECT id, title, done, created_at FROM tasks;

-- 2. Filter completed tasks
SELECT id, title, done FROM tasks WHERE done = 1;

-- 3. Count total tasks
SELECT COUNT(*) FROM tasks;

-- 4. Count completed tasks
SELECT COUNT(*) FROM tasks WHERE done = 1;

-- 5. Keyword search using LIKE
SELECT id, title FROM tasks WHERE title LIKE '%FastAPI%';
```

**Output Result:**
```
--- 1. SELECT * FROM tasks ---
ID: 1 | Title: Review FL-01 workflow audit | Done: True
ID: 2 | Title: Build BE-01 CRUD API with FastAPI | Done: True
ID: 3 | Title: Configure SQLite persistence for BE-02 | Done: False

--- 2. SELECT * FROM tasks WHERE done = 1 ---
ID: 1 | Title: Review FL-01 workflow audit | Done: True
ID: 2 | Title: Build BE-01 CRUD API with FastAPI | Done: True

--- 3. SELECT COUNT(*) FROM tasks ---
Total task count: 3
```

---

## 6. Requirements Checklist

- [x] Same CRUD endpoints as BE-01, now backed by SQLite.
- [x] Data survives server restarts; database and table auto-create if missing.
- [x] 3 example tasks insert only on first run (verified idempotent seed).
- [x] CRUD operations execute real SQL queries (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
- [x] Correct error handling preserved (404 on missing ID, 400 on empty/missing title).
- [x] Public GitHub repo updated with documented SQL exploration and tests.
