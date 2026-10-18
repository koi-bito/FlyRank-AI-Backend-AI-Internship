from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_containerized_app_crud():
    print("=== Testing BE-04 Containerized Application API ===")
    
    # Root check
    res = client.get("/")
    assert res.status_code == 200
    print(f"[PASS] GET / -> 200 OK (Engine: {res.json()['engine']})")
    
    # Health check
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    print(f"[PASS] GET /health -> 200 OK: {res.json()}")
    
    # List tasks
    res = client.get("/tasks")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) >= 3
    print(f"[PASS] GET /tasks -> 200 OK ({len(tasks)} tasks returned)")
    
    # Create task
    res = client.post("/tasks", json={"title": "Test containerized stack insertion"})
    assert res.status_code == 201
    created = res.json()
    created_id = created["id"]
    print(f"[PASS] POST /tasks -> 201 Created (ID {created_id}): {created['title']}")
    
    # Validation error check
    res = client.post("/tasks", json={})
    assert res.status_code == 400
    print(f"[PASS] POST /tasks {{}} -> 400 Bad Request: {res.json()}")
    
    # Update task
    res = client.put(f"/tasks/{created_id}", json={"title": "Updated container task", "done": True})
    assert res.status_code == 200
    assert res.json()["done"] is True
    print(f"[PASS] PUT /tasks/{created_id} -> 200 OK: {res.json()['title']}")
    
    # Delete task
    res = client.delete(f"/tasks/{created_id}")
    assert res.status_code == 204
    print(f"[PASS] DELETE /tasks/{created_id} -> 204 No Content")
    
    print("\n>>> ALL BE-04 API TESTS PASSED! <<<")

if __name__ == "__main__":
    test_containerized_app_crud()
