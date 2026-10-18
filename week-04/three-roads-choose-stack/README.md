# Three Roads: Choosing the Portfolio Tech Stack with AI

**Track:** General AI Fluency  
**Author:** Kunal Aggarwal  
**Date:** October 2026  
**Status:** Completed  

---

## 1. Project Constraints & Requirements

- **Budget:** Exactly $0. No credit card, no monthly hosting fees, no domain renewal dependencies.
- **Skill Level:** Strong in backend engineering (Python/FastAPI, Node.js/Express, Docker, SQL); comfortable with clean HTML, Vanilla CSS, and modern JavaScript; pragmatic on frontend UI.
- **Portfolio Job:** Showcase backend resilience, verified curl outputs, Inngest background job architecture, and Docker stacks. Drive visitors toward a single action: **Booking a 20-minute code walkthrough call**.
- **Display Needs:** High-contrast terminal blocks, interactive preset sandbox, responsive mobile layout, SVG monogram branding, and Cal.com embed.
- **Dynamic Requirement:** "Does it need a backend on day 1?" **Answer: No.** Case studies are proven through verified GitHub repos, live curl snippets, and interactive frontend simulation. A dedicated backend server for the presentation layer would add maintenance risk, cold starts, and potential downtime for zero user benefit.

---

## 2. The Three Stack Options Evaluated

| Evaluation Metric | Road 1: Static HTML5 + Vanilla CSS (Simplest) | Road 2: Astro or Vite SSG (Intermediate) | Road 3: Next.js + Tailwind + Vercel (Most Powerful) |
|---|---|---|---|
| **Build Method** | Hand-crafted semantic HTML5, custom CSS tokens, modern ES6 modules. Zero build step. | Static Site Generator compiling Markdown and components into pure HTML. | React 19 Server Components, App Router, Tailwind CSS, API routes. |
| **Hosting Path ($0)** | Netlify, Cloudflare Pages, or GitHub Pages (instant drag-and-drop). | Netlify or Vercel Hobby Tier. | Vercel Hobby Tier. |
| **Backend Required?** | **No.** 100% static client bundle. | **No.** Pre-rendered static pages. | Optional (API routes available). |
| **Build Tooling** | None (`index.html` opens directly in browser). | Node/npm build script required. | Heavy Node dependencies, continuous webpack/turbopack compilation. |
| **Major Trade-off** | Requires manual markup for repeated elements. | Requires learning Astro component syntax and build pipeline. | Massive dependency overhead; easy to break with React hydration errors or SSR version mismatches. |

---

## 3. Pressure-Testing the Options

1. **What breaks if I pick Road 1 (Static HTML + Vanilla CSS)?**  
   Nothing breaks. There are zero build scripts, zero dependency vulnerabilities, zero bundler errors, and zero cold starts. It loads in under 200ms anywhere in the world on a free CDN.
2. **What must I maintain if I pick Road 3 (Next.js)?**  
   I have to maintain a Node package tree with 400+ dependencies, resolve periodic breaking changes in Next.js App Router, debug React hydration mismatches between server and client, and risk hitting Vercel serverless function limits. For a portfolio site, this is self-inflicted architectural friction.
3. **Can I finish and launch in 2 weeks?**  
   Road 1 can be built, styled with our exact Identity Kit, tested, and deployed to Netlify in 3 to 4 hours. Road 3 would consume 15 hours on styling framework setup and component configuration alone.

---

## 4. Final Architectural Decision & Rationale

> **"I have chosen Road 1: Modern Semantic HTML5 + Vanilla CSS deployed to Netlify.**
> 
> **Why Road 1 won:** As a backend AI engineer, my credibility comes from technical discipline and zero-waste architecture. Loading 50MB of React and Tailwind dependencies just to display three case studies, an interactive terminal, and a Cal.com booking link contradicts everything I preach about resilient, low-overhead systems. 
> 
> With pure HTML5 and Vanilla CSS using our defined design tokens (`#090D16`, `#10B981`, `Space Grotesk`), every single line of code in the deployment is 100% understood and directly editable. It renders instantly on mobile, never fails due to bundler deprecation, and deploys to Netlify with zero build-step friction. 
> 
> **Why I rejected Road 2 & 3:** Astro and Next.js are outstanding tools for multi-author content hubs or dynamic web apps, but for this portfolio, they introduce build complexity and maintenance overhead that add zero evidentiary value to the hiring manager reading my proof."**

---

## 5. Pass / Revise Self-Check

- [x] 3 genuine stack options analyzed with explicit trade-offs and hosting paths.
- [x] Chosen stack is completely free and matched to real evidentiary goals.
- [x] Written rationale in original engineering voice with honest "can I maintain this" analysis.
- [x] Backend necessity answered honestly ("not yet needed on day 1 for the presentation layer").
