# FlyRank Internship — Master Task Tracker

**Intern:** Kunal Aggarwal
**Tracks enrolled:** General AI Fluency (optional track, do it fully) + Backend AI Engineering (main/declared track)
**Goal:** Complete ALL assignments across both tracks, plus at least 1 capstone per track (more if time allows).
**Internship structure:** Fully self-paced, no deadlines, indefinite portal access. Weekly labels are guidelines only — work in any order, but this file is organized week-by-week per the portal's own labeling for folder organization.
**Certificate requirement (minimum, not the goal here):** 5 assignments + 1 capstone per track. You're aiming for everything.

> **How to use this file:** Each `##` heading is one assignment/task. Mirror this structure in your IDE: one folder per `#` Week heading, one subfolder per `##` assignment inside it. Capstones are pulled into their own top-level `CAPSTONES` section near the end since there are multiple options per track and only one is required — build once you've picked.

---

## 💰 PAYMENT / COST FLAGS — read before starting

Everything in this entire program can be done for $0. The ONLY two friction points:

| Where                                               | The issue                                                            | The free fix                                                                                                                                        |
| --------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **BE-07 — Connect to an AI API** (Week 6)           | Anthropic Claude API has no free tier (intern reported spending ~$5) | Use **OpenRouter** (`openrouter/free` model, free, no card) or **Ollama** (fully local, no card) instead. FlyRank explicitly confirms this is fine. |
| **"Plant Your Flag" — Domain + Badge** (Week 7, FL) | A real custom domain costs ~$10–15/year                              | A free subdomain (Netlify/Vercel/GitHub Pages) is an **explicitly accepted fallback**, no penalty                                                   |
| **Capstone: LLM Usage Metering & Billing**          | Needs Stripe — if your country isn't supported (e.g. Pakistan)       | Use mocked/test fixtures with the Stripe SDK, or swap to Razorpay — FlyRank confirmed both are fine                                                 |

Everything else — Netlify, Supabase, SQLite, Docker + Postgres, GitHub, Claude.ai/ChatGPT free tier, Anthropic Academy, Inngest, Playwright, Gemini free tier, Telegram/Discord/Mastodon bots — is **100% free, no credit card, ever.**

---

## 📌 General rules that apply to EVERY assignment in this file

- **Submission:** Portal submission box on each assignment card. Accepts a public URL, pasted notes, or an uploaded file — your choice, any format (PDF, Word, Google Doc link, etc.) works for every single assignment.
- **No deadlines anywhere.** Weekly labels are suggestions only.
- **AI tool choice is always free:** Claude, ChatGPT, Gemini — use whichever is available/not rate-limited. No FlyRank-provided paid subscriptions exist.
- **"Track thread" = the submission box** on the assignment card. This confused dozens of interns in the Q&A — it is NOT a separate forum/Slack thread.
- **For Backend (BE) assignments specifically:**
  - Any language/framework is accepted (not just the JS/Python "lanes" — .NET, Go, PHP, TypeScript, Golang have all been explicitly approved in Q&A).
  - You can build every assignment in one repo (with clear subfolders) OR a separate repo per assignment — both accepted, just stay consistent.
  - Never commit `.env` files or API keys. Always `.gitignore` them and ship a `.env.example`.
  - "AI vs Me" bonus stages are optional but genuinely good learning — recommended, not required.

---

# WEEK 1

## FL-01 — AI Workflow Audit and Tool Setup

**Track:** General AI Fluency | **Workload:** ~4h | **Phase:** Onboarding

### Why it matters

You can't improve a workflow you've never mapped. This audit is the foundation every later AI Fluency assignment reuses.

### Brief

1. List **10–15 recurring tasks** from your real week (study, FlyRank internship, Deccan AI work, side projects, coursework). Classify each into one of four buckets: **just me** / **delegate to AI with review** / **collaborate with AI** / **fully automate**. One line of rationale per task.
2. Set up your free toolkit: Claude, ChatGPT, and Anthropic Academy accounts. Enroll in **AI Fluency: Framework & Foundations** (Anthropic Academy) and complete at least the first module. (This course is OPTIONAL per FlyRank Q&A, but encouraged — do it if time allows.)
3. Create **one Claude Project** with custom instructions: who you are, tone preferences, current goals.
4. Pick **three audit tasks** you'll reuse in FL-02 through FL-04, and define what "done well" means for each.

### Deliverable

A 1–2 page workflow audit (table format) + a screenshot of your configured Claude Project + your three target tasks with success definitions.

### Evaluation criteria (pass/revise)

- 10+ tasks are genuinely yours, not generic examples
- Every task classified with a one-line rationale
- At least 2 tasks honestly marked "just me" with a reason
- Three target tasks are specific with measurable success definitions
- Tool accounts + Academy enrollment evidenced

### Suggested target tasks (from our planning conversation — feel free to use/adapt)

1. **GitHub repo understanding assistant** — Given any public repo URL, AI produces a clear architecture summary, file map, and answers 3 specific questions about the codebase accurately. (Ties into your interest in building a "chat with your codebase" tool — good side-project seed too.)
2. **Job application cold emails / outreach**
3. **Technical README / project writeups**

### Resources

- "On-boarding your AI Intern" (Ethan Mollick) — the task-classification framework this is based on
- AI Fluency: Framework & Foundations (Anthropic Academy) — optional, free, certified
- "What are projects?" (Claude Help Center) — how Claude Projects work

### Clarifications from Q&A

- Submit however is easiest: Word doc, Google Doc link, PDF, even a photo of a handwritten table converted via AI.
- No deadline; self-paced.

---

## Draw the Path — Portfolio Sitemap + Toolkit

**Track:** General AI Fluency | **Workload:** ~3h | **Phase:** Setup

### Why it matters

Before building your portfolio, map the minimum pages it needs — nothing more.

### Brief

1. Sketch a **portfolio sitemap**: the few pages it takes to walk one visitor from landing → believing you → one action. Usually: hero (states the claim) + work/case-studies + short about + contact. Resist adding pages "just because."
2. Set up free toolkit accounts: **Claude, ChatGPT, Gemini, and Perplexity.**
3. Create **one Claude Project** named for this build, with custom instructions (your proof statement pasted in — see "What Are You Proving?" below) and a request to act as a tutor. This Project follows you for all 8 weeks.
4. Run one real prompt: have it **pressure-test your sitemap** against your one action and your claim. Save the answer.

### Deliverable

A photo of your sitemap sketch + a screenshot of your configured Claude Project + the pressure-test prompt and output.

### Pass/revise

- Sitemap is small; every page earns its place against the claim and the one action
- Claude Project has genuine custom instructions (not defaults)
- First prompt pressure-tested the map; you noted ≥1 thing you'll change

### Clarifications from Q&A

- Any AI tool is fine, not Claude exclusively.
- Submit as Google Drive link, PDF, or whatever works.

---

## What Are You Proving?

**Track:** General AI Fluency | **Workload:** ~2h | **Phase:** Setup

### Why it matters

A portfolio with no claim is decoration. This is the single most useful hour of the whole track — everything downstream depends on it.

### Brief

1. Write a **one-paragraph proof statement** answering three questions plainly:
   - **The one claim** — one primary skill, named. ("I can design usable interfaces," not "I'm creative.")
   - **The one person** — a specific person who could hire/engage you, not "people."
   - **The one action** — the single most important thing you want them to do (email you, hire you, download your CV, book a call, try your thing).
2. Use AI as a thinking partner, not an author: have it interview you with sharp questions until the claim is genuinely narrow and true. Push back until it's yours.
3. Write **one honest line** on why this needs to exist — what you can't prove with a CV/LinkedIn alone that owning this fixes.

### Deliverable

The one-paragraph proof statement (claim + person + action) + the one-line "why."

### Pass/revise

- One primary claim named, not three skills hiding behind "and"
- Audience is a specific person who could hire you, not "everyone"
- A single most-important action is chosen
- The statement could only describe YOUR proof, not any portfolio

### Clarifications from Q&A

- Submit as PDF, notes, Google Doc — any format.

---

# WEEK 2

## BE-01 — Build your first CRUD API

**Track:** Backend AI Engineering | **Code:** BE-01 | **Workload:** ~3h | **Phase:** Foundations

### Goal

Build a small API that manages a to-do list (full CRUD: Create, Read, Update, Delete). See and test it via Swagger UI, publish to GitHub.

### Purpose

CRUD is the heartbeat of almost every backend. Data lives only in memory for now (no DB — that's next assignment). Everything is submitted through GitHub.

### Tools — pick ONE lane (any language actually accepted per Q&A)

|            | JavaScript lane               | Python lane         |
| ---------- | ----------------------------- | ------------------- |
| Language   | Node.js                       | Python 3.10+        |
| Framework  | Express                       | FastAPI             |
| Swagger UI | `swagger-ui-express` (manual) | built-in at `/docs` |
| Testing    | curl + browser + Hoppscotch   | same                |

### The six stages

**Stage 0 — Hello, server (~30min)**

- Install Node or Python. Start a server on localhost (Express port 3000, FastAPI port 8000).
- Checkpoint: `curl -i http://localhost:3000/` returns 200 + your message.
- Commit: `Stage 0: hello server`

**Stage 1 — Your first real endpoint (~45min)**

- `GET /` → `{ "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }`
- `GET /health` → `{ "status": "ok" }`
- Checkpoint: both URLs return JSON via browser and curl.
- Commit: `Stage 1: root and health endpoints`

**Stage 2 — Read: list and single task (~1h)**

- In-memory list of task objects, pre-filled with 3 example tasks: `id`, `title`, `done`.
- `GET /tasks` → whole list. `GET /tasks/:id` → one task; unknown id → `404` + `{ "error": "Task 99 not found" }`.
- Checkpoint: `curl -i .../tasks/1` → 200 + task. `curl -i .../tasks/99` → 404 + error JSON.
- Commit: `Stage 2: read endpoints with 404`

**Stage 3 — Create: POST a new task (~1h)**

- `POST /tasks` with `{ "title": "Buy milk" }` → assigns next id, `done: false`, returns created task with `201`.
- Validate: missing/empty title → `400` with JSON error.
- Checkpoint: POST returns 201 + task; a follow-up GET /tasks shows it; posting `{}` → 400.
- Commit: `Stage 3: create with validation`

**Stage 4 — Update & Delete (~1h)**

- `PUT /tasks/:id` replaces title/done. Unknown id → 404. Invalid body → 400.
- `DELETE /tasks/:id` removes task, returns `204` (empty body). Unknown id → 404.
- Checkpoint: full CRUD cycle via curl with correct codes (201, 200, 204, 404).
- Commit: `Stage 4: full CRUD`

**Stage 5 — See it: Swagger UI (~1–1.5h)**

- Python: `/docs` is automatic via FastAPI — add one-line descriptions per endpoint.
- JS: install `swagger-ui-express`, write a small `openapi.json` describing your 5 endpoints, serve at `/docs`.
- Do the full CRUD cycle via Swagger's "Try it out," no curl.
- Checkpoint: screenshot `/docs` showing all endpoints working.
- Commit: `Stage 5: Swagger UI`

**Stage 6 — Publish to GitHub (~1h)**

- Public repo, push code (≥6 commits from the stages above).
- README: what this is, how to install & run (one command), endpoint table, one pasted curl output, Swagger screenshot.
- Commit: `Stage 6: publish and docs`

### Optional extras (★ not required)

- Query filtering: `GET /tasks?done=true`
- Search: `GET /tasks?search=milk`
- Stats endpoint: `GET /stats` → `{ total, done, open }`
- Seed & reset: `POST /reset`
- **The mortality experiment**: restart server, `GET /tasks`, write 2 sentences on what happened — this sets up Week 3's DB assignment.

### Stage 7 — Bonus: the AI rematch (~1h, optional)

Write your own prompt (don't copy from the brief) asking an AI to build the same API from memory-specs. Put AI's code in `ai-version/` folder — never touch your hand-built code. Run your Stage 4 checkpoints against it. Write an "AI vs me" README section: what AI did better, what it got wrong/silently ignored, what your prompt forgot to specify. Do one rematch with an improved prompt.

### Requirements checklist

- [ ] Server starts with one documented command
- [ ] Full CRUD on in-memory list, all 5 endpoints work
- [ ] Correct status codes everywhere (200/201/204/400/404), JSON error messages
- [ ] POST/PUT validate input
- [ ] Swagger UI at `/docs`, full CRUD cycle works via "Try it out"
- [ ] Public GitHub repo, ≥6 commits, README with run instructions + endpoint table + curl output + Swagger screenshot

### Stretch (optional)

- Generate OpenAPI spec from code comments (`swagger-jsdoc`) instead of hand-written file (Express lane)
- Pagination: `GET /tasks?limit=2&offset=2`
- Stage 7 AI rematch (see above)

### Clarifications from Q&A

- Any language welcome (.NET, Go, TypeScript all confirmed fine)
- Deployment NOT required — just public GitHub repo link
- No deadline

---

## FL-02 — Prompting Fundamentals on Real Tasks v2

**Track:** General AI Fluency | **Code:** FL-02 | **Workload:** ~6h | **Phase:** Foundations

### Why it matters

The gap between a lazy prompt and an engineered one is the cheapest performance upgrade in AI.

### Brief

1. Work through the basics chapters of the **Anthropic Prompt Engineering Interactive Tutorial**.
2. Take ONE of your FL-01 target tasks. Write the naive one-line prompt you'd have used before this track; save the output.
3. Iterate **at least 5 more versions**, each applying ONE named technique: role assignment, context/motivation, few-shot examples, output structure, step decomposition. Save every version + output.
4. Run the final prompt on **both Claude and ChatGPT**. Compare honestly: tone, accuracy, structure, failure points.
5. Distill into **one reusable prompt template** a stranger could apply.

### Deliverable

A prompt iteration log: the task, all 6 versions with outputs, a note per iteration on what changed and why, the cross-model comparison, the final template.

### Evaluation criteria

- 5+ iterations beyond naive version, each tied to a named technique
- Notes explain the observed OUTPUT difference, not just the prompt change
- Cross-model comparison says something specific, not "both were fine"
- Final template is reusable without your personal context
- Work is on a real task from your FL-01 audit

### Resources

- Prompting best practices (Claude Docs)
- Prompt engineering best practices for ChatGPT (OpenAI Help)
- Anthropic Prompt Engineering Interactive Tutorial + DAIR.AI Prompt Engineering Guide (resource library)

### Clarifications from Q&A

- Can use any work from your repo, doesn't have to literally be from FL-01.
- Submit as PDF or chat transcript — both fine.

---

## Frame It as Cases: Work That Speaks for Itself

**Track:** General AI Fluency | **Workload:** ~3h | **Phase:** Foundations

### Why it matters

A portfolio is mostly the framing around the work. AI means you never face a blank page — but only if you use it to surface YOUR decisions and results, not a generic story.

### Brief

1. Write a **voice card**: 5–7 words for how you want to sound (e.g. "direct, warm, plain, no buzzwords"). Add it to your Claude Project as a standing instruction.
2. **Be interviewed**: pick each real piece of work (start with what you're building in this internship) and have AI ask you about it, one question at a time, until the problem, your decisions, and the outcome are clear. Answer honestly and messily.
3. Draft each piece into a **case study with three beats**: the problem → what you did (and decided) → what came of it, plus bio and contact/CTA copy. Direct AI to use your words and keep your voice.
4. **Edit hard.** Read every line out loud; cut anything you wouldn't say.

### Deliverable

The framed cases for every piece the sitemap calls for (one document) with your voice card at the top, plus one before/after: a generic AI line and your edited version.

### Pass/revise

- A framed case exists for each piece the sitemap calls for
- Each case has the three beats, could only describe their project
- Sounds like a specific person; before/after shows the difference
- Speaks to the one audience, points at the one action; no "results-driven" filler

---

## The Prompt Ladder

**Track:** General AI Fluency | **Workload:** ~2h | **Phase:** Foundations

### Why it matters

Most people change 5 things at once and learn nothing. This forces discipline: one change at a time, output compared at every step.

### The task

1. Start with a genuinely weak prompt from your own track (e.g. "Build a website," "Write backend code," "Summarize this article"). Run it, save the output — your baseline, should be a little embarrassing.
2. Improve across **5 versions**. Each version adds exactly ONE layer (pick from: clearer goal, defined audience, real context, output format, constraints, examples of good output, quality criteria, review instructions, stated assumptions, verification requirements). One layer per version, no bundling.
3. Run every version, compare output against the previous one side by side.
4. For each version, write 4 short notes: what changed in the prompt, what actually improved in the OUTPUT, what still failed, what you'd try next.
5. Finish with your final best prompt, cleaned up so a stranger on your track could use it without you.

### Deliverable

A prompt ladder document: weak baseline + 5 versions + outputs + 4 notes per version + final reusable prompt.

### Pass/revise

- 6 runs total (baseline + 5), each tied to exactly one named layer
- Notes describe OUTPUT changes, not just prompt changes
- At least one honest "this didn't help" moment — if everything improved smoothly, you weren't looking hard enough
- Final prompt works for a stranger

---

# WEEK 3

## BE-02 — A2 Connecting to the database

**Track:** Backend AI Engineering | **Code:** BE-02 | **Workload:** ~4h | **Phase:** Foundations

### Goal

Take your BE-01 CRUD API and replace the in-memory task list with a real **SQLite** database. Endpoints behave identically — but data now survives a restart.

### Tools

SQLite (`better-sqlite3` for JS, `SQLModel`/`sqlite3` for Python). No installation needed — requires no server.

### The six stages

**Stage 0 — Create your database (~30min)**

- Create `tasks.db` with a `tasks` table: `id` (int PK), `title` (text), `done` (boolean).
- On startup: create table if missing; insert 3 example tasks only if table is empty.
- Checkpoint: restart repeatedly — example tasks appear only once.
- Commit: `Stage 0: create SQLite database`

**Stage 1 — Read from the database (~45min)**

- `GET /tasks` and `GET /tasks/{id}` now run real SQL queries. Unknown id → 404 still.
- Commit: `Stage 1: database read endpoints`

**Stage 2 — Create new tasks (~45min)**

- `POST /tasks` inserts a row. Same validation (missing title → 400, success → 201).
- Checkpoint: create tasks, restart server, `GET /tasks` again — tasks still exist (first time data survives a restart!).
- Commit: `Stage 2: insert into database`

**Stage 3 — Update and delete (~45min)**

- `PUT`/`DELETE` now run SQL UPDATE/DELETE. API behavior identical to before.
- Commit: `Stage 3: update and delete with SQL`

**Stage 4 — Learn your first SQL (~45min)**

- Open DB with any SQLite viewer (DB Browser for SQLite recommended). Run manually: `SELECT * FROM tasks;`, `SELECT * FROM tasks WHERE done = 1;`, `SELECT COUNT(*) FROM tasks;`, `UPDATE tasks SET done = 1;`, `DELETE FROM tasks WHERE done = 1;`. Notice the API reflects these changes immediately.
- Commit: `Stage 4: explored SQLite`

**Stage 5 — Publish your database project (~30min)**

- Update README: why SQLite, where the DB file lives, how to start, a screenshot of your DB viewer, one example SQL query you ran.
- Commit: `Stage 5: database documentation`

### Optional extras

- Search via SQL `LIKE`, filter completed via `WHERE`, sort alphabetically, `GET /stats` using `COUNT()`, add `created_at`/`updated_at` timestamps.

### Requirements checklist

- [ ] Same CRUD endpoints as BE-01, now backed by SQLite
- [ ] Data survives restarts; DB and table auto-create if missing
- [ ] 3 example tasks insert only on first run
- [ ] CRUD uses SQL queries; 404/400 behavior preserved
- [ ] Public GitHub repo updated, README + DB screenshot

### Clarifications from Q&A

- PostgreSQL or MySQL instead of SQLite — both explicitly fine.
- Can reuse the same repo or make a new one.

---

## BE-04 — A3 Containerize your stack

**Track:** Backend AI Engineering | **Code:** BE-04 | **Workload:** ~6h | **Phase:** Foundations

### Goal

Run Postgres in Docker, connect your BE-02 service to it (swapping the in-memory/SQLite store for a real Postgres repository), start app + database together with ONE command.

### Purpose

Proves "switch storage" really does change only one file — your layering from BE-02 proving itself. Every later week (jobs, caching, RAG) assumes this local stack exists.

### The task

1. Start Postgres in Docker with a **volume** so data persists (exact command in Docker guide).
2. Connection string in `.env` (gitignored), with a committed `.env.example`.
3. Create your table with one SQL file or tiny init script.
4. Write a **Postgres repository** implementing the same interface as your in-memory one, swap it in. **Service and routes must not change** — this is the architecture proving itself.
5. `docker-compose.yml`: app + database together; `docker compose up` runs the whole stack.
6. Prove persistence: create rows → restart app and container → rows still there.

### Requirements checklist

- [ ] Postgres runs in Docker with a volume; whole stack starts with `docker compose up`
- [ ] Connection string from `.env` (gitignored, `.env.example` committed)
- [ ] A Postgres repository replaced the in-memory one — service and routes unchanged (say so honestly in README)
- [ ] Persistence proven across an app + container restart (document how you checked)

### Stretch (optional)

- Add Redis to compose file (useful for Week 7 background jobs), ping it from the app
- Add one index, show `EXPLAIN ANALYZE` before/after on a seeded table

### Clarifications from Q&A

- Fine to containerize SQLite instead of Postgres if that's what you used in BE-02.
- SQL Server instead of Postgres — also fine, no mandatory DB engine.

---

## Decide Once: Build Your Identity Kit

**Track:** General AI Fluency | **Workload:** ~2h | **Phase:** Foundations

### Brief

1. Choose your **type**: 1–2 free fonts (heading + body; can be same).
2. Choose your **palette**: main color, near-black text, near-white background, at most one accent — calm enough that your work is the loudest thing.
3. Make a **logo/favicon**: your name in your heading font, or a clean monogram. Keep simple.
4. Write a **two-line style note** (fonts, hex codes, one sentence on mood) and add it to your Claude Project.

### Deliverable

Identity kit on one page: fonts named, palette with hex codes, logo/favicon, two-line style note.

### Pass/revise

- 1–2 fonts, not a pile
- Tight palette (~3–4 colors) with actual hex codes
- Simple logo/favicon exists
- Style note describes one coherent mood

---

## Consistency, Not Talent (and Frame, Not Upstage)

**Track:** General AI Fluency | **Workload:** 90min

A live-session/study topic (not a standalone deliverable assignment per se, but tracked here): the few simple choices that make any site feel intentional (no design talent required), the rule that design frames the work and never upstages it, and judging AI-generated images — deciding which serves your proof, rejecting the rest, and knowing when a real screenshot beats anything generated. Link: aifluency.flyrank.ai/week-03.html

---

## Kill your darlings: Curate Your Images

**Track:** General AI Fluency | **Workload:** ~2h | **Phase:** Foundations

### Brief

1. List the images your portfolio actually needs, matching the content map. Most should be REAL: screenshots, photos of actual work.
2. For your work: use real captures, clean/cropped/legible. For connective tissue (hero texture, icons): generate options in one consistent style/mood matching your kit; iterate the prompt to hold the style steady.
3. For anything that is YOU: use a real photo. Note where you made each call.
4. **Curate ruthlessly.** Write 1–2 lines on a generated image you rejected and why — this is the graded discernment part.

### Deliverable

Final image set (the keepers) + the short rejection note + where you chose real capture over AI.

### Pass/revise

- Images map to real needs; work shown with real captures, not AI stand-ins
- Any AI-generated images share one consistent style/mood
- Real photo used where subject is you
- Rejection note shows genuine judgment, not just "I liked this one"

---

## The Through-Line: Map Content & CTAs

**Track:** General AI Fluency | **Workload:** ~2h | **Phase:** Foundations

### Brief

1. Write your **one-line claim**: the single sentence a visitor should remember. (Use AI for 10 options, then pick/sharpen one yourself.)
2. Build a **content map**: for each page, list sections in order, decide which cases sit where (strongest leads), name the **call to action** — all laddering up to your one action from Week 1.
3. Note any proof you still need to gather (screenshots, live demo link, repo, before/after numbers, testimonial) — including internship work not yet finished.

### Deliverable

One-line claim + content map (pages → sections → which case → CTA) + "still need to gather" list.

### Pass/revise

- Single memorable claim, not a paragraph
- Every page has ordered sections + named CTA; strongest work leads
- CTAs ladder up to the one action from Chapter 1
- Gather-list is honest so the build week isn't blocked

---

# WEEK 4

## BE-03 — Auth: Login & Protect

**Track:** Backend AI Engineering | **Code:** BE-03 | **Workload:** ~6h | **Phase:** Build

### Goal

Build a secure API with Sign Up, Log In, Log Out, and protected routes using **Supabase Auth**. Issue/verify JWTs, protect "user-only" endpoints, test in Swagger, publish.

### The trust triangle

Client → Supabase (credentials) → JWT issued → Client sends JWT in `Authorization: Bearer <token>` header → Your backend verifies it → opens the protected door.

### Routes to build

- `POST /auth/signup` — `{ email, password }` → Supabase `signUp()`
- `POST /auth/login` — `{ email, password }` → Supabase `signInWithPassword()`
- `POST /auth/logout` — protected, calls Supabase `signOut()`
- `GET /protected/profile` — requires valid Bearer token
- `GET /public/info` — no auth required

### Tools

Supabase (free account, no card) + Next.js/Express (JS) or FastAPI (Python).

### The six stages

**Stage 0 — Setup Supabase & Server (~45min)**

- Create free Supabase project. Get Project URL + Anon Key. `.env`: `SUPABASE_URL`, `SUPABASE_KEY`, `PORT`.
- Checkpoint: server logs "connected to Supabase" with no errors.
- Commit: `Stage 0: setup server and supabase client`

**Stage 1 — Open Auth: Sign Up & Log In (~1h)**

- `POST /auth/signup`: missing fields → 400; success → 201 + user object.
- `POST /auth/login`: missing fields → 400; wrong password → 401 `{ "error": "Invalid login credentials" }`; success → 200 + access_token + refresh_token.
- Checkpoint: curl signup then login, confirm `access_token` string returned.
- Commit: `Stage 1: signup and login routes working`

**Stage 2 — Public & Protected Gates (~1h)**

- `GET /public/info` → 200, no auth.
- `GET /protected/profile` → if header missing/malformed → 401 `{ "error": "Access token required" }`.
- Commit: `Stage 2: public route and unverified protected route`

**Stage 3 — The Guard: Token Verification (~1h)**

- `GET /protected/profile` now actually verifies via Supabase `getUser(token)`. Expired/tampered token → 401 `{ "error": "Invalid or expired token" }`. Valid → 200 + user metadata.
- Checkpoint: valid token → 200 + details; one changed character → 401.
- Commit: `Stage 3: profile route token verification`

**Stage 4 — Middleware Protection & Logout (~1.5h)**

- Extract token-checking into reusable **middleware** (Express) / **dependency** (FastAPI). Apply to `/protected/profile`.
- `POST /auth/logout`: protected route, calls Supabase sign out, returns 204.
- Checkpoint: add a second protected route using the same middleware — confirm it auto-rejects/permits correctly.
- Commit: `Stage 4: auth middleware and logout endpoint`

**Stage 5 — Swagger UI (~1–1.5h)**

- Python: configure FastAPI's `HTTPBearer` security scheme for the "Authorize" padlock.
- JS: define `securitySchemes` block (type `http`, scheme `bearer`) in `openapi.json`.
- Checkpoint: screenshot showing lock icon on protected routes, successful authorized test.
- Commit: `Stage 5: Swagger UI documentation with bearer auth`

**Stage 6 — Publish to GitHub (~1h)**

- **CRITICAL:** `.env` in `.gitignore`. NEVER commit Supabase keys.
- README: what this is, env var setup, how to run, API reference table (endpoint + auth required y/n), Swagger screenshot.
- Commit: `Stage 6: publish to GitHub and write README`

### Stage 7 — Bonus: AI Rematch (optional ~1h)

Prompt an AI to build the same setup from memory-spec. Analyze: Bearer-prefix parsing, security flaws, what your prompt missed.

### Requirements checklist

- [ ] Server starts with one command
- [ ] `.env` used properly, gitignored
- [ ] Signup/login communicate with Supabase Auth
- [ ] `/protected/profile` extracts+verifies Bearer token
- [ ] Correct status codes: 201/200/204/400/401
- [ ] Auth check extracted into reusable middleware/dependency
- [ ] Swagger UI with Bearer auth functional
- [ ] Public GitHub repo, ≥6 commits, comprehensive README

### Clarifications from Q&A

- Neon instead of Supabase — fine. Fastify/Prisma instead of Next.js — fine, doesn't have to be Next.js specifically.

---

## FL-05 — Agent Concepts and MCP Basics

**Track:** General AI Fluency | **Code:** FL-05 | **Workload:** ~5h | **Phase:** Build (core)

### Why it matters

"Agent" is the most abused word in AI right now. This separates people who can evaluate agent products from people who repeat marketing copy.

### Brief

1. Read "Building Effective Agents" (Anthropic Engineering). In your own words, write the difference between a **workflow** and an **agent**, and classify your FL-04 pipeline as one or the other.
2. Read the MCP introduction; understand the three primitives: **tools, resources, prompts**.
3. Connect **one MCP server or connector** to Claude (any MCP client counts). Run **3 tasks** through it that chat alone couldn't do (e.g. reading local files, querying a live service).
4. Write a **600–900 word explainer**: what an agent is, what MCP is, what your FL-04 workflow would need to become an agent.

### Deliverable

The explainer + evidence of one working MCP/connector setup (screenshots of the 3 tasks running tool calls).

### Evaluation criteria

- Explainer technically correct, clearly your own words
- Workflow vs agent distinction applied accurately to your FL-04 build
- Connector demonstrably working: outputs show tool use, not plain chat
- 3 tasks chat alone couldn't have done
- One concrete agent upgrade named for your pipeline

### Resources

- "Building Effective Agents" (Anthropic Engineering) — canonical essay
- "What is MCP?" (Model Context Protocol Docs)
- "Introduction to Model Context Protocol" (Anthropic Academy, optional Python deep dive)

---

## FL-04 — Ship an Automation Workflow v2

**Track:** General AI Fluency | **Code:** FL-04 | **Workload:** ~7h | **Phase:** Build (core)

### Why it matters

Single prompts save minutes; workflows save hours. This is the bridge from "I use ChatGPT" to "I build systems."

### Brief

1. Pick a research/writing pipeline from your FL-01 audit: "weekly industry brief," "source-grounded study notes," or "draft, critique, revise."
2. Design it as **3+ distinct steps** (gather, synthesize, draft, review, format); sketch the flow before building.
3. Build with no-code tools: a Claude Project with structured instructions, **NotebookLM** for source-grounded research, a custom GPT, or an **n8n** workflow. Mix tools if helpful.
4. Run the pipeline on **5 real inputs**. Time yourself against doing one manually.
5. Note where it breaks and what a human must still check.

### Deliverable

The working workflow + a walkthrough document: step diagram, every prompt/config used, the 5 runs, time-saved estimate, known failure points.

### Evaluation criteria

- Workflow runs end-to-end on a brand new input
- 3+ distinct steps with defined handoffs
- 5 real runs documented with outputs
- Honest time accounting including setup cost
- Failure points and required human review named

### Resources

- NotebookLM (free, source-grounded research)
- n8n quickstart (free self-hosting; paid cloud)
- Creating a GPT (OpenAI Help) — requires paid ChatGPT plan, treat as optional path

---

## Empty but Live: Ship a Blank Page

**Track:** General AI Fluency | **Workload:** ~2h | **Phase:** Build

### Brief

1. Create the empty project for your chosen stack: start the no-code project, or create a repo + connect a free host (GitHub Pages / Netlify / Cloudflare Pages / Vercel) so a near-blank page is reachable on a URL.
2. Confirm it's really live — open the URL **on your phone**, not just your laptop.
3. Drop your identity kit, case studies, and content map into your Claude Project.

### Deliverable

The live URL of the empty/near-blank project (even if it just says your name) + a screenshot.

### Pass/revise

- A real, reachable URL exists, opened on a second device
- Matches the chosen stack from "Three Roads"
- Claude Project has identity kit, case studies, content map loaded

---

## Three Roads: Choose Your Stack with AI

**Track:** General AI Fluency | **Workload:** ~2h | **Phase:** Build

### Brief

1. Give AI your 4 constraints: free only, your honest skill level, what your portfolio needs to do (paste sitemap + content map), how work must be displayed (image galleries, embedded demo, code repo, long-form reading). State whether anything needs to be dynamic yet.
2. Make it produce **3 stack options**, simplest to most powerful, each with: how to build, where to host (free), whether it needs a backend, the real trade-off.
3. Pressure-test the front-runner: what breaks if simplest? what do I maintain if most powerful? finish in 2 weeks? does it show my work right?
4. Decide, write a short rationale in your own words: chosen stack + the two you didn't + why (including "can I maintain this" and "does it show my work well").

### Deliverable

The written rationale (chosen stack + alternatives considered + why).

### Pass/revise

- 3 genuine options with trade-offs considered, not one answer obeyed
- Chosen stack is free, matched to real needs, displays your kind of work properly
- Rationale in your own words, includes "can I maintain this"
- Backend question answered honestly (most correctly choose "not yet")

---

# WEEK 5

## BE-05 — The Polite Scraper

**Track:** Backend AI Engineering | **Code:** BE-05 | **Workload:** ~6h | **Phase:** Build

### Goal

Build a small, polite scraper: download the first 3 catalogue pages of **Books to Scrape** (books.toscrape.com — a practice sandbox built exactly for this), visit all 60 book pages, turn messy HTML into clean checked JSON, survive a broken page without crashing, end every run with an honest report.

### Three professional habits this teaches

1. **Check before you collect** — classify the target before writing any code.
2. **Be a polite guest** — identify yourself, go slowly, never hammer a site.
3. **Trust nothing you scraped** — a web page is untrusted input; validate before storing.

### Tools

JS: built-in `fetch` + Cheerio + Zod. Python: Requests + Beautiful Soup + Pydantic. Target: `books.toscrape.com` ONLY.

### The seven stages

**Stage 0 — Check before you collect (~30min)**

- Create `scraper/` folder with README, `.gitignore`, entry file.
- Confirm Books to Scrape is an explicit practice sandbox (read their own page).
- Request `https://books.toscrape.com/robots.txt` once, note the result.
- README "Target classification" section: site, why, scope (first 3 pages only), what data, one sentence on appropriateness.
- Checkpoint: README states target, 3-page scope, robots result, and "I will not reuse this code on another site without checking its rules first."
- Commit: `Stage 0: classify scraping target`

**Stage 1 — Fetch once, cache once (~45min)**

- Honest user-agent naming you (e.g. `FlyRankInternship-A9/1.0 (+your-repo-link)`). Set a timeout. Check status code before parsing. Save HTML to `cache/catalogue-page-1.html` — read from cache during development, not re-fetching.
- Checkpoint: run twice — first prints FETCH + creates file, second prints CACHE HIT.
- Commit: `Stage 1: fetch and cache HTML`

**Stage 2 — Find all three pages (~45min)**

- Parse with Cheerio/BeautifulSoup. Collect every book link on page 1, convert relative→absolute URLs properly (`new URL()` / `urljoin()`, never string concat). Follow the "next" link through page 3, then stop (don't hardcode 60 links). Wait ≥500ms between real requests. Dedupe links.
- Checkpoint: `catalogue_pages=3, discovered=60, unique_urls=60` — same numbers on a rerun (mostly from cache).
- Commit: `Stage 2: discover three catalogue pages`

**Stage 3 — Extract the raw records (~1h15)**

- For every book page, collect: `title, product_url, price_text, availability_text, rating_text, description, source_page, fetched_at`.
- Same politeness (user-agent, timeout, status check, delay) on detail pages. Missing description → `null`, never invented text.
- Checkpoint: print one complete raw record (all 8 keys) + `detail_pages=60`.
- Commit: `Stage 3: extract book details`

**Stage 4 — Clean it, check it, store it (~1h)**

- Turn `price_text` ("£51.77") into `price_gbp` (51.77), keeping both. Use absolute `product_url` as canonical identity (dedupe).
- Write a Zod/Pydantic schema; validate every record. Failures → `errors.json` with reason, never into `books.json`.
- Write good records to `output/books.json`. Rerunning must give exactly 60, not 120 — idempotency.
- Checkpoint: `books.json` has exactly 60 records, every `price_gbp` a number, every URL `https://` — stays 60 after a second run.
- Commit: `Stage 4: validate normalized records`

**Stage 5 — One bad page must not kill the run (~45min)**

- Handle each page separately — one broken page logged and skipped. Retry on timeout/5xx only (NOT 404/403). End every run writing `output/run-report.json`: start time, duration, pages fetched, cache hits, valid/invalid records, failed pages.
- Prove it: add one made-up book URL on purpose and run.
- Checkpoint: with one fake URL, run still finishes, `books.json` still has 60 good records, `run-report.json` shows `failed_pages: 1`.
- Commit: `Stage 5: survive failures, report the run`

**Stage 6 — Publish the evidence (~45min, required)**

- Push to public GitHub repo (add `cache/` to `.gitignore` — don't commit hundreds of cached HTML files).
- README: target classification, one run command, lane + install, record schema, politeness rules, one honest limitation.
- Paste one real `run-report.json` into README, one sentence on why no browser was needed here.
- Short ethics note in your own words.
- Checkpoint: stranger can clone, run one command, get `books.json` + `run-report.json` in under 5 minutes.
- Commit: `Stage 6: publish scraper evidence`

### Optional extras

CSV export, change-detection via hashing, tiny local dashboard, selector fixtures, upgrading retry to real exponential backoff + Retry-After header handling (this is what next assignment, A16, covers properly — good head start).

### Bonus — AI rematch (~1h, optional)

Same pattern as other assignments: write your own prompt from memory, generate in `ai-version/`, compare, write "AI vs me" section.

### Requirements checklist

- [ ] One command processes exactly first 3 catalogue pages, discovers 60 unique URLs
- [ ] Every detail page produces 8 raw fields + numeric `price_gbp`
- [ ] Records schema-validated; failures → `errors.json` with reason
- [ ] `output/books.json` holds exactly 60 unique records, after first run AND rerun
- [ ] Every real request: user-agent, timeout, ≥500ms delay, status check; dev reads cache
- [ ] README documents target classification + robots check result
- [ ] One deliberately broken URL logged and skipped; run finishes
- [ ] `output/run-report.json` reports counts, failures, cache hits, duration
- [ ] Public GitHub repo, 7+ commits, README runnable in <5min

### Stretch (optional)

- Browser cost comparison: fetch a JS-rendered page with plain HTTP vs Playwright, compare time/memory
- 5+ unit tests (price normalization, URL conversion, missing description, duplicates, malformed fixture)
- Background execution via BE-06 pattern if you've done it (queued job, concurrency cap, idempotent writes)
- Local AI enrichment via Ollama: add category + summary from validated descriptions, schema-forced

### Note

Next week's A16 (not in your current assignment list, may appear later) builds the production version of this: full retry/backoff rules, structured logs, finding hidden data layers. Don't gold-plate Stage 5 — keep it simple here.

---

## FL-06 — Design Your Personal Agent

**Track:** General AI Fluency | **Code:** FL-06 | **Workload:** ~4h | **Phase:** Build (core)

### Why it matters

The capstone is a working personal AI agent, and agents fail at the DESIGN stage more often than the build stage. A tight spec is the difference between a 10-hour build and a 30-hour swamp.

### Brief

1. Choose the job your agent will do: inbox triager, research scout, study coach grounded in your notes, weekly review assistant. Scope to ONE job done well, roughly 10 build hours.
2. Write the **spec** (1–2 pages): job to be done; the user (you) and usage frequency; tools/data needed with access plan; draft instructions; **5 eval cases**; risks and guardrails (what the agent must confirm, what it must never do).
3. Choose your build platform and justify it: Claude Project with connectors/skills, Claude Cowork (paid), custom GPT (paid), n8n agent workflow, or scripted agent. **Pick a free path you can actually run.**
4. Post the spec in the submission section.

### Deliverable

The agent design doc, done your way.

### Evaluation criteria

- Scope achievable in ~10 build hours
- Every tool/data source has a realistic access plan
- 5+ eval cases defined BEFORE building
- Guardrails specified for risky/irreversible actions
- Platform choice justified against ≥1 alternative

### Resources

- "A Practical Guide to Building Agents" (OpenAI, PDF)
- "Writing effective tools for agents" (Anthropic Engineering)
- "Your AI Product Needs Evals" (resource library)

### Note from Q&A

A "FlyRank Hackathon Brief" attachment that sometimes appears on this card is unrelated — ignore it.

---

## PF-04 — Personal Website Live on the FlyRank Domain

**Track:** General AI Fluency | **Code:** PF-04 | **Workload:** ~6h | **Phase:** Build (core)

### Why it matters

A personal website is the one profile no platform can take away. You build it now on a free host with a public URL you can send anyone today.

### Brief

1. Plan a simple site: who you are, what you're building, links to LinkedIn/GitHub/CV/booking link, space for future posts and capstone work. One page is enough to start.
2. Build on a free hosting path. **Netlify recommended** (free tier covers everything, HTTPS automatic). GitHub Pages, Cloudflare Pages, Vercel hobby tier also accepted. Hand-written HTML, static site generator, or AI-assisted build all fine — you must understand every file you deploy.
3. Get it live over HTTPS, then **rename the site** to something CV-worthy: `yourname.netlify.app`, not a random string (Netlify: Site configuration → Change site name).
4. Write your **DNS walkthrough**: what DNS does, what a CNAME record is, what happens between someone typing an address and the host answering — resolver, nameserver, record, response. Explain so a non-technical person could follow it. (No need to actually buy a custom domain for this one.)
5. Link the site from your LinkedIn profile and CV.

### Deliverable

Your live HTTPS URL + your DNS walkthrough (half a page to a page, your own words).

### Evaluation criteria

- Site live/loading over HTTPS on a clean public URL, tested in a private window
- Contains your positioning + working links (LinkedIn, GitHub, CV, booking link)
- DNS walkthrough technically correct, your own words
- You can explain every file in the deployed site
- Site linked from LinkedIn and CV
- (At capstone time: FlyRank completion badge added to the site)

### Resources

- Deploy on Netlify (FlyRank intern guide) — start here
- Netlify Drop — drag a folder, get a live URL instantly
- What is DNS? / What is a CNAME record? (Cloudflare Learning) — read before writing the walkthrough

---

## Explain It Like You Built It

**Track:** General AI Fluency | **Workload:** (unspecified) | **Phase:** Build+

### Brief

1. Pick one part of your build you found interesting or didn't fully understand (page structure, styling, how deploying pushes it live, nav links).
2. Have AI **tutor you on it** until you genuinely get it, then write a short plain-words explanation, as if teaching a friend who's never built a site.

### Deliverable

The short plain-words explanation of one real piece of your build.

### Pass/revise

- It's a real piece of YOUR build, not a generic tutorial topic
- Explanation in your own words and actually correct
- Demonstrates learning, not pasted output

---

## FL-07 — Build the Agent

**Track:** General AI Fluency | **Code:** FL-07 | **Workload:** ~10h | **Phase:** Build (core)

### Why it matters

This is Checkpoint 1, the MVP. An agent that completes its core job end-to-end with at least one live tool connection is the artifact everything else orbits.

### Brief

1. Build on the platform you chose in FL-06. Start with the NARROWEST version of the core job, get ONE full end-to-end run working before adding anything.
2. Connect **at least one real tool or data source**: an MCP server/connector, your files, a knowledge base, or an external service.
3. Keep a **build log**: what broke, what you changed, what you cut from the spec and why. Deviating from the spec is normal; document it.
4. When the core job works, record **one raw, unedited screen capture (~2 min)** of a successful end-to-end run.

### Deliverable

The working agent + build log + raw run capture.

### Evaluation criteria

- Agent completes core job end-to-end without mid-run hand-editing
- At least one live tool/file/data connection in use
- Matches FL-06 spec, or deviations documented with reasons
- Build log shows real iteration, not a clean retroactive story
- Run capture unedited, full loop from request to result

### Resources

- Introduction to Claude Cowork (Anthropic Academy)
- Connect to local MCP servers (MCP Docs) — Claude Desktop filesystem access, copy-paste setup
- Anthropic Courses catalog

### Clarifications from Q&A

- Google AI Studio is fine to use.
- Large video uploads (>80MB) failing → upload to Google Drive and submit the link instead.

---

# WEEK 6

## BE-07 — Put an LLM Behind Your API

**Track:** Backend AI Engineering | **Code:** BE-07 | **Workload:** ~6h | **Phase:** Build+

> ⚠️ **PAYMENT NOTE:** Anthropic's Claude API has NO free tier. Use **OpenRouter** (`openrouter/free` model — 20 req/min, 50/day, no card) or **Ollama** (fully local, unlimited, no card) instead. Both explicitly approved by FlyRank.

### Goal

Add ONE new endpoint to your growing API. It takes something messy, asks a model, returns clean validated JSON — with a real timeout, sensible retries, a cost log, and a kill switch. **This is not a chatbot assignment** — one request in, one structured answer out.

### The core mental model

An LLM call = an HTTP request to someone else's server, with 4 special properties: it's slow (needs its OWN timeout — SDK defaults wait 10 minutes), non-deterministic (validate shape, not exact text), costs money/quota (count every call), and will confidently return something wrong (treat it as untrusted input, same as last week's scraped data).

The whole endpoint in 6 lines: validate input → build prompt (versioned file) → call model (timeout + selective retries) → parse+validate output against schema → repair once if it failed → return clean JSON or a clear 422.

### Step one — pick your job

Your endpoint must pass 3 tests:

1. **Closed output** — same field names every time; any category field comes from a short predefined list
2. **One decision** — one request in, one answer out, no conversation memory
3. **A human could grade it** — you can look at an input and say right/wrong

**Ideas:** enrich your BE-05 scraped records (category + summary + quality_flags), triage support messages (category/urgency/team), tidy messy job titles into a canonical list, extract fields from a receipt/CV, check text against house rules (allow/flag/block), turn commits into changelog entries, score a README against a rubric.

**Where NOT to use a model:** arithmetic/totals, exact lookups, anything with one computable right answer, anything where being quietly wrong 5% of the time is unacceptable (payments, permissions, deletions).

**Write `JOB-CARD.md` first** (5 lines): what it does, input shape, output shape (closed lists spelled out), what it must never do, what to do when unsure.

### Tools

Any language works. JS: Express + `openai` npm package (yes, even for non-OpenAI providers — it's the shape everyone copies) + Zod. Python: FastAPI + `openai` pip package + Pydantic.

**Provider — pick one, both $0:**
| | OpenRouter (hosted) | Ollama (local) |
|---|---|---|
| Setup | Sign up, flip 2 privacy settings, copy key (~5min) | Download, pull a model (~15min) |
| Budget | 20 req/min, 50/day | Unlimited |
| Base URL | `https://openrouter.ai/api/v1` | `http://localhost:11434/v1/` |
| Model | `openrouter/free` | `gemma3:1b` (815MB) or `llama3.2:3b` (2GB) |

**⚠️ OpenRouter gotcha:** free models return 404 until you go to Settings → Privacy and turn ON both "Free endpoints that may train on request data" AND "Free endpoints that may publish prompts." Do this BEFORE writing any code. Because of this, never send real personal/confidential data through the free endpoint — use made-up test data.

### The six stages

**Stage 0 — Pick the job, make a model answer you (~45min)**

- Write `JOB-CARD.md`. Pick provider lane, get a key/model running. Key in `.env`, gitignored, `.env.example` committed. Write a throwaway `hello.js`/`hello.py` that asks the model to reply with exactly "ready."
- Checkpoint: script prints something containing "ready"; `.env` not in git status.
- Commit: `Stage 0: job card, provider working, key in .env`

**Stage 1 — Build the endpoint before the AI (~45min)**

- Add the route, NO model call yet. Validate input with Zod/Pydantic first — wrong type/missing field/too long → 400 naming the field.
- Define the output schema in code (`src/llm/schema.js`). Closed lists become enums.
- Add a **stub mode**: `LLM_STUB=1` env var → endpoint skips the model, returns a hardcoded schema-valid object. (This saves your daily quota during dev.)
- Checkpoint: with `LLM_STUB=1`, valid curl → 200 + schema JSON; bad field → 400 naming it. Zero model calls made.
- Commit: `Stage 1: endpoint, input validation, output schema, stub mode`

**Stage 2 — The prompt is a specification (~1h15)**

- Create `prompts/<job>-v1.md` — **prompt lives in a versioned file, not a string in your route.**
- System prompt, 5 parts in order: role/job (1 sentence) → exact output shape with closed lists → rules (never invent category, never add fields, never return non-JSON) → what to do when unsure (the single highest-value line — e.g. "use category 'other' with low confidence, don't guess") → 2–3 examples (typical, ambiguous, hostile/empty).
- User's data goes in a separate **user message**, never glued into the system prompt (defends against prompt injection too).
- Wire it up, temperature low (0–0.2). Run on 3 real inputs, read answers with your own eyes.
- Checkpoint: with `LLM_STUB` unset, real model answers for 3 different inputs; prompt file committed.
- Commit: `Stage 2: prompt v1 as a versioned file, wired to the endpoint`

**Stage 3 — Make the output trustworthy (~1h30)**

- Parse model output (strip code fences, find JSON object).
- Validate against your schema (`safeParse`/`model_validate_json`).
- **Repair once, only once:** if parse/validation failed, one more call with the broken output + exact validation error + "return only corrected JSON."
- Give up cleanly: if repair also fails, `422` + log raw output to `logs/quarantine.jsonl`. Never crash, never fake a default.
- Never return raw model text to the caller — success or failure.
- Checkpoint: happy path → schema JSON. Temporarily break your prompt to demand a bad category → 422 + new quarantine log line. Undo.
- Commit: `Stage 3: parse, validate, repair once, quarantine on failure`

**Stage 4 — Production-ready (~1h15)**

- **Real timeout**: `timeout: 30000` (JS) / `timeout=30.0` (Python) on the client — SDK default of 10 minutes is not acceptable. 504 on timeout.
- **Selective retries**: YES on timeout/429/5xx, NEVER on 400/401/403 (wastes quota, won't succeed anyway). Exponential backoff + jitter. Obey `Retry-After` if present.
- **Cost logging**: one structured log line per call — prompt version, model, input/output tokens, duration, repair flag.
- **Kill switch**: `LLM_ENABLED=false` → skip model entirely, return safe deterministic fallback or clean 503.
- Checkpoint: `LLM_ENABLED=false` → instant fallback, zero calls in logs. Then a wrong API key → fails fast, no retries (401 never retried). Restore real key.
- Commit: `Stage 4: timeout, retry policy, cost logging, kill switch`

**Stage 5 — Prove it, publish it (~1h, required)**

- Build `evals/cases.json`: **8 inputs you write yourself**, each with the answer you believe is correct. Include ≥1 ambiguous case and ≥1 that should hit your "when unsure" rule.
- Script that runs all 8, prints match percentage + failures. Record the number in README HONESTLY (6/8 reported as 6/8, not hidden).
- README, in order: what the endpoint does (plain paragraph); one copy-paste curl + its exact response; job card including "must never" list; provider/model used + the 3 env vars to swap; eval result with date + prompt version; cost log for one call + 10,000/day estimate; one honest "what I'd fix with another day" line.
- Double-check `.env` isn't in the repo.
- Checkpoint: stranger clones, adds their own key, runs one command, gets a valid response in <5min. README shows a real eval score.
- Commit: `Stage 5: eval set, results, README, published`

### Optional extras

Caching repeated requests (hash input+prompt version), swap providers in one line, race two models and compare, prompt v2 + eval delta, try to break your own endpoint with injection attempts (most interesting one to write up), handle refusals gracefully, try `response_format` schema-constrained output, streaming.

### Bonus — AI rematch

Same pattern: write your own spec-prompt from memory, generate in `ai-version/`, run your checkpoints against it, diff, "AI vs me" README section. Watch for: 10-minute default timeout left in place, raw model text returned, retrying on 401.

### Requirements checklist

- [ ] `JOB-CARD.md` exists with full spec
- [ ] Job passes all 3 rules (closed output, one decision, human-gradeable)
- [ ] POST endpoint added; invalid input → 400 naming the field, before any model call
- [ ] Output schema defined in code with enums
- [ ] `LLM_STUB=1` returns schema-valid response with zero model calls
- [ ] Prompt is a versioned file, not inline string
- [ ] Prompt has role, output shape, rules, when-unsure instruction, 2+ examples
- [ ] User content sent as user message, never in system prompt
- [ ] Output parsed+validated before returning
- [ ] One repair retry on failure, then 422 + quarantine log; never crashes
- [ ] Raw model text never returned to caller
- [ ] Explicit timeout ≤60s set (SDK default NOT left in place)
- [ ] Retries only on timeout/429/5xx, never 400/401/403, with backoff+jitter
- [ ] Every call logs: prompt version, model, tokens, duration, repair count
- [ ] `LLM_ENABLED=false` disables model, returns deterministic fallback
- [ ] `evals/cases.json` has 8 labelled cases; README states score+date+prompt version
- [ ] `.env` gitignored, `.env.example` committed, no key anywhere in repo history
- [ ] Public repo, README with runnable curl + real output, 6+ commits

### Stretch (optional)

Grow eval to 25 cases (easy/hard split), provider behind an interface (single `complete()` function, 2 implementations), proper OWASP prompt-injection defenses + 5 attack eval cases, count tokens before sending + reject over a limit + report cost per 1000 requests.

### Clarifications from Q&A

- Local models (Qwen/Mistral via LM Studio/Ollama) explicitly fine if no API credits available.
- Groq via the OpenAI SDK also fine.

---

## Make It Do Something

**Track:** General AI Fluency | **Workload:** ~4h | **Phase:** Submit

### Brief

1. Choose the ONE dynamic feature your portfolio actually needs — most often a working contact form or email capture; for some, a live demo of your own work or a small AI feature. **One, not several.**
2. Wire it end to end on a free tier, with AI as your build partner. It has to genuinely work — a real submission reaches you, or the demo really runs.
3. Write a short plain-words explainer: what a backend is, what your feature does, how the data flows.

### Deliverable

The live feature working (evidence: a real test submission that reached you / the working demo) + the plain-words explainer.

### Pass/revise

- Exactly one feature, working live end to end, not several half-wired
- On a free tier, genuinely functions on a real test
- Explainer correct, your own words, shows understanding of data flow

---

## Open It on Your Phone

**Track:** General AI Fluency | **Workload:** ~4h | **Phase:** Build+

### Brief

1. **Mobile first:** open your portfolio on a real phone, fix everything broken (text size, images spilling/blurry, untappable buttons, broken layout). Then check tablet and desktop.
2. **Readability:** comfortable text size/line spacing, check color contrast, confirm work captures are crisp.
3. **Kill obvious breaks:** click every link (demo, repo included), compress oversized images, use AI to audit a section ("what's broken on mobile, accessibility problem, why is this slow").
4. Keep a short **fix log**: what was broken, what you changed.

### Deliverable

Updated live URL + the fix log (before/after notes, ideally phone screenshots).

### Pass/revise

- Genuinely works on mobile, checked on a real phone
- Text readable, contrast passes, work images crisp
- All links work, no oversized images, nothing obviously broken on any width
- Fix log shows real problems found and fixed

---

## Survive the Crit

**Track:** General AI Fluency | **Workload:** (unspecified) | **Phase:** Build+

### Brief

1. Submit your live portfolio for design review (fellow student or friend). Provide your proof statement so they can judge it against its actual job.
2. Ask the reviewer two questions first: in 10 seconds, what do I do? would you believe I'm good at it? Then collect the rest WITHOUT defending. Sort: must-fix (confusing, broken, hurts the one action, proof doesn't land) vs nice-to-have (later).
3. Fix the must-fixes and reply with what you changed.

### Deliverable

The reviewer's feedback + your must-fix/nice-to-have sort + evidence of must-fixes addressed on the live site. **This checkpoint must pass to proceed to Week 7.**

### Pass/revise

- Portfolio submitted with proof statement, real feedback received
- Reviewer could state what you do and felt backed up, or gaps now fixed
- Feedback sorted honestly
- Must-fixes actually fixed on the live site, not just acknowledged
- You engaged with feedback rather than defending the original

---

# WEEK 7

> ⚠️ **Note on internal labeling:** BE-06 and BE-08's own PDF documents are internally titled "Week 4" (A7 and A8 respectively), but the FlyRank portal places them at **Week 7**. Follow the portal's week placement for your folder structure — the internal PDF week numbers are just leftover from how the content was originally authored. Doesn't affect anything about how you build them.

## BE-06 — Your First Background Job

**Track:** Backend AI Engineering | **Code:** BE-06 | **Workload:** ~5–6h (+2h stretch, +1h bonus)

### Goal

Build an API with one slow task (a report that takes 8 seconds). The API answers instantly; the slow work happens in a background job. A status endpoint reports when it's ready. Also build ONE cron job (runs on a clock, no request at all). This assignment stands alone — doesn't need earlier code, though you can build on your CRUD API if you want.

### The big idea

| How work starts                  | Example                                 | Name                                 |
| -------------------------------- | --------------------------------------- | ------------------------------------ |
| Client asks and waits            | `GET /health`                           | Request/response (everything so far) |
| Client asks, work happens later  | "Make my report" → 202 now, ready in 8s | Background job, started by an event  |
| Nobody asks, the clock starts it | "Every day at 08:00, send summary"      | Cron job, started by a schedule      |

**Cron expression** = 5 fields: minute, hour, day-of-month, month, day-of-week. `* * * * *` = every minute. `0 8 * * *` = every day at 08:00. Use **crontab.guru** to decode any expression in plain words.

### Tools

Inngest (free, runs on your machine, no account needed, used by FlyRank in production) + Express or FastAPI. Install: `npm install inngest` / `pip install inngest`.

### The stages (6 + bonus)

**Stage 0 — Hello, server (~30min)**

- `GET /health` → `{ "status": "ok" }` (reuse your CRUD API's first stage if you have it).
- Commit: `Stage 0: hello server`

**Stage 1 — Hire the worker: connect Inngest (~1h)**

- Install Inngest. Create the Inngest client (`id: report-api`). Create one function `say-hello`, triggered by event `test/hello` — sleep 5s (`step.sleep`), return "Hello from the background!". Serve at `/api/inngest`.
- Start Dev Server: `npx inngest-cli@latest dev -u http://localhost:3000/api/inngest`. Open dashboard at `http://localhost:8288`, press Invoke.
- Checkpoint: dashboard shows `say-hello` run with 5s sleep step, ending Completed.
- Commit: `Stage 1: Inngest connected, first function runs`

**Stage 2 — The fast door: accept now, work later (~1h30)**

- In-memory reports dictionary. `POST /reports` with `{ "topic": "cats" }`: makes id, saves `{ id, topic, status: "pending" }`, sends event `report/requested`, returns **202 immediately** with `{ id, status: "pending" }`. Endpoint does no slow work.
- Second Inngest function `make-report`, triggered by `report/requested`: `step.sleep("do-the-slow-work", "8s")` then `step.run("build-report", ...)` saves `status: "done"`.
- `GET /reports/:id` → the object (pending → done). Unknown id → 404. (This polling pattern is called "eventual consistency.")
- Checkpoint: POST returns 202 in well under 1 second; GET says pending, then ~10s later says done.
- Commit: `Stage 2: 202 + background job + status endpoint`

**Stage 3 — Jobs fail. Watch the retry. (~45min)**

- In `make-report`, if topic is `"fail"`, throw an error in the `build-report` step. Set `retries: 2`.
- `POST /reports` with topic "fail" → watch dashboard: attempt 1 fails → wait → attempt 2 → attempt 3 → ends Failed (growing waits = "backoff").
- Add validation: missing topic → 400, no event sent (a wrong INPUT is rejected at the door; only a wrong MOMENT deserves a retry — write one README sentence on this distinction).
- Checkpoint: dashboard shows 3 attempts, final Failed. POST with no topic → 400, no job created.
- Commit: `Stage 3: retries seen, bad input rejected`

**Stage 4 — The clock knocks: your first cron job (~45min)**

- Third function `heartbeat`, cron trigger `* * * * *` (every minute, for testing only). Logs: how many reports pending/done/failed. No endpoint, no event — the clock alone triggers it.
- Watch dashboard for 2 minutes. README: one sentence each on the cron expression for "every day at 08:00" and "every Sunday at 22:00" (build on crontab.guru).
- Checkpoint: dashboard shows 2 heartbeat runs, 1 minute apart.
- Commit: `Stage 4: cron heartbeat`

**Stage 5 — Publish to GitHub (required)**

- Public repo. README: what this is, how to run (two commands — API + Dev Server), endpoint/function table, pasted 202+poll proof, Stage 3 & 4 sentences, dashboard screenshot.
- Commit: `Stage 5: publish and docs`

### Optional extras

List endpoint `GET /reports`, "email" stand-in (write to `outbox/<id>.txt`), cleanup cron (delete old done reports), design your own cron schedule, the restart experiment (stop API mid-sleep, restart, watch the job survive — this is "durability").

### Stage 6 — Bonus: AI rematch (~1h)

Write your own prompt from memory specifying the full system. Generate in `ai-version/`. Run Stage 2/3 checkpoints against it. "AI vs me" README section.

### Requirements checklist

- [ ] API + Inngest Dev Server each start with one command
- [ ] `POST /reports` → 202 + id in <1s; 8s work happens in background, not in endpoint
- [ ] `GET /reports/:id` → pending then done+result; unknown id → 404; missing topic → 400
- [ ] `make-report` uses ≥2 steps (sleep + run), visible in dashboard
- [ ] Topic "fail" → 3 attempts, ends Failed in dashboard
- [ ] Cron function runs every minute, logs a summary line
- [ ] Public repo, ≥6 commits, README with run commands + endpoint table + 202-poll proof + Stage 3&4 sentences + dashboard screenshot

### Stretch (optional)

Idempotency (send same `report/requested` event twice with same id → built only once), concurrency limit (max 2 at once, enqueue 5, watch 3 wait), durable restart proof with a 3-step function + dashboard screenshot showing finished steps didn't re-run, AI rematch above.

---

## BE-08 — PDF Report Generator

**Track:** Backend AI Engineering | **Code:** BE-08 | **Workload:** ~4–5h (+2h stretch, +1h bonus)

### Goal

Query your data with SQL, render into a real PDF, let your API generate and hand out the file by link. **No background jobs required** — the whole pipeline runs inside a plain endpoint (you'll feel why that's eventually a problem — that's exactly what BE-06 solves, and a stretch goal shows where it slots in if you did BE-06).

### The pipeline (4 moves)

Query (SQL → 5 numbers) → Render (HTML template + numbers → PDF) → Store (save file to disk, path in DB) → Serve (client downloads by link). **Rule: store and link, don't pass bytes around.**

### Tools

SQLite (built into Node 22+/Python) + **Playwright** (drives a real headless browser, `page.pdf()` prints HTML to PDF).

### The seven stages

**Stage 0 — The setup (~30min)**

- `GET /health` endpoint. Install Playwright + Chromium (`npx playwright install chromium` / `playwright install chromium`).
- Commit: `Stage 0: setup ready`

**Stage 1 — Data worth reporting on (~45min)**

- Pick **Option A (shop)**: SQLite `report.db`, table `orders` (id, customer, product, amount, created_at). Seed script inserts ~200 random orders.
- OR **Option B (bookstore)**, if you did BE-05: reuse your scraped `books.json` → table `books` (id, title, price, rating, url).
- Seed script must be idempotent: delete-all-then-insert, so running twice ≠ double rows.
- Checkpoint: `SELECT COUNT(*)` → 200 orders (or 60 books), even after seeding twice.
- Commit: `Stage 1: seeded report.db`

**Stage 2 — Boring SQL is 80% of reporting (~1h)**

- Write aggregation queries (COUNT, SUM, AVG, GROUP BY). Shop: total orders, total revenue, top 5 products by revenue, orders per day (last 7 days). Bookstore: total books, avg price, top 5 most expensive, count per star rating.
- One function `getReportData()` returning all 4 as one object. Print as JSON, sanity-check the numbers.
- Checkpoint: test script prints full report object — 4 sections, real numbers.
- Commit: `Stage 2: aggregation queries`

**Stage 3 — Render: from numbers to PDF (~1h30)**

- Build an HTML page (template string) from the report object: title+date, two totals, top-5 table, a long table (all orders/books). Render with Playwright (`setContent` + `page.pdf({ path, format: "A4", printBackground: true })`).
- **The classic trap:** a long table crosses a page break, a row gets sliced. Fix with `tr { break-inside: avoid; }` and put the header row in `<thead>` so it repeats per page.
- Checkpoint: PDF opens, ≥2 pages, no row cut in half, header repeats on both pages.
- Commit: `Stage 3: HTML to PDF with clean page breaks`

**Stage 4 — Serve it from your API (~45min)**

- `reports` table: id, path, created_at. `POST /reports` runs the WHOLE pipeline inside the endpoint (query→render→insert row), returns `201` + `{ id, file: "/reports/<id>/file" }` (yes, this takes a few seconds — allowed here).
- `GET /reports/:id` → the row + file link. Unknown id → 404.
- `GET /reports/:id/file` → serves the PDF from disk (only THIS endpoint moves megabytes — "store and link" in practice).
- Write one README sentence: at what point would you move this work out of the request (into BE-06's background-job pattern)?
- Checkpoint: POST shows a visible pause then 201+link; downloaded file opens as a real PDF.
- Commit: `Stage 4: generate and serve by link`

**Stage 5 — Ask twice, get one (~45min)**

- `POST /reports` checks: if a report was already generated TODAY, return the existing id+link with `200` (not 201) instead of regenerating. Accept `{ force: true }` to force a fresh one.
- Write 2 README sentences: what this protects against, and a real-world example where a missing check costs money.
- Checkpoint: two rapid POSTs → same id both times, one new file. With `force: true` → new id.
- Commit: `Stage 5: duplicate requests make one report`

**Stage 6 — Publish to GitHub (~45min, required)**

- Add `reports/` and `report.db` to `.gitignore`.
- README: what this is, which dataset, how to run (seed + API commands), pasted SQL, POST→download proof, Stage 4&5 sentences, screenshot of page 1 of a PDF.
- Commit: `Stage 6: publish and docs`

### Optional extras

Make it pretty (logo, brand colors, footer with page numbers), parameterized report (`{ days: 7 }`), control panel (`GET /reports` lists all), nice filenames, big-table experiment (5000 rows, time it, write 2 sentences).

### Bonus — Stage 7: AI rematch (~1h)

Same pattern as always: own prompt from memory, `ai-version/` folder, run checkpoints, "AI vs me" section.

### Requirements checklist

- [ ] `report.db` exists, seed fills it (even run twice)
- [ ] Aggregation queries feed the report — pasted in README
- [ ] PDF renders from real data, ≥2 pages, no row cut by page break
- [ ] `POST /reports` → 201 + id + file link; `GET /reports/:id` → record; unknown id → 404
- [ ] File stored on disk, served by link — JSON never carries file bytes
- [ ] Duplicate requests same day → one file, same id
- [ ] Public repo, ≥7 commits, README with run commands + SQL + download proof + Stage 4&5 sentences + PDF screenshot; `reports/` and `report.db` gitignored

### Stretch (optional)

- **Bring in BE-06:** move generation into a background job (202+id instant, Inngest function does query→render→save as steps, status endpoint reports pending/done). One README line on trade-offs.
- Cron it (every Monday 08:00, no request at all) via Inngest scheduled function or node-cron/APScheduler.
- Email it via Mailpit (local mailcatcher) — "send" an email containing the report LINK, not the file attached. One line why links beat attachments.
- AI rematch above.

---

## BE-09 — Build an AI Decision Flow with React Flow + Inngest

**Track:** Backend AI Engineering | **Code:** BE-09 | **Workload:** ~2h listed (likely longer in practice given 4 phases)

### Goal

Build a visual AI workflow system: each node is an AI decision step that returns **YES** or **NO**, routing execution down different edges. Inngest runs the workflow; React Flow visualizes it.

### Phase 1 — Setup (~1h)

- React or Next.js app. Install + configure: React Flow, Inngest, OpenAI SDK, Shadcn. Env vars. Basic project structure.
- Deliverables: running frontend, working Inngest dev server, repo initialized with README.

### Phase 2 — Foundations (~2h)

- Render a React Flow canvas: adding nodes, connecting nodes, editing node prompts, define edge types (**YES path**, **NO path**), store graph state locally.
- Deliverables: interactive flow editor, editable prompt nodes, functional node connections.

### Phase 3 — Build core (~2h)

- Each node maps to an Inngest step. Send node prompt to an LLM — model must return ONLY "YES" or "NO." Continue execution based on selected edge. Track execution order.
- Example: "Is this a support request?" → YES → Support Node / NO → Sales Node.
- Deliverables: end-to-end workflow execution, dynamic node traversal, AI-powered branching logic.

### Phase 4 — Build polish (~2h)

Choose at least 3: visual execution state, execution logs panel, save/load workflows, JSON export/import, better node styling, error handling, retry failed nodes, animated active edges, execution history.
Deliverables: improved UI/UX, more reliable execution flow.

### Clarifications from Q&A

- Backend can be Python/FastAPI instead of Node/Next.js (React Flow stays frontend-side either way).
- Groq via OpenAI SDK is fine instead of a real OpenAI key.

---

## Break Your Own Site

**Track:** General AI Fluency | **Workload:** ~2h | **Phase:** Submit

### Brief

1. **Try to break it.** Submit forms empty and with garbage, open in an untested browser/device, click everything (demo + repo links too), submit twice fast. Note what breaks.
2. **Findability & speed.** Add basic SEO/meta (page title, description, social-share preview), search your own name/site, run a free speed check.
3. **Triage:** sort every finding into fix-now vs known-limitation. Fix the fix-nows.
4. Submit for hardening review (mentor or structured peer). Show the "where it breaks" list + fixes.

### Deliverable

The honest "where it breaks" list (fixed vs known-limitation) + evidence of fix-nows addressed + basic SEO/meta added. **This checkpoint must pass to proceed to launch.**

### Pass/revise

- You genuinely tried to break your own site — real edge cases, not just happy path
- SEO/meta added, portfolio findable, speed checked
- Findings triaged honestly; fix-nows actually fixed; known limitations named, not hidden
- Hardening review happened, its must-fixes addressed

---

## Plant Your Flag: Domain + Badge

**Track:** General AI Fluency | **Workload:** ~20h | **Phase:** Build+

> ⚠️ **PAYMENT NOTE:** A real custom domain costs money (~$10–15/year). A **free subdomain is an explicitly accepted fallback** if budget is truly zero — no penalty either way per FlyRank Q&A.

### Brief

1. Point a custom domain at your site (or use a clean free subdomain fallback).
2. Add free analytics; confirm the site is fully live over HTTPS on the new address.
3. **Launch hygiene:** confirm social-share preview, favicon, page titles. Open the final address on your phone once more.
4. Install the **FlyRank graduate badge** in your footer, linking to your verification page. (Badge available at: internship-badge.netlify.app — though per Q&A, the actual badge asset/instructions are only provided once your capstone is approved, around early September in FlyRank's timeline; you can submit this assignment with the badge section pending until then.)

### Deliverable

Live custom-domain URL + screenshot of analytics installed + confirmation share preview/favicon/titles correct + badge visible in footer.

### Pass/revise

- Site live on custom domain (or clean fallback subdomain), over HTTPS
- Analytics installed and working
- Share preview, favicon, titles correct on the real address
- Graduate badge installed in footer, links to verification page

### Clarification from Q&A

- Any free subdomain from any hosting platform (not just Netlify) qualifies as the fallback — no strict requirement on which one.

---

# WEEK 8

## The Plan to Keep Building

**Track:** General AI Fluency | **Workload:** ~1h | **Phase:** Submit

### Why it matters

A portfolio that never gets a second project goes stale. This sets up the habit while you still remember how everything works.

### Brief

1. Write down, in a few lines, exactly where your next case study will go and the steps to add one (reuse the 3-beat shape: problem, what you did, what came of it).
2. Name the next real piece of work you intend to add, set a concrete reminder (calendar nudge, recurring note).
3. Keep your Claude Project — it already knows your voice, stack, identity kit, so the next case is a short conversation, not a rebuild.

### Deliverable

Short "how to add the next case" note + the named next piece + evidence of the reminder set.

### Pass/revise

- Concrete "how to add" note, not a vague intention
- Specific next piece named with a real reminder set
- Build context (Claude Project) preserved

---

## FL-09 — Documentation and Demo Video (a.k.a. "Show It / Tell the Story" part 1)

**Track:** General AI Fluency | **Code:** FL-09 | **Workload:** ~5h | **Phase:** Submit

> **Note:** This appears twice in the portal under slightly different titles ("Show It / Tell the Story" and standalone "Documentation and Demo Video") — they're the same assignment (FL-09), just do it once.

### Why it matters

An undocumented agent is a private hobby; a documented one is portfolio evidence.

### Brief

1. Write a **README**: what the agent does and for whom, setup steps a stranger could follow, usage examples, a simple architecture sketch, your v2 eval results, limitations list.
2. Record a **3–5 minute demo video**: a live end-to-end run with voice narration explaining what's happening and why. **No slide decks** — show the real thing, including one guardrail/limitation explained on camera.
3. Record with OBS Studio, Loom free tier, or any screen recorder; upload as unlisted YouTube link.
4. Post both in submissions.

### Deliverable

The README + demo video link.

### Evaluation criteria

- Stranger could reproduce setup from README alone
- Eval results and limitations included, not hidden
- Video shows a live end-to-end run, not slides, 3–5 min, clear narration
- One design decision and one limitation explained on camera
- **Honest about where AI did the work** — a line in the README naming what you built with AI and how (framed as "transparency diligence," reads as credibility not weakness)

### Resources

- Make a README — standard template
- Technical Writing One (Google, free self-paced)
- OBS Studio (free, open-source screen recording)

---

## FL-10 — Final Package, Retrospective, and Capstone (final checkpoint)

**Track:** General AI Fluency | **Code:** FL-10 | **Workload:** (part of "Show It / Tell the Story")

### Why it matters

This is the second required checkpoint — the documented human sign-off the certificate depends on.

### Brief

1. Assemble everything in one place (GitHub repo or shared folder) with an **index** linking every deliverable from the whole track.
2. Write a **500–800 word retrospective** — written for the person you were in Week 1: what you set out to do, what changed, what you'd build next, the 3 most transferable things you learned.
3. Complete your **hours log** in the portal.
4. Publish your personal site on the FlyRank domain + one build-in-public post telling the story.
5. Submit for the final review checkpoint (written sign-off or scheduled review/demo session).

### Deliverable

The submission package + retrospective + completed hours log + live site & post URL.

### Evaluation criteria

- Every deliverable present and reachable from the index
- Retrospective specific to YOUR build, not generic reflection ("what specifically changed in how you work?")
- Hours log complete and plausible against timestamps
- Site live on FlyRank domain, navigable in 5 minutes
- Build-in-public post explains one real decision and one real limitation
- Demo shown is the REAL thing, not slides

### Framework note — AI as a career partner

Use AI as a thinking partner for this: paste your retrospective + README and ask it to help draft your story for an application, LinkedIn post, or university statement. Have it mock-interview you about your own build. Ask where your project is weakest so you can speak to it honestly. You've earned the right to do this well because you actually built the thing.

---

# CAPSTONES

> **Only ONE capstone per track is required** to get that track's completion certificate (5 assignments + 1 capstone minimum). You can do more than one if you want — this section lists every option available so you can pick. Each capstone is self-paced, no deadline, submitted via a public GitHub repo link pasted into the portal (no live presentation, no ZIP uploads).

---

## 🅰️ GENERAL AI FLUENCY CAPSTONES (pick one — they're near-identical, see note below)

> **Note:** "General AI Fluency · Impact Project" (Week 6) and "Send the Link: Launch, Demo & Story" (Week 8) have **identical briefs** in the portal data — both describe the same "plan to keep building" deliverable. Treat them as the same capstone option under two names; do it once, submit to whichever card feels right (or both — they're graded the same way). This may be a portal content duplication bug.

### Impact Project / Send the Link: Launch, Demo & Story

**Workload:** ~4–12h

**Why it matters:** A portfolio that never gets a second project goes stale. The difference between a class artifact and a career platform is one habit, set up now while you remember how everything works.

**Brief:**

1. Write down, in a few lines, exactly where your next case study will go and the steps to add one (reuse the 3-beat shape: problem → what you did → what came of it).
2. Name the next real piece of work you intend to add, set a concrete reminder (calendar nudge, recurring note).
3. Keep your Claude Project — it already knows your voice/stack/identity kit, so the next case is a short conversation, not a rebuild.

**Deliverable:** The short "how to add the next case" note + the named next piece + evidence of the reminder set.

**Pass/revise:**

- Concrete "how to add" note, not a vague intention
- Specific next piece named with a real reminder set
- Build context (Claude Project) preserved

**Clarification from Q&A:** If General AI Fluency is your ONLY track, this capstone is mandatory. If it's a secondary track (Backend is your main), this is optional — but still encouraged.

---

## 🅱️ BACKEND AI ENGINEERING CAPSTONES (pick one — 5 options)

All 5 share the same **ground rules**:

- $0 stack, no credit card, ever
- Self-paced, no deadlines
- Own public GitHub repo, created fresh, named `flyrank-capstone-<short-name>`, never inside your assignments repo
- Required files: `README.md`, `capstone.yaml`, `EVIDENCE.md` (one proof per requirement checkbox), `BUILDLOG.md` (honest AI-usage log), `.env.example`
- AI-assisted building encouraged — you must be able to explain any 2–3 lines an evaluator picks
- No live presentation — repo link + document speaks for you, review is asynchronous
- **Shared requirements every capstone must show:** layered architecture (data/logic/HTTP separated), validation at the boundary (bad input → 4xx never 500), ≥1 background job, real persistence with migrations+indexes, idempotency where it matters, secrets clean (env only, never logged), cost tracked if AI used, tests covering the scary cases

### Option 1 — Usage Metering & Billing Engine

**Difficulty:** Medium | **Time:** ~30–45h

**Mission:** Build the service every SaaS needs: how much has this customer used, what does it cost, have they hit their limit? Metering, quotas, correct money math, Stripe test mode.

**Recommended for:** Newcomers to backend — most bounded scope on the menu (2 plans, 2 usage types, 1 dummy billable endpoint, no AI required anywhere in core).

**The 3 genuinely hard parts:**

1. Exactly-once metering (idempotency-key design) — same retried request = one usage event only
2. Boundary honesty — correct 429/402 at exactly the quota limit
3. Token pricing rules — cached input tokens cheaper, reasoning tokens count as output, categories don't simply add

**What you build:**

1. **Usage metering** — every billable action records a usage event, idempotent via key (retries never double-count)
2. **Quota enforcement** — check current+requested usage against plan limits before allowing; `429` (quota exceeded) or `402` (payment required), with a message explaining why
3. **Cost calculation** — API calls → monthly cost; AI tokens with real pricing rules (cached input cheaper, reasoning=output, categories don't simply add). Simulated token counts, no real AI key needed.
4. **Stripe subscription integration (test mode)** — Checkout flow (Free→Pro), webhook handler for `checkout.session.completed`, `customer.subscription.updated/deleted`. Verify signature, prevent duplicate processing, update tenant plan/status.

**Scope:** 2 plans (Free/Pro), 2 usage types (API calls + AI tokens), 1 dummy billable endpoint (e.g. `POST /generate`). No invoicing/proration/overage in core (those are stretch).

**Build phases:** (1) Design — schema, plans/quotas, idempotency strategy [≈4-6h] → (2) Core billing logic — idempotent tracking + quota enforcement [≈9-13h] → (3) Stripe integration — checkout + webhooks + sync [≈8-12h] → (4) Cost & finalization — rollups + docs [≈7-10h]

**$0 stack:** Node/Express or Python/FastAPI, PostgreSQL via Docker (or SQLite), Stripe test mode (test card `4242 4242 4242 4242`), Stripe CLI for local webhook forwarding (`stripe listen`, `stripe trigger`). Store money as integers (cents), never floats.

**Requirements checklist:**

- [ ] A billable action creates exactly one usage event even under retries, dedup'd by idempotency key — proven in EVIDENCE.md
- [ ] Usage checked against plan; over-limit requests rejected with correct 429/402 + explanatory message
- [ ] Monthly usage rolls up into a cost figure per tenant
- [ ] AI token pricing handles cached/reasoning/output rules correctly, constants pinned in config, proof in EVIDENCE.md
- [ ] Stripe test-mode checkout works end-to-end
- [ ] Webhooks verify signatures, ignore duplicates, update tenant plan/status
- [ ] DB includes tenants/plans/subscriptions/usage events, tenant-isolated
- [ ] README + architecture diagram + setup instructions

**Acceptance probes (how it's graded):**

1. Same request+idempotency key sent twice → exactly one usage event
2. Drive a tenant to exact quota → boundary behaves per documented rule; next request → 429/402
3. Complete Stripe test checkout → webhook flips tenant Free→Pro, `GET /usage` shows new limits
4. Forged webhook (bad signature) → 400, nothing changes; replay a real event twice → processed once
5. Pinned pricing rules produce exact expected totals

**Stretch:** overage billing, invoices, usage alerts (80%/100%), proration, reconciliation job, full test suite.

**Payment note from Q&A:** If Stripe doesn't support your country (India/Pakistan both mentioned in Q&A), use **Razorpay** instead, or implement with mocked/test fixtures — both explicitly approved.

---

### Option 2 — AI Image Understanding & Content Matching Engine

**Difficulty:** Medium (most bounded AI scope) | **Time:** ~35–50h

**Mission:** Build a system that understands an image library, tags it automatically, and matches the right image to the right article — a red-fox post gets the red-fox photo, never the wolf. The key feature is NOT finding a match — it's a **mismatch guard** that safely refuses when no image is good enough, with an explanation.

**The 3 genuinely hard parts:**

1. Trusting the model just enough — schema-validate all vision output, flag low-confidence instead of accepting
2. Tuning the guard — pick similarity thresholds using your own labeled eval set, defend with a precision number
3. Batch discipline — vision calls run as background jobs with retries + per-call cost tracking

**What you build:**

1. **Image ingestion & classification** — run every image through a vision model, produce validated structured metadata (`{subject, category, attributes, caption, confidence}`). Never trust invalid responses; low-confidence flagged not guessed.
2. **Semantic image matching** — embeddings for image descriptions + post content, ranked by similarity. Must match CONCEPTS not exact words ("red fox" ≈ "Vulpes vulpes").
3. **The mismatch guard** — combines tag validation + similarity thresholds + confidence to decide "is this good enough?" Rejects with human-readable explanation (e.g. "Animal category mismatch: expected fox, detected wolf").
4. **Background processing** — vision/embedding calls run async as batch jobs with retries, progress tracking, per-call cost tracking.
5. **Review API** — approve/reject a suggested pairing, inspect why an image was selected/refused.

**Scope:** 40+ images across 4+ categories (e.g. fox/wolf/dog/bear/deer). Labeled eval set: 10+ posts, each marked with its one correct image. One vision model + one embedding model (comparing models is stretch, not core).

**Build phases:** (1) Design — metadata schema, matching strategy, ~50-image dataset [≈4-6h] → (2) Image understanding pipeline — vision + validation + batch + cost tracking [≈10-14h] → (3) Matching engine — embeddings + similarity + the guard [≈12-16h] → (4) Production layer — review API + eval dataset + docs [≈8-12h]

**$0 stack:** Node/Express or Python/FastAPI; **Gemini Flash free tier** (image understanding, no card) OR **Ollama local vision models** (llava/moondream, fully offline); embeddings via Gemini free tier or Ollama all-minilm; Zod/Pydantic for schema validation; PostgreSQL via Docker (pgvector optional at this scale); Unsplash/Pexels for licensed-free images.

**Requirements checklist:**

- [ ] Vision output structured + schema-validated; invalid responses never trusted
- [ ] Low-confidence classifications flagged, not accepted
- [ ] Images processed via batch background job with retries
- [ ] Vision/embedding costs tracked per call
- [ ] Image + post embeddings stored; posts return ranked suggestions
- [ ] Semantic matching works for equivalent concepts
- [ ] Mismatch guard provably rejects wrong matches (the wolf-on-fox-post scenario)
- [ ] Rejections include human-readable explanation
- [ ] "No confident match" answered with reasons when nothing clears the bar
- [ ] DB models + required indexes for images/tags/embeddings/posts/suggestions/approvals
- [ ] Review workflow (approve/reject/inspect why) exists
- [ ] Labeled eval dataset measures top-1 precision, reported in README

**Acceptance probes:**

1. Batch job on corpus → every image schema-valid tags; ≥1 low-confidence flagged
2. Query for "red fox" article → fox ranks first, wolf/dog clearly lower
3. Force wolf as candidate for fox post → guard rejects with category-mismatch explanation
4. Query with no suitable image → "no confident match" + reasons
5. Eval script → top-1 precision matches README number
6. Cost log → every vision/embedding call attributed

**Stretch:** auto alt-text, near-duplicate detection, fallback image generation, human-in-the-loop agent QA, test suite.

**Note from Q&A:** If free vision APIs hit quota issues (Gemini/Groq free vision tiers have been unreliable), it's explicitly fine to **pre-generate metadata manually** via Gemini Chat (no rate limits), store as JSON, and have your pipeline read + validate + insert from those files — mock the LLM call, keep the rest of the pipeline real. Document this honestly in BUILDLOG.md.

---

### Option 3 — Embeddable Widget & Lead-Capture Platform

**Difficulty:** Medium–Hard | **Time:** ~35–50h

**Mission:** Let a customer define a widget (signup form, CTA, popover), hand them one `<script>` line, and safely handle everything the public internet throws back — validated, spam-filtered, enriched, dashboarded. This is a real product category (Intercom, Mailchimp, HubSpot all work this way).

**The 3 genuinely hard parts:**

1. CORS debugging — the browser blocks cross-origin requests with terse errors; expect confusion, it's a rite of passage
2. Thinking like an attacker — rate limiting/spam controls only make sense once you imagine someone flooding your endpoint
3. Failure that must not fail — enrichment chain + email side-effect must degrade gracefully, never break the main response

**What you build:**

1. **Widget management API** — authenticated admin CRUD; tenant-isolated (customer A can never see customer B's widgets)
2. **Embed snippet generation** — `<script src="...widget.js?id=abc123"></script>` — config/rendering/submission all flow from this one line
3. **Fast, cached widget delivery** — correct `Cache-Control` headers; versioned bundle for the script (cache long, bust on release), short-lived cache for config
4. **Public submission endpoint** — cross-origin (correct CORS incl. preflight), validate every field, 4xx on invalid/oversized, store what passes
5. **Protection, enrichment & safe side effects:**
   - Rate limiting (per IP + per widget) + ≥1 spam control (honeypot field, heuristic, or token)
   - IP→geolocation with a **fallback chain**: provider A → provider B on failure → still succeeds without geo if both down ("degrade, never fail")
   - Safe side effects (confirmation email/webhook) — a failure here must NOT break the submission response
6. **Owner dashboard API** — authenticated view of submissions + basic analytics (counts, per-widget stats, geo breakdown)

**Scope:** "Customer site" = a plain HTML file on a different local port (no real hosting/CDN/domain needed). 1–2 widget types enough. Email can be fake (console log or Mailpit). Mock geo providers for the deterministic fallback proof; real free APIs for manual dev only.

**Build phases:** (1) Design — models, embed flow, API contracts, one non-goal [≈4-6h] → (2) Hardened submission path — validation+CORS+rate-limit+spam+geo-fallback+safe side effect [≈14-20h] → (3) Delivery, dashboard & proof — cached delivery + second-origin test page + dashboard + docs [≈12-16h]

**$0 stack:** Node/Express or Python/FastAPI, PostgreSQL via Docker (or SQLite), `ip-api.com` (geo provider A, free, no key, 45 req/min), `ipapi.co` (geo provider B fallback, ~1000/day free), console log or Mailpit (email), plain HTML on a second local port ("customer site"), no hosting required.

**Requirements checklist:**

- [ ] Authenticated CRUD for widgets; unauth requests rejected; multi-tenant isolation proven
- [ ] Embed snippet generated per widget
- [ ] Public config endpoint, small payload, correct cache headers
- [ ] Widget JS served as versioned bundle
- [ ] Widget renders on a page from a different origin than the API
- [ ] Cross-origin submissions work: correct CORS, preflight (`OPTIONS`) handled
- [ ] All input validated; malformed/oversized → 4xx JSON errors
- [ ] Valid submissions stored, linked to correct widget+tenant
- [ ] Rate limiting returns 429 under burst, legitimate traffic still served
- [ ] ≥1 spam-prevention technique demonstrably blocks spam
- [ ] Geo fallback chain proven: A down → B answers → enriched; both down → still succeeds without geo
- [ ] Failing email/webhook doesn't prevent submission success
- [ ] README + architecture diagram + API docs

**Acceptance probes:**

1. Valid submission from second-origin test page → stored, 2xx, visible in dashboard
2. Malformed + oversized payload → clean 4xx, never 500
3. Burst of rapid submissions → 429s appear, normal request right after still succeeds
4. Disable geo provider A → next submission enriched by B; disable both → still stored without geo
5. Force email/webhook to throw → submission still succeeds and is stored
6. Fill honeypot like a bot → submission silently dropped/rejected

**Stretch:** production minified bundle, real-time dashboard (WebSockets/SSE), targeting rules, double opt-in/GDPR, bot defense (proof-of-work/CAPTCHA), full test suite.

---

### Option 4 — Multi-Platform Social Campaign Publisher / Social Media Studio

**Difficulty:** Medium–Hard | **Time:** ~35–55h

> **⚠️ IMPORTANT — two versions exist, read this first:** FlyRank originally published this as **"Multi-Platform Social Campaign Publisher"**, which referenced a fake-platform-server starter folder (`starters/challenge-5-social/`) that was planned but **never actually built/shipped**. They replaced it with the current version, **"Social Media Studio"**, where YOU build the mock platform adapters yourself and publish to at least one REAL free platform (Telegram/Discord/Mastodon) instead of a provided fake server. **If starting fresh, use Social Media Studio (below) — it's simpler and is the current official brief.** If you'd already started on the old version, FlyRank says it's still valid; you'd just need to replace the missing fake-server piece yourself (write ~150 lines of Express/FastAPI mock, or use Mockoon/WireMock/Prism, or just publish to a real free platform — same fix either way).

### → Use: Social Media Studio (current version)

**Mission:** Turn one published blog post into a social media campaign. Generate one variant per platform (different length/tone/hashtag rules), a human approves each variant, a scheduler publishes each approved variant **exactly once**.

**The hard parts:**

1. Idempotency — a retry after timeout must never make a second post
2. Constraint profiles — each platform has rules; your CODE must enforce them, not hope
3. Durable scheduling — a worker that crashes mid-batch must resume without duplicate posts
4. The adapter seam — your app must never know which platform it's publishing to

**What you build:**

1. **Post ingestion** — accept a blog post as URL or pasted Markdown; stored post is the single source of truth
2. **Variant generation with constraint profiles** — one variant per platform (X-style short, LinkedIn-style long, Instagram-style caption); each platform has a constraint profile (max length, tone, hashtag count) enforced BY CODE before review
3. **Review workflow** — statuses: `draft → approved/rejected → published`. Only approved variants can be scheduled; unapproved schedule attempt → 4xx
4. **Publisher adapter layer** — one `SocialPublisher` interface, ≥3 implementations: one REAL free platform (Telegram bot / Discord webhook / Mastodon) + ≥2 mock adapters you write yourself (record what they'd post + show a preview)
5. **Idempotent scheduling + publish history** — scheduler publishes approved variants at their time, through the adapter, exactly once even under retries/worker-crash-mid-batch. Every attempt recorded in a visible publish history.

**Scope:** Real accounts only on targets you own that permit bots — never publish to real Instagram/X/LinkedIn (those are always mock adapters). 2 platforms minimum.

**Build phases:** (1) Design — constraint profiles, interface signature, data model [≈4-6h] → (2) Ingestion and generation — endpoint + 2-platform generator + validation [≈6-8h] → (3) Review workflow — statuses + approve/reject/schedule-refusal [≈6-8h] → (4) Adapters and idempotent publish — real adapter + 2 mocks + idempotency key [≈10-14h] → (5) Scheduling, history, hardening — durable worker + crash-resume proof + publish history [≈8-12h]

**$0 stack:** Node/Express or Python/FastAPI; Telegram Bot API / Discord webhook / Mastodon API (free, your own channel); SQLite or Postgres via Docker; Gemini free tier/Ollama/hand-written templates for variant text (AI optional, enforcement is what's graded); BullMQ+Redis(Docker) or APScheduler with a persistent job store for scheduling.

**Requirements checklist:**

- [ ] Ingestion: post enters as URL or Markdown, stored; generation reads only the stored post
- [ ] Constraint profiles enforced BY CODE per platform; proof of a blocked bad variant in EVIDENCE.md
- [ ] Review workflow with 4 statuses; unapproved schedule attempt → 4xx with error naming the issue
- [ ] Adapter layer: 1 interface, 1 real free platform, ≥2 mocks; adapter swap = config change only
- [ ] Idempotent publish: same variant+slot never posts twice even under retries — proof in EVIDENCE.md
- [ ] Durable scheduling: worker restart mid-batch → zero duplicate posts
- [ ] Publish history: every attempt recorded + visible with result
- [ ] Secrets clean (tokens in `.env` only)
- [ ] README + architecture diagram + run steps

**Acceptance probes:**

1. Ingest sample post → variants generated, each passes its constraint profile
2. Variant breaking a platform rule → validation blocks it with error naming the broken rule
3. Try scheduling unapproved variant → refused with 4xx + error
4. Approve + schedule → publishes to real free target; publish record links to the live message
5. Force a retry (stop worker mid-publish, restart) → history shows exactly one successful post
6. Swap adapter in config (e.g. telegram → mock_x) → same campaign publishes through mock, no code change outside adapters

**Stretch:** A/B variants with pick-the-winner flow, a grounding check (claims must exist in source post — catches planted fake stats), cost tracking per campaign if AI used, multi-tenant isolation, full test suite for the scary cases.

---

### Option 5 — Your 10x Solution (build your OWN idea)

**Difficulty:** You set it | **Time:** ~3 weeks part-time (scope-guarded)

> **This is the one for you if you have your own project idea** — like the GitHub-repo-understanding-assistant concept we talked about earlier, or anything else you've been wanting to build. This capstone IS the "build your own idea" option mentioned throughout the other capstone briefs.

**Mission:** You saw a problem, you have a solution. Build it for real and make it count. Your canvas — you define the problem, the technology, the design.

**The concept rule (the heart of this brief):** Your solution is free-form, but the ENGINEERING is not. Pick **at least 5 of these 7 concepts** and implement them:

1. API endpoints — real HTTP API, correct status codes, validation
2. Database — real persistence, survives a restart
3. Authentication — users log in, protected routes actually protected
4. Background jobs or cron jobs — slow work off the request path, or scheduled work
5. Reporting — PDF or email output
6. Caching logic — expensive result stored and reused
7. LLM integration — one narrow AI job behind an endpoint, validated, cost-logged

**Swap rule:** If a concept doesn't fit, swap up to **2 of your 5** for: web scraping pipeline, webhook receiver, RAG with citations, agent with guardrails, containerized stack, test suite, rate limiting/quotas, or deployment. At least 3 of your 5 must come from the original 7.

**Constraints:**

- $0 stack, no credit card
- No secrets in Git
- No other people's personal data (use your own/seeded/public data)
- Your repo, your code — AI help encouraged but you must understand every line
- **Scope guard:** core must be buildable in ~3 weeks part-time. Write your core as a feature list; if it's >5 features, cut it down.

**Build order — 5 milestones:**

1. **The one-pager** (one evening) — problem (3 sentences), who has it, your 10x claim (what becomes 10x faster/cheaper/easier), your 5+ concepts, one explicit non-goal
2. **The walking skeleton** (one weekend) — thinnest slice that runs end-to-end: one endpoint → logic → database → response. Ugly is fine, it must run.
3. **The concepts, one at a time** (~2 weeks) — add remaining concepts one at a time, never two half-built at once: small step → test → commit
4. **Make it runnable by a stranger** (one weekend) — README with exact run steps, seed/demo data, a 5-minute demo path written down
5. **Package and submit** (one evening) — finish overview doc, walk the requirements, tick every box

**Submission (unique to this capstone):**

- Public GitHub repo link
- PLUS one overview document named exactly: `My 10x Solution - Kunal Aggarwal.md` (or `.docx`), 1–2 pages answering: (1) what problem you're solving, in plain words a stranger understands, (2) how you implemented it — name your 5+ concepts (with one line per swap), give run steps.
- **No live presentation.**

**Requirements checklist:**

- [ ] Problem written down in the overview document, a stranger can understand it
- [ ] ≥5 concepts from section 2 implemented, listed in README as a table (concept → where in code)
- [ ] Max 2 swaps, each with a one-line reason
- [ ] System starts with 1-2 documented commands on a clean machine
- [ ] Demo data seeded; README's 5-minute demo path works
- [ ] No secrets in repo; `.gitignore` covers env files/DBs/artifacts
- [ ] Repo public on GitHub

**Stretch:** deploy to a free hosting tier with a live URL, record a 2-min demo video/GIF, measure the actual 10x (one number, before vs after), a test suite for scary cases (if not one of your 5).

**What NOT to build:** no mobile apps, no pixel-perfect UI (a plain page/clean API is enough), no real money/real users/real scale, no second product (one problem, one solution — park shiny tangents in a README "Future ideas" section).

**Reuse your own assignment work freely** — e.g. your BE-01 CRUD patterns, BE-02 database, BE-03 auth, BE-06 background jobs, BE-08 PDF reports, BE-07 LLM integration, BE-05 scraper — "copying from your own assignment repos is not cheating, it's the point."

---

# ✅ SUGGESTED FOLDER STRUCTURE FOR YOUR IDE

```
flyrank-internship/
├── week-01/
│   ├── FL-01-workflow-audit/
│   ├── draw-the-path/
│   └── what-are-you-proving/
├── week-02/
│   ├── BE-01-crud-api/
│   ├── FL-02-prompting-fundamentals/
│   ├── frame-it-as-cases/
│   └── the-prompt-ladder/
├── week-03/
│   ├── BE-02-connecting-database/
│   ├── BE-04-containerize-stack/
│   ├── decide-once-identity-kit/
│   ├── kill-your-darlings-images/
│   └── the-through-line/
├── week-04/
│   ├── BE-03-auth-login-protect/
│   ├── FL-05-agent-concepts-mcp/
│   ├── FL-04-automation-workflow/
│   ├── empty-but-live/
│   └── three-roads-choose-stack/
├── week-05/
│   ├── BE-05-polite-scraper/
│   ├── FL-06-design-personal-agent/
│   ├── PF-04-personal-website/
│   ├── explain-it-like-you-built-it/
│   └── FL-07-build-the-agent/
├── week-06/
│   ├── BE-07-llm-behind-api/
│   ├── make-it-do-something/
│   ├── open-it-on-your-phone/
│   └── survive-the-crit/
├── week-07/
│   ├── BE-06-background-job/
│   ├── BE-08-pdf-report-generator/
│   ├── BE-09-ai-decision-flow/
│   ├── break-your-own-site/
│   └── plant-your-flag-domain-badge/
├── week-08/
│   ├── the-plan-to-keep-building/
│   ├── FL-09-documentation-demo-video/
│   └── FL-10-final-package-retrospective/
└── capstones/
    ├── fl-capstone-impact-project/
    └── be-capstone-<whichever-you-pick>/
```

---

# 🎯 RECOMMENDED EXECUTION ORDER (fastest path through everything)

Since both tracks share Week 1–3 setup work, and Backend assignments build on each other sequentially, this order minimizes rework:

1. **Week 1 all 3** → quick wins, sets up both tracks
2. **BE-01** (needed before BE-02/03/04) → **FL-02** → **Frame It as Cases** → **The Prompt Ladder**
3. **BE-02 → BE-04** (DB then containerize, sequential dependency) → rest of Week 3 FL items
4. **BE-03** (needs BE-02's DB) → **FL-05 → FL-04** → rest of Week 4 FL items
5. **BE-05** (standalone, no deps) → **FL-06 → FL-07** → **PF-04** → **Explain It Like You Built It**
6. **BE-07** (standalone) → rest of Week 6 FL items
7. **BE-06 → BE-08** (BE-08 stretch goal references BE-06) → **BE-09** → rest of Week 7 FL items
8. **Week 8 FL wrap-up items**
9. **Pick + build 1 capstone per track** (recommend: **Your 10x Solution** for Backend if you want to build your own GitHub-assistant idea, since it's genuinely the strongest portfolio piece; or **Usage Metering & Billing Engine** if you want the cleanest, most contained build)

---

_End of tracker. This file is self-contained — every stage, requirement, evaluation criterion, free-tool swap, and Q&A clarification needed to execute this internship end-to-end is captured above._
