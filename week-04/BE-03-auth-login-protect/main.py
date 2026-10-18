import os
import time
from fastapi import FastAPI, HTTPException, status, Request, Depends, Response
from fastapi.responses import JSONResponse
import jwt
import uvicorn
from auth import (
    USERS_DB, REVOKED_TOKENS, hash_password, verify_password,
    create_access_token, decode_access_token
)

app = FastAPI(title="Auth & Protected API", version="1.0.0")

# Reusable Auth Dependency (Middleware Pattern)
async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )
        
    token = auth_header.split(" ")[1].strip()
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except (jwt.InvalidTokenError, Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
        
    user_email = payload.get("email")
    user = USERS_DB.get(user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account no longer exists"
        )
        
    return {
        "id": user["id"],
        "email": user["email"],
        "created_at": user["created_at"],
        "token": token
    }

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

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: dict = Depends(get_current_user)):
    REVOKED_TOKENS.add(current_user["token"])
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/public/info")
def get_public_info():
    return {
        "access": "public",
        "message": "This endpoint requires zero authentication. Open to all clients.",
        "timestamp": int(time.time())
    }

@app.get("/protected/profile")
def get_protected_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
        "authenticated": True
    }

@app.get("/protected/settings")
def get_protected_settings(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["id"],
        "notifications": True,
        "mfa_enabled": False,
        "theme": "dark"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
