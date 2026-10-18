import sys
from fastapi.testclient import TestClient
from main import app, reset_tasks

client = TestClient(app)

def test_full_crud_cycle():
    print("=== Running BE-01 CRUD Verification Suite ===")
    
    # 0. Reset state
    client.post("/reset")
    
    # 1. Root and Health
    res = client.get("/")
    assert res.status_code == 200
    assert "endpoints" in res.json()
    print("[PASS] GET / -> 200 OK")

    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    print("[PASS] GET /health -> 200 OK")

    # 2. Read endpoints
    res = client.get("/tasks")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) == 3
    print(f"[PASS] GET /tasks -> 200 OK (returned {len(tasks)} tasks)")

    res = client.get("/tasks/1")
    assert res.status_code == 200
    assert res.json()["id"] == 1
    print("[PASS] GET /tasks/1 -> 200 OK")

    res = client.get("/tasks/99")
    assert res.status_code == 404
    assert "error" in res.json()
    print(f"[PASS] GET /tasks/99 -> 404 Not Found: {res.json()}")

    # 3. Create endpoint with validation
    res = client.post("/tasks", json={"title": "Buy oat milk"})
    assert res.status_code == 201
    created = res.json()
    assert created["id"] == 4
    assert created["title"] == "Buy oat milk"
    assert created["done"] is False
    print(f"[PASS] POST /tasks -> 201 Created: {created}")

    # Validation: empty body
    res = client.post("/tasks", json={})
    assert res.status_code == 400
    print(f"[PASS] POST /tasks {{}} -> 400 Bad Request: {res.json()}")

    # Validation: empty title string
    res = client.post("/tasks", json={"title": "   "})
    assert res.status_code == 400
    print(f"[PASS] POST /tasks {{'title': '   '}} -> 400 Bad Request: {res.json()}")

    # 4. Update endpoint
    res = client.put("/tasks/4", json={"title": "Buy organic almond milk", "done": True})
    assert res.status_code == 200
    updated = res.json()
    assert updated["title"] == "Buy organic almond milk"
    assert updated["done"] is True
    print(f"[PASS] PUT /tasks/4 -> 200 OK: {updated}")

    res = client.put("/tasks/99", json={"title": "Ghost task"})
    assert res.status_code == 404
    print(f"[PASS] PUT /tasks/99 -> 404 Not Found: {res.json()}")

    res = client.put("/tasks/4", json={"title": ""})
    assert res.status_code == 400
    print(f"[PASS] PUT /tasks/4 {{'title': ''}} -> 400 Bad Request: {res.json()}")

    # 5. Delete endpoint
    res = client.delete("/tasks/4")
    assert res.status_code == 204
    print("[PASS] DELETE /tasks/4 -> 204 No Content")

    # Confirm deletion
    res = client.get("/tasks/4")
    assert res.status_code == 404
    print("[PASS] GET /tasks/4 after delete -> 404 Not Found")

    res = client.delete("/tasks/99")
    assert res.status_code == 404
    print(f"[PASS] DELETE /tasks/99 -> 404 Not Found: {res.json()}")

    # 6. Extras: Query Filtering & Search
    res = client.get("/tasks?done=true")
    assert res.status_code == 200
    assert all(t["done"] is True for t in res.json())
    print(f"[PASS] GET /tasks?done=true -> 200 OK ({len(res.json())} completed)")

    res = client.get("/tasks?search=SQLite")
    assert res.status_code == 200
    assert len(res.json()) >= 1
    print(f"[PASS] GET /tasks?search=SQLite -> 200 OK ({len(res.json())} matched)")

    # 7. Stats
    res = client.get("/stats")
    assert res.status_code == 200
    print(f"[PASS] GET /stats -> 200 OK: {res.json()}")

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_full_crud_cycle()
