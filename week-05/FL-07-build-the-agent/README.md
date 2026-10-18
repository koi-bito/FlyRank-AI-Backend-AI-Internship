# FL-07: Build the Agent — Working MVP & Execution Log

**Track:** General AI Fluency  
**Code:** FL-07  
**Author:** Kunal Aggarwal  
**Agent Name:** `RepoArchitect`  
**Date:** October 2026  
**Status:** Completed  

---

## 1. MVP Overview

Following the specification in **FL-06**, `RepoArchitect` was implemented in Python as an autonomous codebase inspection agent. It connects to real, sandboxed local filesystem and search tools via an MCP-compliant registry:
- **Autonomous Reasoning Loop:** Dynamically decides which directory to list, which entry point to ingest, and what patterns to grep based on emerging discoveries.
- **Security Guardrails:** Rejects any path traversing outside the target workspace; scans for uncommitted `.env` files; strictly limits execution depth to 8 tool calls to prevent runaway loops.
- **Live Tool Connections:** `list_directory`, `read_file`, `grep_search`.

---

## 2. Real Execution Traces

### Run 1: Auditing `week-04/BE-03-auth-login-protect`
```bash
python agent.py ../../week-04/BE-03-auth-login-protect
```
**Output:**
```
[*] Starting RepoArchitect Agent on workspace: .../week-04/BE-03-auth-login-protect
[Tool: list_directory] Discovered root files: ['auth.py', 'main.py', 'README.md', 'test_api.py']
[Tool: read_file] Ingested entry point main.py
[Tool: grep_search] Found 1 auth indicators

=== FINAL REPOARCHITECT AUDIT REPORT ===
{
  "entry_point": "main.py",
  "framework": "FastAPI (Python)",
  "persistence": "None detected",
  "auth": "JWT Bearer detected in auth.py",
  "security_risks": [],
  "files_analyzed": [
    "main.py",
    "auth.py"
  ]
}
```

### Run 2: Auditing `week-05/BE-05-polite-scraper`
```bash
python agent.py ../BE-05-polite-scraper
```
**Output:**
```
[*] Starting RepoArchitect Agent on workspace: .../week-05/BE-05-polite-scraper
[Tool: list_directory] Discovered root files: ['output', 'README.md', 'scraper.py']
[Tool: read_file] Ingested entry point scraper.py
[Tool: grep_search] Found 0 persistence indicators

=== FINAL REPOARCHITECT AUDIT REPORT ===
{
  "entry_point": "scraper.py",
  "framework": "Unknown",
  "persistence": "None detected",
  "auth": "None detected",
  "security_risks": [],
  "files_analyzed": [
    "scraper.py"
  ]
}
```

---

## 3. The Build Log: Real Engineering Iteration

| Issue / Failure Encountered | What Changed in Response | What Was Cut & Why |
|---|---|---|
| **Path Traversal Vulnerability:** Initial `read_file` accepted arbitrary relative paths like `../../../../windows/system32`. | Added `_resolve_safe_path()` using `os.path.commonpath` to throw a `PermissionError` if any path escapes the workspace root. | Bounded workspace traversal strictly to target directory. |
| **Grep Buffer Overflow:** Searching for common terms in large directories returned thousands of matches, freezing the agent. | Added a hard cap of 15 matches maximum per search in `grep_search`. | Cut deep regex syntax options in favor of fast, simple pattern matching. |
| **Token Budget & Runaway Loops:** Spec called for arbitrary re-prompting loops. | Implemented hard iteration counter (`max_iterations=8`). If the agent does not reach a conclusion in 8 tool calls, it cleanly terminates and summarizes current findings. | Cut autonomous shell script modification to guarantee safety (read-only mode). |

---

## 4. Evaluation Checklist

- [x] Agent completes its core inspection job end-to-end without manual intervention.
- [x] At least 3 live local tools (`list_directory`, `read_file`, `grep_search`) connected.
- [x] Matches FL-06 specification with documented guardrails.
- [x] Build log captures authentic development iterations and safety adjustments.
- [x] Execution traces verify multi-repository audits.
