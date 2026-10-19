# BE-07: Put an LLM Behind Your API (Defensive Triage Boundary)

**Track:** Backend AI Engineering  
**Code:** BE-07  
**Author:** Kunal Aggarwal  
**Prompt Version:** `v1` (`prompts/triage-v1.md`)  
**Stack:** FastAPI / Python 3.13 / Pydantic v2 / OpenAI SDK (OpenRouter & Ollama Compatible)  

---

## 1. What This Endpoint Does

This service adds a defensive, non-conversational AI endpoint (`POST /llm/triage`) that takes unformatted customer support messages, parses intent, and returns clean, schema-validated JSON with closed categories, urgency ratings, and escalation triggers. It treats LLMs as untrusted, flaky remote microservices: every request is bounded by a **30-second client timeout**, **selective backoff retries** (ignoring 4xx errors), **automatic single-retry schema repair**, a **quarantine log** for persistent 422 failures, and a **kill-switch** for instant deterministic fallback during provider outages.

---

## 2. Quickstart

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start API Server
```bash
python main.py
```
*Server boots at `http://127.0.0.1:8000` with Swagger UI at `http://127.0.0.1:8000/docs`.*

### Step 3: Run the Benchmark Evals Suite
```bash
python evals/run_evals.py
```

---

## 3. Verified cURL Proof

```bash
curl -i -X POST http://127.0.0.1:8000/llm/triage \
  -H "Content-Type: application/json" \
  -d '{"message": "URGENT: Our production database connection pool is throwing 500 errors on the checkout endpoint!"}'
```

**Exact JSON Response:**
```http
HTTP/1.1 200 OK
content-type: application/json

{
  "category": "technical_support",
  "urgency": "high",
  "assigned_team": "support_tier_2",
  "confidence": 0.98,
  "summary": "Production database connection pool failures on checkout endpoint.",
  "requires_escalation": false
}
```

---

## 3. Boundary Defense & Failure Scenarios

### Validation at the Door (400 Bad Request)
Sending empty payloads or whitespace never touches the model:
```bash
curl -i -X POST http://127.0.0.1:8000/llm/triage \
  -H "Content-Type: application/json" \
  -d '{"message": "   "}'
```
**Response:**
```http
HTTP/1.1 400 Bad Request
{"error": "Field 'message' cannot be empty or whitespace"}
```

### The Kill Switch (`LLM_ENABLED=false`)
When upstream providers experience outages, setting `LLM_ENABLED=false` bypasses all model calls, instantly returning a safe deterministic fallback in <5ms without dropping incoming traffic.

---

## 4. Provider & Model Configuration (Three Env Vars to Swap)

The service is provider-agnostic. Swap providers in `.env` without modifying a single line of Python code:

| Provider | Base URL | Model Name | Setup Notes |
|----------|----------|------------|-------------|
| **OpenRouter (Free)** | `https://openrouter.ai/api/v1` | `openrouter/free` | Turn ON privacy settings in OpenRouter dashboard. |
| **Ollama (Local / Offline)** | `http://localhost:11434/v1/` | `llama3.2:3b` | 100% free, unlimited, no API key required. |
| **Stub Mode (Deterministic)** | Any | Any | Set `LLM_STUB=1` for instant, zero-cost test suites. |

---

## 5. Benchmark Evaluation Suite (8 Cases)

- **Test Suite:** `evals/cases.json` (8 ground-truth test cases covering technical errors, billing queries, sales leads, security leaks, ambiguous spam, and prompt-injection attempts).
- **Execution Script:** `python evals/run_evals.py`
- **Result:** **8/8 (100.0%) passing rate**
- **Benchmark Date:** October 2026 | Prompt Version: `v1`

---

## 6. Observability, Cost Accounting & 10,000/Day Scaling

Every live model call logs structured metrics to `logs/costs.jsonl`:
```json
{"timestamp": 1792294100.12, "prompt_version": "v1", "model": "openrouter/free", "input_tokens": 184, "output_tokens": 42, "duration_ms": 480.25, "repaired": false}
```

### 10,000 Requests/Day Cost Estimation:
- Average tokens per call: 184 input + 42 output = 226 total tokens.
- Daily volume: `10,000 requests * 226 tokens = 2,260,000 tokens/day`.
- **On OpenRouter / Ollama:** **$0.00 / month.**
- **On Claude 3.5 Haiku ($0.80/M input, $4.00/M output):**
  - Input: `1.84M * $0.80 = $1.47/day`
  - Output: `0.42M * $4.00 = $1.68/day`
  - Total: **~$3.15/day (~$94.50/month)**.

---

## 7. What I'd Fix With Another Day

> *"With another day, I would add a local Redis cache keyed by the SHA-256 hash of `(message.strip().lower() + prompt_version)` with a 24-hour TTL. Repeating customer queries like 'where is my receipt?' would answer in 2ms from cache with zero token spend."*

---

## 8. Requirements Checklist

- [x] `JOB-CARD.md` exists with strict closed output schema.
- [x] Job passes all 3 rules: closed output, one decision, human-gradeable.
- [x] POST endpoint validates input with clean 400 before model is called.
- [x] Output schema defined in code with Pydantic Enums.
- [x] `LLM_STUB=1` returns schema-valid response with zero model calls.
- [x] Prompt is a versioned file (`prompts/triage-v1.md`), not an inline string.
- [x] User content sent as user message, defending against prompt injection.
- [x] Output parsed and validated before returning to caller.
- [x] Single repair retry on failure, then clean 422 + quarantine log.
- [x] Explicit 30s timeout configured (SDK default 10min rejected).
- [x] Selective retries on transient errors, never retrying 400/401/403.
- [x] Structured cost and latency logging per call.
- [x] `LLM_ENABLED=false` kill switch returns instant deterministic fallback.
- [x] `evals/cases.json` has 8 ground-truth cases; score reported honestly.
- [x] Public GitHub repository with clean `.env.example` and no committed secrets.
