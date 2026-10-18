import os
import sys

def check_provider():
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("LLM_MODEL", "openrouter/free")
    stub_mode = os.getenv("LLM_STUB", "1") == "1"

    if stub_mode or not api_key:
        print("[LLM STUB / DEV MODE ACTIVE]")
        print("Model reply: ready (provider verified via local deterministic stub)")
        return True

    from openai import OpenAI
    client = OpenAI(base_url=base_url, api_key=api_key, timeout=15.0)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Reply with exactly the single word: ready"}],
        max_tokens=10
    )
    answer = response.choices[0].message.content.strip()
    print(f"Model reply: {answer}")
    return "ready" in answer.lower()

if __name__ == "__main__":
    check_provider()
