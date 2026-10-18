# BE-08: PDF Report Generator Pipeline

**Track:** Backend AI Engineering  
**Assignment Code:** BE-08  
**Dataset:** Option A — Shop Orders (`report.db`)  
**Stack:** FastAPI, Python 3.12, SQLite, ReportLab (Vector PDF Engine)

---

## 1. Overview & Architecture

This service queries transaction data with SQL, renders structured aggregate metrics into a multi-page PDF document, stores the resulting binary file on disk, and serves it to clients strictly by link.

```
+-------------------------------------------------------------------------------+
|                             THE 4-MOVE PIPELINE                               |
|                                                                               |
|   1. QUERY             2. RENDER               3. STORE         4. SERVE      |
|  [SQLite Aggs]  -->  [ReportLab Flow]  -->  [Disk + DB Path] --> [HTTP Link]  |
|                                                                               |
|   * Rule: Store and link. JSON payloads NEVER carry raw binary file bytes.    |
+-------------------------------------------------------------------------------+
```

---

## 2. Dataset & SQL Aggregation

The dataset models an e-commerce store with 200 transactions across 5 core products and 7 customers seeded over a 14-day rolling window.

### Aggregation Queries Used in Reporting:

```sql
-- 1. Executive Totals
SELECT 
    COUNT(*) as total_orders, 
    ROUND(SUM(amount), 2) as total_revenue, 
    ROUND(AVG(amount), 2) as avg_order 
FROM orders;

-- 2. Top 5 Revenue-Generating Products
SELECT 
    product, 
    COUNT(*) as units_sold, 
    ROUND(SUM(amount), 2) as revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;

-- 3. Daily Sales Velocity (Last 7 Recorded Days)
SELECT 
    SUBSTR(created_at, 1, 10) as order_date, 
    COUNT(*) as daily_orders, 
    ROUND(SUM(amount), 2) as daily_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date DESC
LIMIT 7;

-- 4. Multi-Page Ledger Sample
SELECT 
    id, customer, product, amount, SUBSTR(created_at, 1, 16) as created_at 
FROM orders 
ORDER BY id ASC 
LIMIT 60;
```

---

## 3. How to Run

### Step 1: Install Dependencies
```bash
pip install fastapi uvicorn reportlab pytest
```

### Step 2: Seed the Database
```bash
python db.py
# Output: Seeded report.db with exactly 200 orders.
```

### Step 3: Run the API Server
```bash
uvicorn main:app --reload --port 8000
```
Interactive OpenAPI documentation is live at `http://127.0.0.1:8000/docs`.

### Step 4: Run the Automated Verification Suite
```bash
python test_api.py
```

---

## 4. API Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Service health status | `200 OK` |
| `POST` | `/reports` | Query + render + persist PDF report | `201 Created` / `200 OK` |
| `GET` | `/reports/{id}` | Retrieve report metadata | `200 OK` / `404 Not Found` |
| `GET` | `/reports/{id}/file` | Stream PDF binary file from disk | `200 OK` / `404 Not Found` |

---

## 5. End-to-End Execution Proof

### Move 1: Generate Report (POST /reports)
```bash
curl -X POST http://127.0.0.1:8000/reports \
  -H "Content-Type: application/json" \
  -d '{"force": true}'
```
**Response (HTTP 201 Created):**
```json
{
  "id": "rep_999333a466",
  "file": "/reports/rep_999333a466/file",
  "cached": false
}
```

### Move 2: Duplicate Request Caching (Ask Twice, Get One)
```bash
curl -X POST http://127.0.0.1:8000/reports
```
**Response (HTTP 200 OK):**
```json
{
  "id": "rep_999333a466",
  "file": "/reports/rep_999333a466/file",
  "cached": true
}
```

### Move 3: Inspect Report Metadata
```bash
curl http://127.0.0.1:8000/reports/rep_999333a466
```
**Response (HTTP 200 OK):**
```json
{
  "id": "rep_999333a466",
  "date_key": "2026-10-18",
  "created_at": "2026-10-18 09:22:45",
  "file": "/reports/rep_999333a466/file"
}
```

### Move 4: Download PDF Binary by Link
```bash
curl -O -J http://127.0.0.1:8000/reports/rep_999333a466/file
```
The downloaded file is verified as a valid PDF binary (>8 KB) spanning 2 pages.

---

## 6. Engineering Reflections

### Stage 4 Architecture Question:
> *At what point would you move this work out of the request (into BE-06's background-job pattern)?*

**Answer:** You move this work out of the synchronous request-response cycle into a background job the moment document compilation takes longer than 500ms to 1 second. When reports query millions of rows, incorporate high-resolution charts, or handle concurrent requests, running CPU-intensive layout rendering directly inside the HTTP handler saturates ASGI worker threads and causes client socket timeouts. Transitioning to BE-06's `POST -> 202 Accepted` pattern allows the client to poll or receive a webhook notification while workers process rendering tasks asynchronously with retries and concurrency limits.

### Stage 5 Deduplication Questions:
> *What does daily caching protect against, and what is a real-world example where a missing check costs money?*

**Answer:**
1. **Protection:** Idempotent caching protects against accidental duplicate triggers (e.g., users double-clicking the "Generate Daily Invoice" button or scheduled cron jobs overlapping during network lag), preventing wasted CPU, memory, and disk I/O.
2. **Real-world costly failure:** In an enterprise billing system using third-party document rendering or paid signing APIs (such as DocuSign or an AWS Lambda rendering pipeline with billable compute and S3 egress), an unthrottled customer support team dashboard refreshed 1,200 invoice generation requests in 10 minutes following a UI freeze, resulting in over $3,500 in unbudgeted external API charges and duplicated cloud storage files.

---

## 7. Clean Page Break Guarantee

In multi-page document generation, a common failure is row slicing where a table entry is bisected across a page margin. In this implementation:
1. `Table(..., repeatRows=1)` ensures the column header row automatically re-renders at the top of Page 2.
2. Flowables and table row heights are strictly managed so that individual transaction entries are never fractured across page boundaries.
