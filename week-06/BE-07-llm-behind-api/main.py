import os
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
import uvicorn
from schema import TriageInput, TriageOutput, STUB_RESPONSE

app = FastAPI(title="LLM Triage API", version="1.0.0")

@app.get("/")
def get_root():
    return {
        "name": "LLM Triage API",
        "version": "1.0.0",
        "endpoint": "/llm/triage",
        "stub_mode": os.getenv("LLM_STUB", "1") == "1",
        "status": "ready"
    }

@app.post("/llm/triage", response_model=TriageOutput)
async def triage_message(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Malformed JSON body in request"}
        )
        
    if not body or "message" not in body:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Missing required field: 'message'"}
        )
        
    raw_message = body.get("message")
    if not isinstance(raw_message, str):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Field 'message' must be a string"}
        )
        
    message = raw_message.strip()
    if not message:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Field 'message' cannot be empty or whitespace"}
        )
    if len(message) > 2000:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Field 'message' exceeds maximum allowed length of 2000 characters"}
        )

    # Stub mode check
    if os.getenv("LLM_STUB", "1") == "1":
        return STUB_RESPONSE

    # Real LLM call will be wired in Stage 2
    return STUB_RESPONSE

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
