import os
import time
import json
import re
from typing import Optional, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def get_openai_client() -> Optional[Any]:
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = "https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else os.getenv("OLLAMA_BASE_URL")
    if api_key and OpenAI:
        return OpenAI(api_key=api_key, base_url=base_url)
    return None

def evaluate_decision_node(prompt: str, context: str) -> Dict[str, Any]:
    """
    Evaluates an AI decision prompt against input context.
    Strictly yields either YES or NO with a concise rationale.
    Guarantees deterministic zero-dollar fallback when no external LLM key is configured.
    """
    start_time = time.time()
    client = get_openai_client()
    model_name = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct:free")

    if client:
        try:
            system_msg = (
                "You are an automated binary triage engine inside a workflow orchestrator. "
                "Evaluate the user's question against the context. "
                "You MUST reply with a JSON object: {\"decision\": \"YES\" | \"NO\", \"rationale\": \"one concise sentence\"}."
            )
            user_msg = f"Question: {prompt}\nContext: {context}"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.0,
                max_tokens=60
            )
            raw_text = response.choices[0].message.content.strip()
            
            # Extract JSON or YES/NO from text
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                dec = parsed.get("decision", "").strip().upper()
                if dec in ["YES", "NO"]:
                    latency = int((time.time() - start_time) * 1000)
                    return {
                        "decision": dec,
                        "rationale": parsed.get("rationale", "Evaluated by LLM."),
                        "latency_ms": latency,
                        "model": model_name
                    }
        except Exception as e:
            print(f"[ENGINE NOTICE] External API call failed or timed out: {e}. Falling back to deterministic evaluator.")

    # Fallback deterministic evaluator ($0 budget / offline mode)
    latency = int((time.time() - start_time) * 1000)
    p_lower = prompt.lower()
    c_lower = context.lower()

    # Rule-based heuristics for testing support triage / code review / security gates
    is_yes = False
    rationale = ""

    if "billing" in p_lower or "charge" in p_lower or "refund" in p_lower or "invoice" in p_lower:
        if any(w in c_lower for w in ["charge", "billed", "invoice", "payment", "card", "refund", "subscription", "money", "dollar", "$"]):
            is_yes = True
            rationale = "Context explicitly mentions transactional or billing keywords."
        else:
            is_yes = False
            rationale = "Context does not relate to payment or invoicing."
    elif "urgent" in p_lower or "critical" in p_lower or "emergency" in p_lower or "crash" in p_lower:
        if any(w in c_lower for w in ["urgent", "down", "crash", "immediately", "broken", "critical", "outage", "production"]):
            is_yes = True
            rationale = "Context indicates critical production outage or urgent escalation."
        else:
            is_yes = False
            rationale = "No high-severity urgency markers detected."
    elif "technical" in p_lower or "bug" in p_lower or "error" in p_lower:
        if any(w in c_lower for w in ["error", "exception", "bug", "stack trace", "fail", "timeout", "500", "code"]):
            is_yes = True
            rationale = "Technical defect or software error identified in context."
        else:
            is_yes = False
            rationale = "Context lacks software engineering or bug indicators."
    elif "security" in p_lower or "vulnerability" in p_lower:
        if any(w in c_lower for w in ["sql injection", "xss", "cve", "auth bypass", "vulnerability", "leak", "exploit"]):
            is_yes = True
            rationale = "Critical security exploit pattern matched."
        else:
            is_yes = False
            rationale = "Context is free of known security vulnerability signatures."
    else:
        # Default lexical matching
        keywords = [w for w in re.findall(r'\b\w+\b', p_lower) if len(w) > 3 and w not in ["this", "that", "with", "from", "does"]]
        matched_count = sum(1 for kw in keywords if kw in c_lower)
        if matched_count > 0:
            is_yes = True
            rationale = f"Matched key contextual terms ({matched_count} matches)."
        else:
            is_yes = False
            rationale = "Query conditions did not match context criteria."

    return {
        "decision": "YES" if is_yes else "NO",
        "rationale": rationale,
        "latency_ms": max(latency, 12),
        "model": "deterministic-zero-cost-v1"
    }
