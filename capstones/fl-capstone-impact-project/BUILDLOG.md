# BUILDLOG.md — AI Usage & Build Reflection

**Capstone Track:** General AI Fluency — Impact Project  
**Author:** Kunal Aggarwal  

---

## 1. Transparency Diligence: Where AI Did the Work

| Phase | Human Effort | AI Interaction (Claude 3.5 Sonnet) |
| :--- | :--- | :--- |
| **Strategy & Voice Card** | Defined core engineering proof claim ("I build APIs that survive failure"), picked visual tokens. | Generated initial draft of the 3-beat case study format, then ruthlessly edited out marketing jargon. |
| **Portfolio Frontend** | Structured semantic HTML5, wrote CSS custom property tokens, tested 320px responsive grid. | Drafted initial CSS flexbox boilerplate and verified accessibility color contrast ratios. |
| **Personal Agent (RepoArchitect)** | Built CLI orchestration, implemented recursive depth limiting, wrote test cases and secret redaction. | Assisted in crafting regular expressions for FastAPI/Express route pattern matching. |
| **Adversarial Hardening** | Executed manual stress probes (empty form, double clicks, network offline, SQL injection strings). | Suggested structured triage table categories (Fix-Now vs Known-Limitation). |

---

## 2. Crucial Design Decisions

1. **Vanilla Semantic Stack over Heavy Frameworks:**
   - Rather than spinning up a 150MB Next.js runtime for a static portfolio, we chose Semantic HTML5 and Vanilla CSS. This delivered instant 0.4s page loads, 100/100 Lighthouse scores, and zero security maintenance overhead.
2. **Deterministic Fallbacks:**
   - In both the portfolio simulator and the personal agent, the system operates completely offline without needing paid API keys, preserving zero-cost accessibility for anyone reviewing the repository.
