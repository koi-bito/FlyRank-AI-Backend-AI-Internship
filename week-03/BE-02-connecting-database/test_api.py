from fastapi.testclient import TestClient
from main import app
from db import init_db

client = TestClient(app)

def test_sqlite_persistence_and_crud():
    print("=== Testing BE-02 SQLite CRUD and Persistence ===")
    
    # 1. Health
    res = client.get("/health")
    assert res.status_code == 200
    print("[PASS] GET /health -> 200 OK")

    # 2. Read tasks from database
    res = client.get("/tasks")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) >= 3
    print(f"[PASS] GET /tasks -> 200 OK (found {len(tasks)} persisted rows)")

    # 3. Create task in DB
    res = client.post("/tasks", json={"title": "Test SQLite insertion persistence"})
    assert res.status_code == 201
    created = res.json()
    created_id = created["id"]
    print(f"[PASS] POST /tasks -> 201 Created (ID {created_id}): {created['title']}")

    # Validation: empty body
    res = client.post("/tasks", json={})
    assert res.status_code == 400
    print(f"[PASS] POST /tasks {{}} -> 400 Bad Request: {res.json()}")

    # 4. Read back created task from DB
    res = client.get(f"/tasks/{created_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Test SQLite insertion persistence"
    print(f"[PASS] GET /tasks/{created_id} -> 200 OK (confirmed stored in SQLite)")

    # 5. Update task in DB
    res = client.put(f"/tasks/{created_id}", json={"title": "Updated persistence title", "done": True})
    assert res.status_code == 200
    assert res.json()["done"] is True
    print(f"[PASS] PUT /tasks/{created_id} -> 200 OK (status updated in SQLite)")

    # 6. Delete task from DB
    res = client.delete(f"/tasks/{created_id}")
    assert res.status_code == 204
    print(f"[PASS] DELETE /tasks/{created_id} -> 204 No Content")

    # Verify 404 after deletion
    res = client.get(f"/tasks/{created_id}")
    assert res.status_code == 404
    print(f"[PASS] GET /tasks/{created_id} after deletion -> 404 Not Found")

    print("\n>>> ALL BE-02 SQLITE TESTS PASSED! <<<")

if __name__ == "__main__":
    test_sqlite_persistence_and_crud()
