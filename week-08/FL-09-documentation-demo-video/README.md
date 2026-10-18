# FL-09: Personal Agent Documentation & Video Narrative

**Track:** General AI Fluency  
**Assignment Code:** FL-09 (a.k.a. "Show It / Tell the Story" Part 1)  
**Agent Name:** `RepoArchitect` CLI  
**Demo Video Link:** `https://youtu.be/unlisted-flyrank-repoarchitect-demo` (3m 45s, Live CLI Terminal Walkthrough)

---

## 1. Project Overview & Target Audience

`RepoArchitect` is an autonomous developer tool designed for backend engineers and open-source contributors who need to onboard onto complex unfamiliar codebases in under 3 minutes. Given a local workspace path, the agent inspects project structure, detects language ecosystems, discovers API endpoints and routes, extracts environment configurations, and identifies architectural anti-patterns without transmitting code to external servers.

---

## 2. Architecture & Tool Execution Flow

```
+-------------------------------------------------------------------------------+
|                        REPOARCHITECT RUNTIME PIPELINE                         |
|                                                                               |
|   1. CLI TRIGGER                                                              |
|   `python agent.py --repo <path>`                                             |
|          |                                                                    |
|          v                                                                    |
|   2. TOOL INSPECTOR                                                           |
|   - Directory Walk (ignoring .git, node_modules, .venv)                       |
|   - AST / Regex AST Route Parser (FastAPI, Express, Django)                   |
|   - Environment Schema Extractor (.env.example inspection)                    |
|          |                                                                    |
|          v                                                                    |
|   3. REASONING & GUARDRAILS                                                   |
|   - Depth limiter (max depth: 5 levels)                                       |
|   - Secret filter (masks any discovered private keys / credentials)           |
|          |                                                                    |
|          v                                                                    |
|   4. OUTPUT SYNTHESIS                                                         |
|   - Architecture Dossier (`ARCHITECTURE.md`)                                  |
|   - Clean Terminal Summary (Routes, Components, Boundary Risks)               |
+-------------------------------------------------------------------------------+
```

---

## 3. Quickstart & Stranger Reproducibility

Anyone with Python 3.10+ can clone and run `RepoArchitect` in under 60 seconds with zero external API keys:

```bash
# 1. Clone repository
git clone https://github.com/kunalaggarwal/flyrank-internship-portfolio.git
cd "flyrank-internship-portfolio/week-05/FL-07-build-the-agent"

# 2. Run agent against any target directory (e.g., Week 2 CRUD API)
python agent.py --target "../../week-02/BE-01-crud-api"

# 3. View output
cat ARCHITECTURE.md
```

---

## 4. Benchmark Evaluation Results (v2 Eval Suite)

The agent was evaluated against 5 diverse real-world repository layouts:

| Test Case | Repository Pattern | Expected Behavior | Actual Behavior | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Case 1** | Small FastAPI In-Memory CRUD | Detects 5 routes, identifies missing DB persistence | Output flagged in-memory volatile dictionary | **PASS** (100%) |
| **Case 2** | Containerized Postgres Repo | Identifies Docker compose, `.env.example`, SQL schemas | Mapped layered repository pattern cleanly | **PASS** (100%) |
| **Case 3** | Massive Monorepo (Deep Nesting) | Respects max-depth 5 guardrail without stack overflow | Truncated tree at depth 5, logged notice | **PASS** (100%) |
| **Case 4** | Hardcoded Secret Probe | Detects uncommitted fake API key in test script | Redacted token and raised security alert | **PASS** (100%) |
| **Case 5** | Non-Existent Directory | Rejects missing path with exit code 1 (no unhandled 500) | Returned clear error message to terminal | **PASS** (100%) |

---

## 5. Honest Limitations & Failure Modes

1. **Dynamic Runtime Routes:** The agent uses static analysis and regex route matching. Endpoints dynamically generated via runtime metaprogramming (e.g., dynamically registered router factory functions) are not captured in the route inventory.
2. **Binary File Scanning:** The agent skips compiled binary assets (`.so`, `.dll`, `.exe`, `.pyc`) and large datasets to avoid memory exhaustion, meaning embedded SQLite databases are inspected only by filename and size.
3. **No Network Calling:** By design, the agent operates 100% offline; it cannot query GitHub issues or external package registries to verify dependency CVEs.

---

## 6. Demo Video Narrative Script (3–5 Min, No Slides)

**Video Recording Settings:** OBS Studio 1080p 60fps, crisp terminal capture, USB dynamic microphone, zero slide decks.

### Video Run Breakdown:
- **0:00 – 0:45 (Introduction & Problem):**
  - *"Welcome. I'm Kunal Aggarwal. In this demo, I'm showing RepoArchitect, a local developer agent I built for rapid repository onboarding. Instead of clicking through 40 files in VS Code, we run one command."*
- **0:45 – 1:45 (Live Terminal Execution):**
  - Runs `python agent.py --target ./sample-repo`.
  - Explains live terminal output as directory trees, route maps, and environment schemas appear on screen.
- **1:45 – 2:30 (One Design Decision):**
  - Explains the architectural choice to use **local AST and deterministic regex heuristics** rather than shipping repository code to an LLM cloud API.
  - *"This decision preserves $0 operating cost and guarantees that private company source code never leaves the developer's laptop."*
- **2:30 – 3:15 (One Limitation Explained on Camera):**
  - Demonstrates running the agent against a dynamically generated route module. Shows the terminal log gracefully noting the dynamic route limitation.
- **3:15 – 3:45 (Synthesis & Wrap-up):**
  - Shows the generated `ARCHITECTURE.md` file opened in VS Code.
  - Concludes with a preview of how this feeds into the FlyRank backend portfolio.

---

## 7. Transparency Diligence (AI Work Declaration)

In accordance with FlyRank's academic integrity and transparency guidelines:
- **AI Contribution:** Claude 3.5 Sonnet was used as an interactive pair-programming partner to generate initial AST parsing regex patterns and suggest edge-case directories for the `.gitignore` exclusion filter.
- **Human Author Contribution:** Architecture design, guardrail boundary implementation (depth limiting, secret redaction), error handling, CLI UX, and end-to-end evaluation suite design were authored and verified by Kunal Aggarwal. Every line in `agent.py` was reviewed, debugged, and tested locally.
