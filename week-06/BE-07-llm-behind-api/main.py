import os
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
import uvicorn
from schema import TriageInput, TriageOutput
from llm_service import LLMService

app = FastAPI(
    title="Customer Message Triage LLM API",
    description="Defensive API boundary wrapping an LLM for structured message classification, urgency routing, and automated schema repair.",
    version="1.0.0"
)

llm_service = LLMService()

@app.get("/", tags=["General"])
def get_root():
    return {
        "name": "Customer Message Triage LLM API",
        "version": "1.0.0",
        "endpoint": "/llm/triage",
        "llm_enabled": os.getenv("LLM_ENABLED", "true").lower() == "true",
        "stub_mode": os.getenv("LLM_STUB", "1") == "1",
        "docs": "/docs"
    }

@app.get("/health", tags=["General"])
def get_health():
    return {"status": "ok", "llm_gateway": "operational"}

@app.post("/llm/triage", response_model=TriageOutput, tags=["Triage"])
async def triage_message(request: Request):
    # 1. Boundary Input Validation (before model is ever touched)
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

    # 2. Call LLM Service with Timeout, Retries, Validation, Repair, and Quarantine
    result, status_code, err_msg = llm_service.triage_message(message)
    
    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={"error": err_msg}
        )
        
    return result

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
