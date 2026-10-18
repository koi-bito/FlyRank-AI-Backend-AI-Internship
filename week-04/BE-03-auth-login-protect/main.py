import os
import time
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
import uvicorn
from auth import (
    USERS_DB, hash_password, verify_password, create_access_token
)

app = FastAPI(title="Auth & Protected API", version="1.0.0")

@app.get("/")
def get_root():
    return {
        "name": "Auth & Protected Routes API",
        "version": "1.0.0",
        "auth_provider": "JWT Bearer",
        "status": "ready"
    }

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def signup(payload: dict):
    if not payload:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Request body cannot be empty"}
        )
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", "")).strip()
    
    if not email or "@" not in email:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "A valid email is required"}
        )
    if not password or len(password) < 6:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Password is required and must be at least 6 characters"}
        )
        
    if email in USERS_DB:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "User with this email already exists"}
        )
        
    pwd_hash, salt = hash_password(password)
    user_id = len(USERS_DB) + 1
    new_user = {
        "id": user_id,
        "email": email,
        "password_hash": pwd_hash,
        "salt": salt,
        "created_at": int(time.time())
    }
    USERS_DB[email] = new_user
    
    return {
        "id": user_id,
        "email": email,
        "message": "User registered successfully"
    }

@app.post("/auth/login")
async def login(payload: dict):
    if not payload:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Request body cannot be empty"}
        )
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", "")).strip()
    
    if not email or not password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Email and password are required"}
        )
        
    user = USERS_DB.get(email)
    if not user or not verify_password(password, user["salt"], user["password_hash"]):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid login credentials"}
        )
        
    token = create_access_token(user["id"], user["email"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600
    }

@app.get("/public/info")
def get_public_info():
    return {
        "access": "public",
        "message": "This endpoint requires zero authentication. Open to all clients.",
        "timestamp": int(time.time())
    }

@app.get("/protected/profile")
def get_protected_profile(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Access token required"}
        )
    # Stage 2: gate check present, token not yet cryptographically verified
    return {
        "access": "protected",
        "header_received": auth_header[:15] + "..."
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
