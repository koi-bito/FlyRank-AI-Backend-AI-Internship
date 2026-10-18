# PF-04: Personal Website Live & The Plain-Words DNS Walkthrough

**Track:** General AI Fluency  
**Code:** PF-04  
**Author:** Kunal Aggarwal  
**Live URL:** `https://kunal-backend-ai.netlify.app` *(tested over HTTPS)*  
**Date:** October 2026  
**Status:** Completed  

---

## 1. Overview & Deployed Artifacts

The personal website is live over HTTPS via Netlify's global edge network. It directly reflects our identity kit, content map, and proof statement:
- **Zero-Dependency Architecture:** Pure Semantic HTML5 and Vanilla CSS. No React hydration overhead, no bundler compilation lag, 100% testable in any browser.
- **Evidentiary Components:** 3 architectural case studies (BE-07 LLM API, BE-06 Inngest queue, BE-04 Docker Postgres), interactive endpoint simulator with 1-click status probes, and direct Cal.com scheduling.
- **File Structure:**
  - `index.html`: Complete, self-contained, responsive single-page web app.
  - `logo.svg`: Vector monogram favicon with emerald status beacon.

---

## 2. The Plain-Words DNS Walkthrough

*How the Internet Translates a Human Name into a Live Server (Explained for Non-Technical Stakeholders)*

### The Problem DNS Solves
Computers on the internet do not understand human names like `kunal-backend-ai.netlify.app`. They communicate exclusively through numerical IP addresses (such as `104.198.14.52`). **DNS (Domain Name System)** is the global, distributed phonebook of the internet that translates memorable names into numerical server destinations.

---

### The 4-Step Journey: From Typing to Answering
When someone types `kunal-backend-ai.netlify.app` into a phone or laptop browser and presses Enter, an automated chain of events unfolds in under 50 milliseconds:

```
[1. Browser/User] ──(Where is kunal-backend-ai.netlify.app?)──► [2. Recursive Resolver (ISP/Google 8.8.8.8)]
                                                                           │
                                           ┌───────────────────────────────┴───────────────────────────────┐
                                           ▼                               ▼                               ▼
                                  [Root Nameserver]             [TLD Nameserver (.app)]        [Authoritative Netlify NS]
                                           │                               │                               │
                                           └───────────────────────────────┼───────────────────────────────┘
                                                                           ▼
[1. Browser/User] ◄──(Connect to IP: 104.198.14.52)────────────── [Resolver Answers with CNAME/A IP]
       │
       ▼
[Netlify Edge Server] ──(Delivers HTML + CSS over TLS/HTTPS)──► [Visitor Sees Kunal's Portfolio]
```

1. **The Recursive Resolver (The Courier):**  
   The user's computer checks its local memory (cache). If it hasn't visited recently, it sends a query to a **Recursive Resolver** (typically operated by an ISP, or Google at `8.8.8.8`). The resolver's sole job is to track down the address across global phonebooks.
2. **The Root & TLD Nameservers (The Library Indexes):**  
   The resolver asks a **Root Nameserver** ("Where do I find `.app` domains?"). The Root server points it to the **TLD (Top-Level Domain) Nameserver** for `.app`. The `.app` server looks up the domain registry and directs the resolver to **Netlify’s Authoritative Nameservers**.
3. **The Authoritative Nameserver (The Official Record Keeper):**  
   Netlify’s nameserver holds the master record for `kunal-backend-ai.netlify.app`. It inspects its DNS table and answers: *"That domain points to our edge server at IP address `104.198.14.52`."*
4. **The Response & Connection:**  
   The resolver hands this IP back to the user's browser, which opens an encrypted HTTPS connection to Netlify, retrieves `index.html`, and displays the portfolio.

---

### What is a CNAME Record? (The Alias Rule)
In DNS, there are two common ways to point a domain:
- **An `A` Record (Address):** Maps a name directly to a hardcoded numerical IP address (e.g. `example.com` ➔ `192.0.2.1`).
- **A `CNAME` Record (Canonical Name):** Maps one domain name to *another domain name* as an alias.

#### Plain-English Analogy:
Think of an `A` record like writing someone's permanent street address on an envelope ("123 Elm Street"). If the resident moves, all incoming letters get lost.  
A `CNAME` record is like writing "Deliver to Kunal's current workplace." When Netlify moves servers or routes traffic across 50 international data centers to optimize speed, they change their internal IPs. Because our custom subdomain uses a **CNAME** pointing to Netlify's network (`kunal-backend-ai.netlify.app` ➔ `netlify.app`), our site remains live automatically without us ever having to update IP addresses manually.

---

## 3. Evaluation Checklist

- [x] Site live and loading over HTTPS on a clean public URL (`kunal-backend-ai.netlify.app`).
- [x] Contains core positioning, case studies, interactive terminal, and working links (LinkedIn, GitHub, Cal.com).
- [x] DNS walkthrough is technically rigorous yet completely accessible to a non-technical reader.
- [x] Every file in the deployed repository (`index.html`, `logo.svg`) is understood and purpose-built.
- [x] Tested across multiple screen sizes and private browsing windows.
