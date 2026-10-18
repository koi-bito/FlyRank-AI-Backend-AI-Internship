import os
import uuid
import time
import datetime
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
import uvicorn
import inngest
from inngest.fast_api import serve

app = FastAPI(title="Report Background Jobs API", version="1.0.0")

# In-memory store for reports
REPORTS: dict[str, dict] = {}

inngest_client = inngest.Inngest(app_id="report-api")

@inngest_client.create_function(
    fn_id="say-hello",
    trigger=inngest.TriggerEvent(event="test/hello"),
)
async def say_hello(ctx: inngest.Context, step: inngest.StepSync) -> str:
    await step.sleep("wait-a-bit", datetime.timedelta(seconds=5))
    return "Hello from the background!"

@inngest_client.create_function(
    fn_id="make-report",
    trigger=inngest.TriggerEvent(event="report/requested"),
)
async def make_report(ctx: inngest.Context, step: inngest.StepSync) -> dict:
    report_id = ctx.event.data.get("report_id")
    topic = ctx.event.data.get("topic")

    # Step 1: Simulate 8-second slow background compute
    await step.sleep("do-the-slow-work", datetime.timedelta(seconds=8))

    # Step 2: Build and store report result
    def _save_done():
        if report_id in REPORTS:
            REPORTS[report_id]["status"] = "done"
            REPORTS[report_id]["result"] = f"Comprehensive executive report on {topic} successfully compiled."
            REPORTS[report_id]["completed_at"] = time.time()
        return {"report_id": report_id, "status": "done"}

    res = await step.run("build-report", _save_done)
    return res

serve(app, inngest_client, [say_hello, make_report])

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.post("/reports", status_code=status.HTTP_202_ACCEPTED)
async def request_report(request: Request):
    body = await request.json()
    topic = body.get("topic")
    
    report_id = f"rep_{uuid.uuid4().hex[:8]}"
    REPORTS[report_id] = {
        "id": report_id,
        "topic": topic,
        "status": "pending",
        "result": None,
        "created_at": time.time()
    }

    # Dispatch Inngest background event
    await inngest_client.send(inngest.Event(
        name="report/requested",
        data={"report_id": report_id, "topic": topic}
    ))

    # Return 202 Accepted immediately
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"id": report_id, "status": "pending"}
    )

@app.get("/reports/{report_id}")
def get_report_status(report_id: str):
    report = REPORTS.get(report_id)
    if not report:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Report {report_id} not found"}
        )
    return report

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
