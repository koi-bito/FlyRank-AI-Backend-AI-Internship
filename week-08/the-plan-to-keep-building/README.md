# The Plan to Keep Building

**Track:** General AI Fluency  
**Stage:** Week 8 Habit Architecture  
**Author:** Kunal Aggarwal  

---

## 1. How to Add the Next Case Study: 15-Minute Protocol

To prevent the portfolio from decaying into a frozen one-off snapshot, adding future case studies follows a rigid 3-beat markdown structure. Any new backend project can be added directly to `index.html` within 15 minutes by adhering to this protocol:

### The 3-Beat Content Shape:
1. **The Problem (Beat 1 — 2 sentences):**
   - What broke or what boundary failed? No abstract marketing preamble. Name the exact error, throughput bottleneck, or billing leak.
2. **What I Built (Beat 2 — 3 sentences):**
   - The concrete technical mechanism (e.g., SQLite query caching, Inngest background event queue with exponential backoff, Dockerized PostgreSQL repository abstraction). Name the language, framework, and exact files.
3. **What Came of It (Beat 3 — 2 sentences + proof):**
   - The verified metric or terminal checkpoint (e.g., 202 Accepted in 2ms, 0 unhandled 500 errors, 100% test pass rate across 8 benchmark edge cases). Include a one-line terminal command showing proof.

### Deployment Workflow:
```bash
# 1. Duplicate existing .card div in week-05/PF-04-personal-website/index.html
# 2. Fill in the 3 beats
# 3. Commit and push to main
git commit -am "feat: add case study 4 - usage metering engine"
git push origin main
# 4. Netlify auto-deploys in 22 seconds via GitHub Webhook
```

---

## 2. The Named Next Piece of Work

- **Project Name:** *LLM Usage Metering & Quota Billing Gateway* (Backend Capstone Engine)
- **Target Completion Date:** November 2026
- **Scope:**
  - Token-level metering service tracking cached vs reasoning tokens across multi-tenant API keys.
  - Idempotent request ledger ensuring zero double-charging on network retries.
  - Hard HTTP 429 quota enforcement with Stripe webhook synchronization.
- **Calendar Reminder Scheduled:**
  - **Cadence:** Bi-weekly recurring calendar event every alternate Sunday at 18:00 UTC.
  - **Nudge Text:** *"Ship Case Study #4: Review Metering Engine repository, extract the 3 beats, update live portfolio on Netlify."*
  - **Tool:** Google Calendar + iOS Reminders sync.

---

## 3. Preserved Claude Project Context

The custom Claude Project (`FlyRank Backend Engineering & Portfolio Suite`) established in Week 1 remains active and pre-loaded with:
1. **Voice Card Rules:** Direct, active voice, zero adjectives/buzzwords ("seamless", "cutting-edge"), technically grounded in code.
2. **Visual Tokens:** Slate `#090D16`, Emerald `#10B981`, Space Grotesk / Inter typography.
3. **Proof Mandate:** Every claim must link directly to an existing file, test assertion, or curl output.

When drafting the next case study, generation requires only pasting the raw git commit log and tests into the Claude Project thread with the prompt:
> *"Extract the 3-beat case study card for the metering engine using my voice card and identity kit tokens."*
