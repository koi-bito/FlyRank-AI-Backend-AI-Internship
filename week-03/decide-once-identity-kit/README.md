# Decide Once: The Identity Kit

**Track:** General AI Fluency  
**Author:** Kunal Aggarwal  
**Date:** October 2026  
**Status:** Completed  

---

## 1. Typography Selection

| Usage | Font Family | Source | Why It Was Chosen |
|-------|-------------|--------|-------------------|
| **Headings & Display** | `Space Grotesk` (weights 600, 700) | Google Fonts (Free / Open Source) | Technical, monospace-adjacent aesthetic that signals engineering precision without looking like raw unformatted code. |
| **Body & Code** | `Inter` (weights 400, 500) & `JetBrains Mono` | Google Fonts (Free / Open Source) | Ultra-clean neutral readability on mobile screens; monospace font for verified curl requests and status codes. |

---

## 2. Color Palette (Calm & Technical)

The palette is intentionally restrained so that backend code diffs, curl outputs, and status badges remain the loudest visual element on the screen:

| Token Name | Hex Code | Visual Swatch Preview | Role & Purpose |
|------------|----------|-----------------------|----------------|
| **Deep Background** | `#090D16` | Dark Charcoal / Deep Navy | Modern dark mode canvas; minimizes eye fatigue. |
| **Surface Card** | `#0F172A` | Slate 900 | Elevated container for case studies and terminal blocks. |
| **Border / Divider** | `#1E293B` | Slate 800 | Subtle 1px structural lines for technical rigor. |
| **Primary Text** | `#F8FAFC` | Near-White Slate 50 | High contrast, crisp readability for all body copy. |
| **Muted Text** | `#94A3B8` | Slate 400 | Secondary metadata, dates, and parameter types. |
| **Electric Accent** | `#10B981` | Emerald 500 | Signals system health (`200 OK`, active workers, primary CTA). |
| **Error / Alert** | `#F43F5E` | Rose 500 | Reserved exclusively for 4xx/5xx failure mode proofs. |

---

## 3. Logo & Monogram Favicon

A vector monogram (`logo.svg`) was designed combining the initials `KA` with a live operational status beacon:
- Vector file: `week-03/decide-once-identity-kit/logo.svg`
- Embedded below:
  ![KA Monogram Logo](file:///c:/GITHUB%20Repos/FlyRank%20AI%20-%20Backend%20AI%20Internship/week-03/decide-once-identity-kit/logo.svg)

---

## 4. The Two-Line Style Note (Added to Claude Project)

> **"Typography: Space Grotesk (headings) and Inter (body). Palette: Deep Slate (`#090D16`), Card (`#0F172A`), Text (`#F8FAFC`), and Emerald Accent (`#10B981`). Mood: A high-density, calm engineering terminal where verifiable code and status codes speak louder than decorative styling."**

---

## 5. Pass / Revise Self-Check

- [x] Exactly 1–2 fonts chosen (`Space Grotesk` + `Inter`), not a generic pile.
- [x] Tight palette (4 core shades + 1 emerald accent) with verified hex codes.
- [x] Clean, scalable vector monogram/favicon created (`logo.svg`).
- [x] Two-line style note describes a coherent engineering mood and is saved to the Claude Project instructions.
