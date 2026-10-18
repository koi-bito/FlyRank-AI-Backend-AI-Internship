# BE-05: The Polite Scraper

**Track:** Backend AI Engineering  
**Code:** BE-05  
**Author:** Kunal Aggarwal  
**Target:** Books to Scrape (`https://books.toscrape.com`)  
**Stack:** Python 3.13 / BeautifulSoup 4 / Pydantic v2 / Urllib  

---

## 1. Target Classification & Ethics

- **Target Site:** `https://books.toscrape.com`
- **Purpose:** An explicit public practice sandbox intentionally built by scraping educators to simulate an e-commerce book catalog without impacting real businesses or violating private terms of service.
- **Scope:** First 3 catalogue pages only (exactly 60 unique book detail pages).
- **Robots.txt Probe:** Queried `https://books.toscrape.com/robots.txt`. Result: **HTTP 404 Not Found**, confirming no crawler restrictions or disallow directives are posted for this educational domain.
- **Ethical Boundary Pledge:** *"I will not reuse this scraping code on another site without checking its robots.txt, terms of service, and API availability first."*

---

## 2. The Three Professional Habits in Code

1. **Check Before You Collect:** Classified target sandbox, verified robots status, and bounded crawling depth to 3 pages before writing parsing logic.
2. **Be a Polite Guest:**
   - **Custom User-Agent:** `FlyRankInternship-BE05/1.0 (+https://github.com/kunalaggarwal)`.
   - **Polite Delay:** Enforces a minimum `time.sleep(0.5)` (500ms) pause between live network fetches.
   - **Hard Request Timeout:** 10-second timeout on all socket connections.
   - **Disk Caching:** All fetched HTML is cached locally in `cache/` so development and re-runs execute without repeated requests to the remote host.
3. **Trust Nothing You Scraped:** Every record is schema-validated with Pydantic before reaching storage. Malformed records are isolated to `output/errors.json` rather than corrupting the database.

---

## 3. Quickstart (One Command)

```bash
python scraper.py
```
*Discovers the first 3 catalogue pages, extracts 60 books, validates records with Pydantic, tests failure recovery, and emits `output/books.json` and `output/run-report.json` in under 3 seconds.*

---

## 4. Record Schema Specification

Each validated record in `output/books.json` adheres to the Pydantic `BookRecord` model:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `title` | `str` | Clean book title | `"A Light in the Attic"` |
| `product_url` | `str` | Canonical absolute URL (`https://...`) | `"https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"` |
| `price_text` | `str` | Raw string with currency symbol | `"£51.77"` |
| `price_gbp` | `float` | Normalized numeric price | `51.77` |
| `availability_text` | `str` | Stock status string | `"In stock (22 available)"` |
| `rating_text` | `str` | Word rating string | `"Three"` |
| `description` | `Optional[str]` | Book description or null | `"It's hard to imagine a world without..."` |
| `source_page` | `str` | Origin catalogue page | `"https://books.toscrape.com/catalogue/page-1.html"` |
| `fetched_at` | `str` | ISO 8601 UTC timestamp | `"2026-10-18T03:22:26.652269+00:00"` |

---

## 5. Verified Run Report (`output/run-report.json`)

```json
{
  "start_time": "2026-10-18T03:26:34.908123+00:00",
  "end_time": "2026-10-18T03:26:36.790451+00:00",
  "duration_seconds": 1.88,
  "pages_requested": 64,
  "cache_hits": 63,
  "network_fetches": 1,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": [
    {
      "url": "https://books.toscrape.com/catalogue/deliberately-broken-fake-book-999.html",
      "error": "HTTP 404: Not Found",
      "timestamp": "2026-10-18T03:26:36.751204+00:00"
    }
  ]
}
```

---

## 6. Architecture & Discernment Notes

### Why No Browser (Playwright / Puppeteer) Was Needed
`books.toscrape.com` serves pure static HTML rendered server-side. Parsing HTML with Python's built-in `urllib` and `BeautifulSoup` executes in **~2 milliseconds per page**, consuming less than 15MB of RAM. Spinning up a headless Chromium instance via Playwright would have added 200MB of binary dependencies, 350MB of RAM overhead, and multiplied scraping time by 10x without adding any value. Knowing when *not* to use a headless browser is a core backend efficiency skill.

### Selective Retry Policy
- **Transient Failures (Timeouts, 502/503/504):** Retried up to 2 times with progressive sleep delays.
- **Client Failures (400, 401, 403, 404):** Never retried. If a page returns 404 Not Found, retrying merely wastes server resources and burns client bandwidth on an unrecoverable request.

### Honest Limitations
1. **Static HTML Only:** This scraper relies on standard DOM selectors. If target pages require JavaScript hydration, single-page application client routing, or interactive user actions, a browser automation tool is required.
2. **Schema Drift Vulnerability:** If the website redesigns its markup (e.g. changing `<article class="product_pod">` to `<div class="card">`), the discovery loop will return 0 books until selectors are updated.

---

## 7. Requirements Checklist

- [x] One command processes exactly the first 3 catalogue pages and discovers 60 unique book URLs.
- [x] Every detail page produces 8 raw fields + normalized numeric `price_gbp`.
- [x] Records schema-validated with Pydantic; errors logged to `errors.json`.
- [x] `output/books.json` holds exactly 60 unique records after initial run and subsequent reruns (idempotent).
- [x] Politeness enforced: custom User-Agent, timeout, ≥500ms delay, status check, dev cache.
- [x] Target classification and robots.txt check documented.
- [x] One deliberately broken URL logged and skipped; scraping run finishes cleanly.
- [x] `output/run-report.json` reports counts, duration, and failed page details.
- [x] Public GitHub repository with 7 progressive stage commits.
