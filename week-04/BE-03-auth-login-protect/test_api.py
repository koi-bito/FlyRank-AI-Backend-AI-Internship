from unittest.mock import MagicMock
from datetime import datetime
from fastapi.testclient import TestClient
from supabase_auth.errors import AuthApiError
from main import app
from auth import supabase, REVOKED_TOKENS

client = TestClient(app)

def test_full_auth_lifecycle():
    print("=== Testing BE-03 Supabase Auth & Protected Routes Lifecycle ===")
    REVOKED_TOKENS.clear()

    # 1. Public endpoint
    res = client.get("/public/info")
    assert res.status_code == 200
    print("[PASS] GET /public/info -> 200 OK (no auth needed)")

    # Root endpoint metadata verification
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["auth_provider"] == "Supabase Auth"
    print("[PASS] GET / -> 200 OK (auth_provider is 'Supabase Auth')")

    # 2. Protected endpoint without token -> 401
    res = client.get("/protected/profile")
    assert res.status_code == 401
    print(f"[PASS] GET /protected/profile without token -> 401: {res.json()}")

    # 3. Signup validation failures
    res = client.post("/auth/signup", json={"email": "bademail", "password": "123"})
    assert res.status_code == 400
    print(f"[PASS] POST /auth/signup invalid email/pwd -> 400: {res.json()}")

    # 4. Valid Signup -> 201 via Supabase SDK
    mock_user = MagicMock()
    mock_user.id = "sb-user-12345"
    mock_user.email = "kunal@flyrank.ai"
    mock_user.created_at = datetime(2026, 10, 18, 12, 0, 0)

    mock_signup_res = MagicMock()
    mock_signup_res.user = mock_user

    original_sign_up = supabase.auth.sign_up
    original_sign_in = supabase.auth.sign_in_with_password
    original_get_user = supabase.auth.get_user
    original_sign_out = supabase.auth.sign_out

    try:
        supabase.auth.sign_up = MagicMock(return_value=mock_signup_res)
        res = client.post("/auth/signup", json={"email": "kunal@flyrank.ai", "password": "securepassword123"})
        assert res.status_code == 201
        assert res.json()["email"] == "kunal@flyrank.ai"
        assert res.json()["id"] == "sb-user-12345"
        supabase.auth.sign_up.assert_called_once_with({"email": "kunal@flyrank.ai", "password": "securepassword123"})
        print(f"[PASS] POST /auth/signup -> 201 Created (via Supabase SDK): {res.json()}")

        # Duplicate/Error signup -> 400
        supabase.auth.sign_up = MagicMock(side_effect=AuthApiError("User already registered", 400, "user_already_exists"))
        res = client.post("/auth/signup", json={"email": "kunal@flyrank.ai", "password": "securepassword123"})
        assert res.status_code == 400
        print(f"[PASS] POST /auth/signup duplicate error -> 400: {res.json()}")

        # 5. Login wrong password -> 401
        supabase.auth.sign_in_with_password = MagicMock(side_effect=AuthApiError("Invalid login credentials", 400, "invalid_credentials"))
        res = client.post("/auth/login", json={"email": "kunal@flyrank.ai", "password": "wrongpassword"})
        assert res.status_code == 401
        print(f"[PASS] POST /auth/login wrong password -> 401: {res.json()}")

        # 6. Login valid credentials -> 200 + token
        mock_session = MagicMock()
        mock_session.access_token = "supabase-mock-jwt-token-abcdef123456"
        mock_session.token_type = "bearer"
        mock_session.expires_in = 3600
        mock_login_res = MagicMock()
        mock_login_res.session = mock_session

        supabase.auth.sign_in_with_password = MagicMock(return_value=mock_login_res)
        res = client.post("/auth/login", json={"email": "kunal@flyrank.ai", "password": "securepassword123"})
        assert res.status_code == 200
        token = res.json()["access_token"]
        assert token == "supabase-mock-jwt-token-abcdef123456"
        print(f"[PASS] POST /auth/login -> 200 OK (Supabase token issued: {token[:25]}...)")

        # 7. Access protected routes with Bearer token
        mock_user_res = MagicMock()
        mock_user_res.user = mock_user
        supabase.auth.get_user = MagicMock(return_value=mock_user_res)

        headers = {"Authorization": f"Bearer {token}"}
        res = client.get("/protected/profile", headers=headers)
        assert res.status_code == 200
        assert res.json()["email"] == "kunal@flyrank.ai"
        supabase.auth.get_user.assert_called_with(token)
        print(f"[PASS] GET /protected/profile with valid token -> 200 OK: {res.json()}")

        res = client.get("/protected/settings", headers=headers)
        assert res.status_code == 200
        assert res.json()["theme"] == "dark"
        print(f"[PASS] GET /protected/settings with valid token -> 200 OK: {res.json()}")

        # 8. Tampered token -> 401
        supabase.auth.get_user = MagicMock(side_effect=AuthApiError("invalid JWT", 403, "invalid_jwt"))
        tampered_headers = {"Authorization": "Bearer invalid_tampered_token"}
        res = client.get("/protected/profile", headers=tampered_headers)
        assert res.status_code == 401
        print(f"[PASS] GET /protected/profile with tampered token -> 401: {res.json()}")

        # 9. Logout -> 204
        supabase.auth.sign_out = MagicMock()
        supabase.auth.get_user = MagicMock(return_value=mock_user_res)
        res = client.post("/auth/logout", headers=headers)
        assert res.status_code == 204
        supabase.auth.sign_out.assert_called_once()
        print("[PASS] POST /auth/logout -> 204 No Content (Supabase signOut called + token revoked)")

        # 10. Re-attempting access with revoked token -> 401
        res = client.get("/protected/profile", headers=headers)
        assert res.status_code == 401
        print(f"[PASS] GET /protected/profile with revoked token -> 401 Unauthorized: {res.json()}")

    finally:
        supabase.auth.sign_up = original_sign_up
        supabase.auth.sign_in_with_password = original_sign_in
        supabase.auth.get_user = original_get_user
        supabase.auth.sign_out = original_sign_out

    print("\n>>> ALL BE-03 SUPABASE AUTH & SECURITY TESTS PASSED! <<<")

if __name__ == "__main__":
    test_full_auth_lifecycle()
