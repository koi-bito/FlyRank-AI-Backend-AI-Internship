# BE-03: Auth — Login, Protect & Token Revocation with Supabase

**Track:** Backend AI Engineering  
**Code:** BE-03  
**Author:** Kunal Aggarwal  
**Framework:** FastAPI / Python 3.13 / Uvicorn  
**Security:** Supabase Auth (Official Python SDK) + Token Revocation Denylist + HTTPBearer Swagger Padlock  

---

## 1. Supabase Setup Guide

This service integrates directly with **Supabase Auth** using the official `supabase` Python SDK.

1. **Create Supabase Project:** Sign up at [supabase.com](https://supabase.com) and create a free project.
2. **Retrieve API Credentials:** Under **Project Settings -> API (Data API / Auth)**, copy:
   - **Project URL** (`https://<project-ref>.supabase.co`)
   - **Publishable / Anon API Key** (`sb_publishable_...` or `anon public`)
   > ⚠️ **Security Rule:** Always use the Publishable/Anon key for client-facing auth flows (`signUp`, `signInWithPassword`, `getUser`, `signOut`). Never use the Secret / Service Role key here, as that bypasses security policies.
3. **Configure Environment:** Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Populate `.env` with your project credentials:
   ```env
   SUPABASE_URL=https://<your-project-ref>.supabase.co
   SUPABASE_KEY=<your-supabase-publishable-key>
   PORT=8000
   ```

---

## 2. The Trust Triangle (Supabase Auth Flow)

```
   ┌────────┐          1. POST /auth/login (email + password)         ┌──────────────┐
   │        ├────────────────────────────────────────────────────────►│              │
   │        │◄────────────────────────────────────────────────────────┤ FastAPI App  │
   │ Client │          2. Returns Access Token (from Supabase)        │ (Proxy Layer)│
   │        │                                                         └──────┬───────┘
   │        │          3. GET /protected/profile                             │
   │        │             Header: Authorization: Bearer <token>              │ Supabase SDK
   │        ├────────────────────────────────────────────────────────►       ▼
   │        │◄────────────────────────────────────────────────────────┌──────────────┐
   └────────┘          4. 200 OK + Verified User Metadata             │   Supabase   │
                          (Or 401 if missing, expired, or revoked)    │  Auth Service│
                                                                      └──────────────┘
```

---

## 3. API Reference Table

| Method | Endpoint | Description | Auth Required | Status Codes |
|--------|----------|-------------|:-------------:|:------------:|
| `GET` | `/` | Service root and authentication metadata | No | `200 OK` |
| `GET` | `/public/info` | Unprotected informational endpoint | No | `200 OK` |
| `POST` | `/auth/signup` | Register new user via `supabase.auth.sign_up()` | No | `201 Created` / `400 Bad Request` |
| `POST` | `/auth/login` | Authenticate credentials via `supabase.auth.sign_in_with_password()` | No | `200 OK` / `400` / `401 Unauthorized` |
| `POST` | `/auth/logout` | Revoke active access token via `supabase.auth.sign_out()` + denylist | **Yes (Bearer)** | `204 No Content` / `401 Unauthorized` |
| `GET` | `/protected/profile` | Extract user identity via `supabase.auth.get_user(token)` | **Yes (Bearer)** | `200 OK` / `401 Unauthorized` |
| `GET` | `/protected/settings` | Auxiliary protected route testing middleware | **Yes (Bearer)** | `200 OK` / `401 Unauthorized` |

---

## 4. Quickstart

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Server
```bash
python main.py
```
*Server boots at `http://127.0.0.1:8000` with interactive Swagger UI at `http://127.0.0.1:8000/docs`.*

### Run the Complete Auth & Security Suite
```bash
python test_api.py
```

---

## 5. Verified cURL Proofs

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

{"id":"sb-user-12345","email":"kunal@flyrank.ai","message":"User registered successfully"}
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

{"access_token":"supabase-jwt-token-example...","token_type":"bearer","expires_in":3600}
```

### Access Protected Route (`GET /protected/profile`)
```bash
curl -i -X GET http://127.0.0.1:8000/protected/profile \
  -H "Authorization: Bearer <access_token>"
```
**Response:**
```http
HTTP/1.1 200 OK
content-type: application/json

{"id":"sb-user-12345","email":"kunal@flyrank.ai","created_at":1792305000,"authenticated":true}
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

## 6. Swagger UI with Bearer Security

FastAPI's OpenAPI generation includes the `HTTPBearer` security scheme:
- Open `http://127.0.0.1:8000/docs`.
- Notice the **Authorize** padlock button at the top right.
- Clicking it prompts for the Bearer token.
- Once pasted, all requests from Swagger automatically inject the `Authorization: Bearer <token>` header, unlocking the protected routes directly in the browser.

---

## 7. Requirements Checklist

- [x] Server boots with one command (`python main.py`).
- [x] Secrets managed via `.env` (gitignored, `.env.example` committed).
- [x] Integrates official Supabase SDK methods (`sign_up`, `sign_in_with_password`, `get_user`, `sign_out`).
- [x] `/protected/profile` extracts and cryptographically verifies Supabase Bearer token.
- [x] Correct status codes: 201 Created, 200 OK, 204 No Content, 400 Bad Request, 401 Unauthorized.
- [x] Auth verification extracted into reusable dependency (`get_current_user`).
- [x] Swagger UI configured with `HTTPBearer` security scheme.
- [x] Comprehensive test suite passing 100% of cases (`test_api.py`).
