# BE-03: Auth — Login, Protect & Token Revocation

**Track:** Backend AI Engineering  
**Code:** BE-03  
**Author:** Kunal Aggarwal  
**Framework:** FastAPI / Python 3.13 / Uvicorn  
**Security:** JWT (HMAC-SHA256) + PBKDF2 Password Hashing + HTTPBearer Swagger Padlock  

---

## 1. The Trust Triangle

```
   ┌────────┐          1. POST /auth/login (email + password)         ┌──────────────┐
   │        ├────────────────────────────────────────────────────────►│              │
   │        │◄────────────────────────────────────────────────────────┤  Auth Engine │
   │ Client │          2. Returns JWT Access Token (HS256)            │  (FastAPI)   │
   │        │                                                         └──────────────┘
   │        │          3. GET /protected/profile                      ┌──────────────┐
   │        │             Header: Authorization: Bearer <token>       │ Protected    │
   │        ├────────────────────────────────────────────────────────►│ Dependency   │
   │        │◄────────────────────────────────────────────────────────┤ (Verifies    │
   └────────┘          4. 200 OK + User Metadata                      │ Signature)   │
                          (Or 401 if missing, expired, or revoked)    └──────────────┘
```

---

## 2. API Reference Table

| Method | Endpoint | Description | Auth Required | Status Codes |
|--------|----------|-------------|:-------------:|:------------:|
| `GET` | `/` | Service root and authentication metadata | No | `200 OK` |
| `GET` | `/public/info` | Unprotected informational endpoint | No | `200 OK` |
| `POST` | `/auth/signup` | Register new user with email and salted hash | No | `201 Created` / `400 Bad Request` |
| `POST` | `/auth/login` | Authenticate credentials and receive JWT | No | `200 OK` / `400` / `401 Unauthorized` |
| `POST` | `/auth/logout` | Revoke active access token into denylist | **Yes (Bearer)** | `204 No Content` / `401 Unauthorized` |
| `GET` | `/protected/profile` | Extract user identity from verified JWT | **Yes (Bearer)** | `200 OK` / `401 Unauthorized` |
| `GET` | `/protected/settings` | Auxiliary protected route testing middleware | **Yes (Bearer)** | `200 OK` / `401 Unauthorized` |

---

## 3. Quickstart

### Run the Server
```bash
python main.py
```
*Server boots at `http://127.0.0.1:8000` with Swagger UI at `http://127.0.0.1:8000/docs`.*

### Run the Complete Auth & Security Suite
```bash
python test_api.py
```

---

## 4. Verified cURL Proofs

### Register Account (`POST /auth/signup`)
```bash
curl -i -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "kunal@flyrank.ai", "password": "supersecurepassword123"}'
```
**Response:**
```http
HTTP/1.1 201 Created
content-type: application/json

{"id":1,"email":"kunal@flyrank.ai","message":"User registered successfully"}
```

### Authenticate (`POST /auth/login`)
```bash
curl -i -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "kunal@flyrank.ai", "password": "supersecurepassword123"}'
```
**Response:**
```http
HTTP/1.1 200 OK
content-type: application/json

{"access_token":"eyJhbGciOiJIUzI1NiIsInR5c...","token_type":"bearer","expires_in":3600}
```

### Access Protected Route (`GET /protected/profile`)
```bash
curl -i -X GET http://127.0.0.1:8000/protected/profile \
  -H "Authorization: Bearer <token>"
```
**Response:**
```http
HTTP/1.1 200 OK
content-type: application/json

{"id":1,"email":"kunal@flyrank.ai","created_at":1792293425,"authenticated":true}
```

### Access with Tampered / Missing Token (401 Unauthorized)
```bash
curl -i -X GET http://127.0.0.1:8000/protected/profile \
  -H "Authorization: Bearer invalid_tampered_token"
```
**Response:**
```http
HTTP/1.1 401 Unauthorized
content-type: application/json

{"detail":"Invalid or expired token"}
```

---

## 5. Swagger UI with Bearer Security

FastAPI's OpenAPI generation includes the `HTTPBearer` security scheme:
- Open `http://127.0.0.1:8000/docs`.
- Notice the **Authorize** padlock button at the top right.
- Clicking it prompts for the Bearer token.
- Once pasted, all requests from Swagger automatically inject the `Authorization: Bearer <token>` header, unlocking the protected routes directly in the browser.

---

## 6. Requirements Checklist

- [x] Server boots with one command (`python main.py`).
- [x] Secrets managed via `.env` (gitignored, `.env.example` committed).
- [x] Signup and Login communicate with secure salted password hashing (`pbkdf2_hmac`).
- [x] `/protected/profile` extracts and cryptographically verifies Bearer JWT.
- [x] Correct status codes: 201, 200, 204, 400, 401.
- [x] Auth verification extracted into reusable dependency (`get_current_user`).
- [x] Swagger UI configured with `HTTPBearer` security scheme.
- [x] Public GitHub repo with ≥6 progressive commits and comprehensive test suite.
