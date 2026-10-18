# FL-05: Agent Concepts and MCP (Model Context Protocol) Basics

**Track:** General AI Fluency  
**Code:** FL-05  
**Author:** Kunal Aggarwal  
**Word Count:** ~820 words  
**Date:** October 2026  
**Status:** Completed  

---

## 1. Technical Explainer: Workflows vs. Agents & MCP

### The Core Distinction: Workflows vs. Agents
In modern AI systems engineering, the terms "workflow" and "agent" are frequently conflated, yet they represent fundamentally distinct architectures.

A **workflow** is a deterministic, predefined sequence of steps where LLMs and programmatic functions execute in a hardcoded path. The control flow is orchestrated entirely by code (or a DAG runner like Inngest or LangGraph). Step 1 executes, passes its output to Step 2, and so forth. Even if individual steps leverage generative models, the decision of *what step to execute next* is fixed. My **FL-04 Repository Digest pipeline is strictly a workflow**: it always scans the tree, then synthesizes boundaries, then runs verification rules, then formats the output. It cannot decide to pause, pull git commit history, run a test suite, or backtrack based on an unexpected discovery.

An **agent**, in contrast, is an autonomous system where the **LLM itself controls the execution loop**. Given an overarching objective and a toolset, an agent:
1. Gathers context and observes current state.
2. Reasons about the next optimal action.
3. Decides *dynamically* which tool to call (or whether to conclude).
4. Inspects the tool execution result and repeats the loop until the objective is satisfied or an error threshold is hit.

Where a workflow is an assembly line, an agent is an interactive problem-solver operating in an environment.

---

### Understanding the Model Context Protocol (MCP)
As LLM integrations proliferate, connecting models to internal data sources and tools has historically resulted in fragmented, proprietary integrations. Anthropic's **Model Context Protocol (MCP)** solves this by acting as an open standard (the "USB-C for AI apps") that cleanly decouples AI models from local and remote data providers.

MCP defines three core primitives:
1. **Tools:** Executable functions that the model can invoke to take action or cause side effects (e.g. `run_command`, `git_checkout`, `query_sql_database`). Tools take JSON Schema arguments and return execution results.
2. **Resources:** Read-only data payloads exposed to the model as context (e.g. file contents, database table schemas, API log streams). Resources are URI-addressable (`file:///...`, `postgres://...`).
3. **Prompts:** Pre-engineered prompt templates and conversation starters served by the MCP server to guide the model through complex operational tasks.

---

### Upgrading FL-04 from a Workflow to an Agent
To evolve the FL-04 repository workflow into a full-fledged **Autonomous Codebase Explorer Agent**, three structural components must be introduced:

1. **Tool Invocation via MCP:** Replace static text ingestion with live MCP filesystem and git tools (`read_file`, `git_log`, `grep_search`, `run_tests`). Instead of ingesting the entire repo indiscriminately, the agent dynamically requests only the files it suspects are relevant.
2. **Dynamic Backtracking Loop:** If the agent inspects an endpoint and finds an unfamiliar custom decorator (e.g. `@rate_limited`), it can decide on its own to search the codebase for the decorator's definition rather than guessing its behavior.
3. **Guardrails & Budget Caps:** Because autonomous agents can enter infinite loops or burn API tokens through repeated tool queries, production agents require hard boundary constraints: a maximum iteration limit (e.g. 10 tool calls max), timeout ceilings (30s per action), and permission prompts before executing irreversible side effects (e.g. `git push` or DB drops).

---

## 2. Evidence of Working MCP Tool Execution

Using an MCP-compatible environment with local filesystem and execution connectors, three distinct operations were executed that standard chat interfaces cannot perform without external tool grounding:

### Task 1: Autonomous File System Inspection (`list_dir` & `view_file`)
- **Action:** Inspected local repository tree and verified actual file existence.
- **Tool Invoked:** `list_dir(DirectoryPath="c:/GITHUB Repos/FlyRank AI - Backend AI Internship")`
- **Model Grounding:** Confirmed the exact directory structure and file sizes directly from disk, preventing hallucination of non-existent project files.

### Task 2: Live Shell & Environment Probing (`run_command`)
- **Action:** Executed local runtime checks for Python, Node, and Docker.
- **Tool Invoked:** `run_command(CommandLine="node -v; python --version; docker --version")`
- **Output Captured:** Verified Node v25.9.0, Python 3.13.13, and Docker build 7fc2dff directly from host shell.

### Task 3: Interactive Database Query & State Verification
- **Action:** Queried active SQLite `tasks.db` records created in Week 3.
- **Tool Invoked:** Executed Python database query script to inspect task row counts.
- **Evidence:** Model observed live SQLite rows directly without user copy-pasting text.

---

## 3. Evaluation Checklist

- [x] Explainer is ~820 words, strictly written in original engineering language.
- [x] Workflow vs Agent distinction clearly defined and accurately applied to FL-04.
- [x] Three MCP primitives (Tools, Resources, Prompts) explained with concrete technical roles.
- [x] 3 live tool tasks executed that plain chat could not achieve alone.
- [x] Architectural requirements for upgrading FL-04 to an agent detailed.
