import os
import pytest
from fastapi.testclient import TestClient
from main import app
from db import init_and_seed_db

client = TestClient(app)

def setup_module():
    init_and_seed_db()

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_stage_4_generate_and_download_flow():
    # 1. POST /reports (initial generation)
    res = client.post("/reports", json={"force": True})
    assert res.status_code == 201
    payload = res.json()
    assert "id" in payload
    report_id = payload["id"]
    assert payload["file"] == f"/reports/{report_id}/file"
    assert payload["cached"] is False

    # 2. GET /reports/:id (metadata query)
    meta_res = client.get(f"/reports/{report_id}")
    assert meta_res.status_code == 200
    meta = meta_res.json()
    assert meta["id"] == report_id
    assert "date_key" in meta

    # 3. GET /reports/:id/file (file download stream)
    file_res = client.get(f"/reports/{report_id}/file")
    assert file_res.status_code == 200
    assert file_res.headers["content-type"] == "application/pdf"
    assert len(file_res.content) > 5000, "PDF payload must be substantial and multi-page"

    # 4. Unknown id 404 check
    err_res = client.get("/reports/rep_nonexistent123")
    assert err_res.status_code == 404
    err_file_res = client.get("/reports/rep_nonexistent123/file")
    assert err_file_res.status_code == 404

def test_stage_5_idempotent_caching_and_force():
    # 1. First normal request
    res1 = client.post("/reports")
    id1 = res1.json()["id"]

    # 2. Immediate duplicate request without force -> returns 200 OK + same ID
    res2 = client.post("/reports")
    assert res2.status_code == 200
    assert res2.json()["cached"] is True
    assert res2.json()["id"] == id1

    # 3. Third request with force: true -> returns 201 Created + new ID
    res3 = client.post("/reports", json={"force": True})
    assert res3.status_code == 201
    assert res3.json()["cached"] is False
    assert res3.json()["id"] != id1

if __name__ == "__main__":
    test_health()
    test_stage_4_generate_and_download_flow()
    test_stage_5_idempotent_caching_and_force()
    print("All BE-08 API Tests Passed Successfully!")
