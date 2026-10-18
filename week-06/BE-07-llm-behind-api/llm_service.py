import os
import re
import json
import time
from typing import Dict, Any, Optional
from pydantic import ValidationError
from schema import TriageOutput, STUB_RESPONSE

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

QUARANTINE_FILE = os.path.join(LOGS_DIR, "quarantine.jsonl")
COSTS_FILE = os.path.join(LOGS_DIR, "costs.jsonl")

def load_prompt(version: str = "v1") -> str:
    path = os.path.join(PROMPTS_DIR, f"triage-{version}.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def clean_json_text(text: str) -> str:
    text = text.strip()
    # Strip markdown code blocks if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    # Find JSON bounds
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        return text[start:end+1]
    return text

def log_cost(prompt_version: str, model: str, in_tokens: int, out_tokens: int, duration_ms: float, repaired: bool):
    record = {
        "timestamp": time.time(),
        "prompt_version": prompt_version,
        "model": model,
        "input_tokens": in_tokens,
        "output_tokens": out_tokens,
        "duration_ms": duration_ms,
        "repaired": repaired
    }
    with open(COSTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def log_quarantine(raw_text: str, error_msg: str):
    record = {
        "timestamp": time.time(),
        "raw_text": raw_text,
        "error": error_msg
    }
    with open(QUARANTINE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("LLM_MODEL", "openrouter/free")
        self.prompt_version = "v1"
        self.system_prompt = load_prompt(self.prompt_version)

    def _call_model(self, messages: list, timeout: float = 30.0) -> tuple[str, int, int]:
        from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError
        client = OpenAI(base_url=self.base_url, api_key=self.api_key, timeout=timeout)
        
        # Selective retries on transient network/rate-limit/5xx errors; NEVER retry on 401/400
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=250
                )
                text = response.choices[0].message.content or ""
                in_tok = response.usage.prompt_tokens if response.usage else 0
                out_tok = response.usage.completion_tokens if response.usage else 0
                return text, in_tok, out_tok
            except (RateLimitError, APIConnectionError) as e:
                if attempt == max_retries:
                    raise
                time.sleep(1.0 * (attempt + 1))
            except APIStatusError as e:
                if e.status_code and e.status_code >= 500 and attempt < max_retries:
                    time.sleep(1.0 * (attempt + 1))
                    continue
                raise

    def triage_message(self, user_message: str) -> tuple[Optional[Dict[str, Any]], int, Optional[str]]:
        # 1. Kill Switch Check
        if os.getenv("LLM_ENABLED", "true").lower() == "false":
            return {
                "category": "other",
                "urgency": "low",
                "assigned_team": "support_tier_1",
                "confidence": 0.0,
                "summary": "LLM kill switch active; routed to fallback queue.",
                "requires_escalation": False
            }, 200, None

        # 2. Stub Mode Check
        if os.getenv("LLM_STUB", "1") == "1" or not self.api_key:
            return STUB_RESPONSE, 200, None

        start_time = time.time()
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            raw_text, in_tok, out_tok = self._call_model(messages, timeout=30.0)
        except Exception as e:
            # Handle timeout / downstream failure with clean 504 / 502
            return None, 504, f"Upstream LLM gateway failure: {str(e)}"

        repaired = False
        parsed_json = None
        cleaned = clean_json_text(raw_text)

        try:
            parsed_json = json.loads(cleaned)
            validated = TriageOutput(**parsed_json)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            log_cost(self.prompt_version, self.model, in_tok, out_tok, duration_ms, repaired=False)
            return validated.model_dump(), 200, None
        except (json.JSONDecodeError, ValidationError) as err:
            # REPAIR ONCE, ONLY ONCE
            repaired = True
            repair_messages = list(messages)
            repair_messages.append({"role": "assistant", "content": raw_text})
            repair_messages.append({
                "role": "user",
                "content": f"Your previous response failed validation with error: {str(err)}. Fix the schema and return ONLY valid JSON matching the exact specification."
            })
            try:
                repair_text, r_in, r_out = self._call_model(repair_messages, timeout=15.0)
                cleaned_repair = clean_json_text(repair_text)
                parsed_json = json.loads(cleaned_repair)
                validated = TriageOutput(**parsed_json)
                duration_ms = round((time.time() - start_time) * 1000, 2)
                log_cost(self.prompt_version, self.model, in_tok + r_in, out_tok + r_out, duration_ms, repaired=True)
                return validated.model_dump(), 200, None
            except Exception as repair_err:
                # Persistent failure: clean 422 + quarantine log, NEVER crash
                log_quarantine(raw_text, f"Initial: {err} | Repair: {repair_err}")
                return None, 422, "Model generated unparseable or schema-invalid response that could not be repaired."
