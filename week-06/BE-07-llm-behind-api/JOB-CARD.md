# JOB-CARD: Customer Support Message Triage & Urgent Escalation Engine

**Component:** BE-07 LLM API Boundary  
**Service:** Inbound Support Message Classifier & Routing Gateway  
**Author:** Kunal Aggarwal  
**Prompt Version:** `v1` (`prompts/triage-v1.md`)  

---

### 1. What It Does
Takes an unformatted, messy inbound customer message, classifies it into a closed set of business categories, assigns an urgency rating, identifies the target response team, calculates a confidence score, provides a 1-sentence clean summary, and flags whether the message requires immediate managerial escalation.

### 2. Input Shape
```json
{
  "message": "string (1 to 2000 characters, required)"
}
```

### 3. Output Shape (Closed Enums Spelled Out)
```json
{
  "category": "technical_support | billing | sales | security_incident | other",
  "urgency": "low | medium | high | critical",
  "assigned_team": "support_tier_1 | support_tier_2 | finance | sales_reps | security_ops",
  "confidence": 0.0 to 1.0,
  "summary": "string (single concise sentence, max 120 chars)",
  "requires_escalation": boolean
}
```

### 4. What It Must NEVER Do
- Never invent non-existent categories (e.g. "complaint", "feedback").
- Never guess if the input is completely ambiguous or garbled.
- Never return conversational preamble or non-JSON markdown blocks.
- Never evaluate financial totals or process account cancellations.

### 5. What to Do When Unsure
If the message is ambiguous, empty, in an unknown language, or spam:
- Assign `"category": "other"`
- Assign `"urgency": "low"`
- Assign `"assigned_team": "support_tier_1"`
- Set `"confidence": 0.3` (or below)
- Set `"requires_escalation": false`
- Do not hallucinate intentions.
