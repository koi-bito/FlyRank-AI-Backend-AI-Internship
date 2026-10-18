import os
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import inngest.fast_api
import uvicorn

from workflow import (
    inngest_client,
    inngest_decision_flow,
    execute_workflow_sync,
    ExecutionRequest,
    RUN_HISTORY
)
from sample_flows import SAMPLE_FLOWS

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Decision Flow Engine", version="1.0.0")

# Enable CORS for React Flow frontend Vite dev server & production clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "frontend", "dist")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if os.path.exists(os.path.join(FRONTEND_DIST, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

# Mount Inngest endpoint
inngest.fast_api.serve(
    app,
    inngest_client,
    [inngest_decision_flow]
)

@app.get("/")
def get_index():
    dist_index = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(dist_index):
        return FileResponse(dist_index)
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "AI Decision Flow Studio running. Static asset not found."}

@app.get("/health")
def get_health():
    return {"status": "ok", "service": "ai-decision-flow", "inngest": "connected"}

@app.get("/api/sample-flows")
def get_sample_flows():
    return {flow_id: flow.model_dump() for flow_id, flow in SAMPLE_FLOWS.items()}

@app.post("/api/run")
def run_flow_sync(req: ExecutionRequest):
    if not req.graph.nodes:
        raise HTTPException(status_code=400, detail="Graph must contain at least one node")
    result = execute_workflow_sync(req.graph, req.input_context)
    return result

@app.get("/api/runs/{run_id}")
def get_run_status(run_id: str):
    record = RUN_HISTORY.get(run_id)
    if not record:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return record

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
