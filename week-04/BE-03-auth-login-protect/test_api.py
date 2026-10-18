from fastapi.testclient import TestClient
from main import app
from auth import USERS_DB, REVOKED_TOKENS

client = TestClient(app)

def test_full_auth_lifecycle():
    print("=== Testing BE-03 Auth & Protected Routes Lifecycle ===")
    USERS_DB.clear()
    REVOKED_TOKENS.clear()

    # 1. Public endpoint
    res = client.get("/public/info")
    assert res.status_code == 200
    print("[PASS] GET /public/info -> 200 OK (no auth needed)")

    # 2. Protected endpoint without token -> 401
    res = client.get("/protected/profile")
    assert res.status_code == 401
    print(f"[PASS] GET /protected/profile without token -> 401: {res.json()}")

    # 3. Signup validation failures
    res = client.post("/auth/signup", json={"email": "bademail", "password": "123"})
    assert res.status_code == 400
    print(f"[PASS] POST /auth/signup invalid email/pwd -> 400: {res.json()}")

    # 4. Valid Signup -> 201
    res = client.post("/auth/signup", json={"email": "kunal@flyrank.ai", "password": "securepassword123"})
    assert res.status_code == 201
    assert res.json()["email"] == "kunal@flyrank.ai"
    print(f"[PASS] POST /auth/signup -> 201 Created: {res.json()}")

    # Duplicate signup -> 400
    res = client.post("/auth/signup", json={"email": "kunal@flyrank.ai", "password": "securepassword123"})
    assert res.status_code == 400
    print(f"[PASS] POST /auth/signup duplicate email -> 400: {res.json()}")

    # 5. Login wrong password -> 401
    res = client.post("/auth/login", json={"email": "kunal@flyrank.ai", "password": "wrongpassword"})
    assert res.status_code == 401
    print(f"[PASS] POST /auth/login wrong password -> 401: {res.json()}")

    # 6. Login valid credentials -> 200 + token
    res = client.post("/auth/login", json={"email": "kunal@flyrank.ai", "password": "securepassword123"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    assert token is not None
    print(f"[PASS] POST /auth/login -> 200 OK (JWT token issued: {token[:25]}...)")

    # 7. Access protected routes with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/protected/profile", headers=headers)
    assert res.status_code == 200
    assert res.json()["email"] == "kunal@flyrank.ai"
    print(f"[PASS] GET /protected/profile with valid token -> 200 OK: {res.json()}")

    res = client.get("/protected/settings", headers=headers)
    assert res.status_code == 200
    assert res.json()["theme"] == "dark"
    print(f"[PASS] GET /protected/settings with valid token -> 200 OK: {res.json()}")

    # 8. Tampered token -> 401
    tampered_headers = {"Authorization": f"Bearer {token[:-5]}abcde"}
    res = client.get("/protected/profile", headers=tampered_headers)
    assert res.status_code == 401
    print(f"[PASS] GET /protected/profile with tampered token -> 401: {res.json()}")

    # 9. Logout -> 204
    res = client.post("/auth/logout", headers=headers)
    assert res.status_code == 204
    print("[PASS] POST /auth/logout -> 204 No Content (Token revoked)")

    # 10. Re-attempting access with revoked token -> 401
    res = client.get("/protected/profile", headers=headers)
    assert res.status_code == 401
    print(f"[PASS] GET /protected/profile with revoked token -> 401 Unauthorized: {res.json()}")

    print("\n>>> ALL BE-03 AUTH & SECURITY TESTS PASSED! <<<")

if __name__ == "__main__":
    test_full_auth_lifecycle()
