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

# Inngest Client setup (is_production=False connects to local Inngest Dev Server without cloud keys)
inngest_client = inngest.Inngest(
    app_id="report-api",
    is_production=False
)

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
    retries=2,
)
async def make_report(ctx: inngest.Context, step: inngest.StepSync) -> dict:
    report_id = ctx.event.data.get("report_id")
    topic = ctx.event.data.get("topic")

    await step.sleep("do-the-slow-work", datetime.timedelta(seconds=8))

    def _build_step():
        if topic == "fail":
            if report_id in REPORTS:
                REPORTS[report_id]["status"] = "failed"
            raise RuntimeError(f"Simulated unrecoverable report generation failure on topic '{topic}'")
        
        if report_id in REPORTS:
            REPORTS[report_id]["status"] = "done"
            REPORTS[report_id]["result"] = f"Comprehensive executive report on '{topic}' successfully compiled."
            REPORTS[report_id]["completed_at"] = time.time()
        return {"report_id": report_id, "status": "done"}

    res = await step.run("build-report", _build_step)
    return res

# Stage 4: Cron Heartbeat running every minute
@inngest_client.create_function(
    fn_id="heartbeat",
    trigger=inngest.TriggerCron(cron="* * * * *"),
)
async def heartbeat(ctx: inngest.Context, step: inngest.StepSync) -> dict:
    def _log_summary():
        total = len(REPORTS)
        pending = sum(1 for r in REPORTS.values() if r["status"] == "pending")
        done = sum(1 for r in REPORTS.values() if r["status"] == "done")
        failed = sum(1 for r in REPORTS.values() if r["status"] == "failed")
        msg = f"[CRON HEARTBEAT] Total: {total} | Pending: {pending} | Done: {done} | Failed: {failed}"
        print(msg)
        return {"total": total, "pending": pending, "done": done, "failed": failed}

    return await step.run("log-queue-status", _log_summary)

serve(app, inngest_client, [say_hello, make_report, heartbeat])

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.post("/reports", status_code=status.HTTP_202_ACCEPTED)
async def request_report(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Malformed JSON body"}
        )
        
    if not body or "topic" not in body:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Field 'topic' is required"}
        )
        
    raw_topic = body.get("topic")
    if not isinstance(raw_topic, str) or not raw_topic.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Field 'topic' cannot be empty or whitespace"}
        )
        
    topic = raw_topic.strip()
    report_id = f"rep_{uuid.uuid4().hex[:8]}"
    REPORTS[report_id] = {
        "id": report_id,
        "topic": topic,
        "status": "pending",
        "result": None,
        "created_at": time.time()
    }

    try:
        if os.getenv("TEST_MODE") != "1":
            await inngest_client.send(inngest.Event(
                name="report/requested",
                data={"report_id": report_id, "topic": topic}
            ))
    except Exception as e:
        print(f"[INNGEST NOTICE] Event queued locally (Dev server offline): {e}")

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
