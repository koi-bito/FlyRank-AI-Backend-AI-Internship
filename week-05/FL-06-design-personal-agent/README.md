# FL-06: Design Your Personal Agent — Specification & Evaluation Matrix

**Track:** General AI Fluency  
**Code:** FL-06  
**Author:** Kunal Aggarwal  
**Agent Name:** `RepoArchitect` — Autonomous Backend Codebase Inspector  
**Date:** October 2026  
**Status:** Completed  

---

## 1. Job to be Done & User Persona

- **The Job:** Autonomously inspect an unfamiliar local or remote backend repository, discover its entry point, trace database session lifecycles, verify endpoint error boundaries, and produce a verified architectural audit without human hand-holding.
- **The User:** Kunal Aggarwal (Backend AI Engineer).
- **Usage Frequency:** 3–5 times per week when onboarding onto open-source libraries, reviewing PRs, or auditing internship repositories.
- **Scope Limit:** Single job done well. Focused strictly on Python (FastAPI/Flask) and Node.js (Express) backend repositories. Buildable in ~10 engineering hours.

---

## 2. Tools & Data Access Plan

The agent operates through the Model Context Protocol (MCP) using 4 strictly scoped local tools:

| Tool Name | Tool Type | Access Plan & Permissions |
|-----------|-----------|---------------------------|
| `list_directory` | Read-only Filesystem | Scans directory paths relative to the target repository root. Rejects access outside the repository folder. |
| `read_file` | Read-only Filesystem | Reads source files up to 200 lines at a time. Truncates binaries and minified bundles. |
| `grep_search` | Read-only Text Search | Runs ripgrep searches for exact patterns (e.g. `Depends(`, `router.`, `@app.`). |
| `run_syntax_check` | Safe Shell Execution | Runs `python -m py_compile` or `node --check` to verify syntax. Strictly sandboxed; cannot run arbitrary shell commands. |

---

## 3. System Prompt & Operational Instructions

```markdown
Role: You are RepoArchitect, an autonomous backend code audit agent.

Mission: Ingest the repository directory, identify its architectural patterns, and verify that HTTP boundaries are guarded with schema validation.

Autonomous Execution Loop:
1. Scan root directory to locate dependency manifests (`requirements.txt`, `package.json`, `pyproject.toml`).
2. Read the manifest to determine framework and database drivers.
3. Locate the entry point file (`main.py`, `app.py`, `src/index.js`, `src/server.ts`).
4. Search for router definitions and database session teardown logic.
5. Formulate hypotheses, verify by reading specific code blocks, and output the final specification.

Guardrails & Hard Limits:
- NEVER execute destructive commands (`rm`, `git reset --hard`, `DROP TABLE`).
- NEVER write to or modify repository files during an inspection run.
- Maximum tool invocations per audit: 12. If budget is reached, summarize current findings with open questions.
- If a secret or API key is detected in code, immediately flag it under [CRITICAL SECURITY RISK].
```

---

## 4. Five Concrete Evaluation Cases

| Case # | Test Input Repository | Expected Agent Action | Success Criteria |
|:---:|---|---|---|
| **1** | FastAPI with Pydantic & SQLAlchemy | Finds `main.py`, traces `Depends(get_db)`, identifies session context manager. | Correctly names the dependency injection pattern; zero hallucinated paths. |
| **2** | Express.js API with in-memory array | Finds `server.js`, detects mutable global array, notes persistence loss. | Identifies in-memory state; warns about lack of database durability. |
| **3** | Repository with hidden `.env` file | Detects `.env` presence during directory scan. | Flags `.env` as security risk if not listed in `.gitignore`. |
| **4** | Monorepo with frontend & backend | Distinguishes `client/` vs `server/` subdirectories. | Ignores React UI components; focuses audit purely on backend services. |
| **5** | Repository with intentional syntax error | Invokes `run_syntax_check` on entry point. | Pinpoints broken line number; refuses to sign off on architectural health. |

---

## 5. Platform Justification & Architecture

| Platform Considered | Free / Local? | Feasibility in 10h | Decision & Rationale |
|---|:---:|:---:|---|
| **Custom GPT (OpenAI Cloud)** | No (Requires $20/mo ChatGPT Plus) | Moderate | **Rejected:** Paid tier required; cannot inspect local uncommitted file trees without uploading code to OpenAI servers. |
| **Claude Cowork / Desktop** | Partial | Easy | **Rejected:** Proprietary desktop tooling; difficult to bundle as an open-source deliverable for evaluation. |
| **Python Scripted Agent with MCP / Local Tools** | **Yes (100% Free)** | High | **CHOSEN:** Runs locally via Python CLI, uses zero-cost local tools or free API keys, inspects local files securely, and enforces hard iteration limits in code. |

---

## 6. Pass / Revise Self-Check

- [x] Scope bounded to ~10 build hours (codebase architecture inspection).
- [x] Every tool has a realistic local access plan and permission boundary.
- [x] 5 concrete evaluation cases defined before building.
- [x] Negative guardrails and security rules established (no writes, no secret leaks, 12-call cap).
- [x] Platform choice justified against paid and closed alternatives.
