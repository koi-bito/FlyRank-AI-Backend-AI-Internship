# FlyRank AI — Backend AI Engineering & General AI Fluency

This repository contains the complete portfolio of assignments, systems, and artifacts produced during the FlyRank AI Internship, spanning two core tracks:
1. **Backend AI Engineering (BE)**: Production-grade backend systems, databases, authentication, distributed task workers, polite web scrapers, LLM microservices, PDF reporting pipelines, and interactive AI decision flows.
2. **General AI Fluency (FL & PF)**: Prompt engineering, workflow audits, personal AI agents, automation pipelines, and portfolio demonstrations.

---

## Capstone Project

The engineering capstone has been extracted into its own dedicated production repository with isolated test suites, CI validation, and architecture documentation:

Capstone (Usage Metering & Billing Engine): https://github.com/koi-bito/flyrank-capstone-usage-metering-billing

---

## Repository Structure (Week-by-Week)

### Week 01: Foundations & Workflow Audits
- `week-01/FL-01-workflow-audit/` — Workflow audit and opportunity mapping for AI integration.
- `week-01/draw-the-path/` — Career trajectory and milestone design.
- `week-01/what-are-you-proving/` — Personal thesis and capability proofs.

### Week 02: REST APIs & Prompt Engineering
- `week-02/BE-01-crud-api/` — Production-grade RESTful Task Management API using FastAPI and Pydantic with full test suite.
- `week-02/FL-02-prompting-fundamentals/` — System prompting and evaluation techniques.
- `week-02/frame-it-as-cases/` — Use case structuring and domain modeling.
- `week-02/the-prompt-ladder/` — Progressive prompting frameworks.

### Week 03: Databases & Containerization
- `week-03/BE-02-connecting-database/` — SQLite/SQLAlchemy persistent storage layer with connection pooling, migrations, and schema validation.
- `week-03/BE-04-containerize-stack/` — Dockerized container stack for FastAPI and SQLite with health checks and multi-stage builds.
- `week-03/decide-once-identity-kit/` — Design identity kit and branding guidelines.
- `week-03/kill-your-darlings-images/` — Asset curation and visual editing strategy.
- `week-03/the-through-line/` — Narrative continuity for technical projects.

### Week 04: Authentication & Modern Agent Concepts
- `week-04/BE-03-auth-login-protect/` — Production-ready auth integration with Supabase Auth, JWT verification, role-based access control, and route guards.
- `week-04/FL-04-automation-workflow/` — End-to-end automation pipelines.
- `week-04/FL-05-agent-concepts-mcp/` — Model Context Protocol (MCP) architectural concepts and agent tool definitions.
- `week-04/empty-but-live/` — Live minimal deployment patterns.
- `week-04/three-roads-choose-stack/` — Technical stack evaluation and architectural trade-off analysis.

### Week 05: Polite Web Scraping & Agent Design
- `week-05/BE-05-polite-scraper/` — Rate-limited, resilient web scraper respecting robots.txt, exponential backoff, caching, and quarantine logs.
- `week-05/FL-06-design-personal-agent/` — Specification and architecture for personal autonomous agents.
- `week-05/FL-07-build-the-agent/` — Implementation of personal agent tools and execution loop.
- `week-05/PF-04-personal-website/` — Personal portfolio site.
- `week-05/explain-it-like-you-built-it/` — Deep technical breakdown and architecture walkthroughs.

### Week 06: LLM Behind APIs & Interface Design
- `week-06/BE-07-llm-behind-api/` — Defensive non-conversational LLM triage endpoint with structured JSON outputs and benchmark evaluation suite.
- `week-06/make-it-do-something/` — Interactive UX prototype.
- `week-06/open-it-on-your-phone/` — Mobile-responsive testing and viewport optimization.
- `week-06/survive-the-crit/` — Peer critique defense and design iteration.

### Week 07: Distributed Jobs, PDF Reports & Decision Flows
- `week-07/BE-06-background-job/` — Asynchronous background task worker with job queuing, state machines, and polling endpoints.
- `week-07/BE-08-pdf-report-generator/` — High-fidelity PDF report generator rendering CSS-rich reports via headless Chromium (Playwright).
- `week-07/BE-09-ai-decision-flow/` — Full-stack visual decision tree engine with FastAPI backend and React + Vite frontend (ReactFlow + shadcn UI).
- `week-07/break-your-own-site/` — Chaos testing, vulnerability audits, and edge case fuzzing.
- `week-07/plant-your-flag-domain-badge/` — Domain verification and public identity deployment.

### Week 08: Documentation, Demos & Final Packages
- `week-08/FL-09-documentation-demo-video/` — Agent documentation, system walkthroughs, and demo video narratives.
- `week-08/FL-10-final-package-retrospective/` — Final internship portfolio packaging and engineering retrospective.
- `week-08/the-plan-to-keep-building/` — Post-internship roadmap and continuous development plan.

---

## Getting Started

Each backend module contains its own self-contained environment and `requirements.txt`:
```bash
cd week-02/BE-01-crud-api
pip install -r requirements.txt
python main.py
```
Refer to the individual README in each directory for endpoint specifications, curl examples, and verification proofs.
