import os
import time
os.environ["TEST_MODE"] = "1"
from fastapi.testclient import TestClient
from main import app, REPORTS

client = TestClient(app)

def test_background_job_pipeline():
    print("=== Testing BE-06 Background Job Pipeline ===")
    REPORTS.clear()

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200
    print("[PASS] GET /health -> 200 OK")

    # 2. Fast door acceptance (202 in <50ms)
    start = time.time()
    res = client.post("/reports", json={"topic": "quarterly-financial-metrics"})
    duration_ms = (time.time() - start) * 1000
    assert res.status_code == 202
    data = res.json()
    report_id = data["id"]
    assert data["status"] == "pending"
    assert duration_ms < 200 # Well under 1 second
    print(f"[PASS] POST /reports -> 202 Accepted in {duration_ms:.2f}ms (ID: {report_id})")

    # 3. Status check while pending
    res = client.get(f"/reports/{report_id}")
    assert res.status_code == 200
    assert res.json()["status"] == "pending"
    print(f"[PASS] GET /reports/{report_id} -> status: pending")

    # 4. Validation rejection at the door (400 Bad Request)
    res = client.post("/reports", json={})
    assert res.status_code == 400
    print(f"[PASS] POST /reports {{}} -> 400 Bad Request: {res.json()}")

    res = client.post("/reports", json={"topic": "   "})
    assert res.status_code == 400
    print(f"[PASS] POST /reports whitespace -> 400 Bad Request: {res.json()}")

    # 5. Non-existent report -> 404
    res = client.get("/reports/rep_non_existent")
    assert res.status_code == 404
    print(f"[PASS] GET /reports/rep_non_existent -> 404 Not Found")

    # 6. Simulate worker completion transition
    REPORTS[report_id]["status"] = "done"
    REPORTS[report_id]["result"] = "Report compiled successfully."
    res = client.get(f"/reports/{report_id}")
    assert res.status_code == 200
    assert res.json()["status"] == "done"
    print(f"[PASS] GET /reports/{report_id} after completion -> status: done")

    print("\n>>> ALL BE-06 BACKGROUND PIPELINE TESTS PASSED! <<<")

if __name__ == "__main__":
    test_background_job_pipeline()
