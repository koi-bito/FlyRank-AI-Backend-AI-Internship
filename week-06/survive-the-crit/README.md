# Survive the Crit: External Design & Positioning Review

**Track:** General AI Fluency  
**Author:** Kunal Aggarwal  
**Reviewer:** Peer Senior Backend Engineer & Technical Mentor  
**Date:** October 2026  
**Status:** Completed  

---

## 1. The Two Benchmark Questions & Raw Feedback

I presented the live portfolio alongside my proof statement to an external technical reviewer without providing any introductory sales pitch:

### Question 1: *"In 10 seconds, what do I do?"*
> **Reviewer Answer:** *"You're a backend engineer who builds APIs and background workers that don't fall over when external AI services or databases hiccup."*  
> **Verdict:** **SUCCESS.** The positioning landed in under 10 seconds.

### Question 2: *"Would you believe I'm good at it?"*
> **Reviewer Answer:** *"Yes, because you lead with actual curl commands, status codes (202, 400, 401), and Inngest/Docker specifics rather than waving your hands about AI revolutions. But there are a few rough edges in your flow."*

---

## 2. Feedback Triage: Must-Fix vs. Nice-to-Have

| Feedback Item | Classification | Why / Action Taken |
|---|---|---|
| **"The booking call button only existed at the very bottom."** | **MUST-FIX** | If a technical director is sold within 15 seconds, making them scroll past three case studies to find the booking link causes drop-off. **Fixed:** Added a high-contrast primary CTA `[Book 20-Min Technical Walkthrough]` directly in the hero banner. |
| **"The interactive simulator didn't show what headers were sent."** | **MUST-FIX** | It showed JSON responses, but didn't show the `Authorization: Bearer` or `Content-Type` headers that prove HTTP mastery. **Fixed:** Updated terminal presets to display the full HTTP header block. |
| **"Add a dark/light mode toggle."** | **NICE-TO-HAVE** | Dark mode (`#090D16`) fits our terminal aesthetic perfectly; building a light mode theme adds styling complexity for zero conversion gain. Shelved for later. |
| **"Add blog post articles about your favorite libraries."** | **NICE-TO-HAVE** | Our proof relies on reproducible code and case studies; writing generic blog tutorials distracts from the single target action. Shelved. |

---

## 3. Evidence of Must-Fixes Addressed on the Live Site

1. **Sticky & Hero CTA Placement:** Updated `index.html` hero section with dual action buttons: `[Book 20-Min Technical Walkthrough]` and `[Inspect Case Studies]`.
2. **Full HTTP Header Inspection in Simulator:** The interactive terminal now renders the complete raw HTTP response block including `HTTP/1.1 200 OK`, `Content-Type: application/json`, and relevant headers.
3. **Engaged with Feedback:** No defensive excuses were made; feedback was categorized solely by whether it accelerated or hindered the target action (scheduling a walkthrough call).

---

## 4. Pass / Revise Self-Check

- [x] Portfolio submitted with proof statement and real external feedback collected.
- [x] Reviewer could immediately state what I do and felt backed up by concrete technical proof.
- [x] Feedback triaged objectively between Must-Fix and Nice-to-Have.
- [x] Must-fixes verified and implemented on the live site.
