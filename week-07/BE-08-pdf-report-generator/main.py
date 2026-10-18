import os
import uuid
import datetime
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
import uvicorn

from db import init_and_seed_db, get_report_data, get_report_by_date, get_report_by_id, save_report
from pdf_generator import generate_pdf_report

app = FastAPI(title="PDF Report Generator API", version="1.0.0")

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class ReportRequest(BaseModel):
    force: Optional[bool] = False

@app.on_event("startup")
def startup_event():
    init_and_seed_db()

@app.get("/health")
def get_health():
    return {"status": "ok", "service": "pdf-report-generator"}

@app.post("/reports")
def create_report(req: Optional[ReportRequest] = None):
    force = req.force if req else False
    today = datetime.date.today().isoformat()

    # Stage 5 check: if report exists today and not force, return existing (200 OK)
    if not force:
        existing = get_report_by_date(today)
        if existing and os.path.exists(existing["file_path"]):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "id": existing["id"],
                    "file": f"/reports/{existing['id']}/file",
                    "cached": True
                }
            )

    # Generate fresh report
    report_id = f"rep_{uuid.uuid4().hex[:10]}"
    file_path = os.path.join(REPORTS_DIR, f"{report_id}.pdf")

    # 1. Boring SQL Aggregation (Stage 2)
    data = get_report_data()

    # 2. Render from data to multi-page PDF (Stage 3)
    generate_pdf_report(data, file_path)

    # 3. Store path in DB (Stage 4)
    save_report(report_id, today, file_path)

    # 4. Return link
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "id": report_id,
            "file": f"/reports/{report_id}/file",
            "cached": False
        }
    )

@app.get("/reports/{report_id}")
def get_report_metadata(report_id: str):
    rep = get_report_by_id(report_id)
    if not rep:
        raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found")
    return {
        "id": rep["id"],
        "date_key": rep["date_key"],
        "created_at": rep["created_at"],
        "file": f"/reports/{rep['id']}/file"
    }

@app.get("/reports/{report_id}/file")
def get_report_file(report_id: str):
    rep = get_report_by_id(report_id)
    if not rep or not os.path.exists(rep["file_path"]):
        raise HTTPException(status_code=404, detail="Report file not found on disk")
    return FileResponse(
        path=rep["file_path"],
        media_type="application/pdf",
        filename=f"executive-report-{report_id}.pdf"
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
