import os
import time
from fastapi import FastAPI, HTTPException, status, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn
from supabase_auth.errors import AuthApiError
from auth import supabase, REVOKED_TOKENS

app = FastAPI(
    title="Auth & Protected Routes API",
    description="Supabase Auth service with signup, login, token revocation (logout), and Bearer token security schemes.",
    version="1.0.0"
)

# HTTPBearer security scheme gives Swagger UI the padlock "Authorize" button
security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )
        
    token = credentials.credentials
    if token in REVOKED_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked via logout"
        )
        
    try:
        user_res = supabase.auth.get_user(token)
        if not user_res or not user_res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        user = user_res.user
        created_at_val = user.created_at
        if hasattr(created_at_val, "timestamp"):
            created_at_ts = int(created_at_val.timestamp())
        else:
            created_at_ts = str(created_at_val or int(time.time()))
            
        return {
            "id": str(user.id),
            "email": user.email,
            "created_at": created_at_ts,
            "token": token
        }
    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

@app.get("/", tags=["Public"])
def get_root():
    return {
        "name": "Auth & Protected Routes API",
        "version": "1.0.0",
        "auth_provider": "Supabase Auth",
        "docs": "/docs",
        "status": "ready"
    }

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED, tags=["Auth"])
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
        
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        user = res.user
        user_id = str(user.id) if user and user.id else "user-registered"
        user_email = user.email if user and user.email else email
        return {
            "id": user_id,
            "email": user_email,
            "message": "User registered successfully"
        }
    except AuthApiError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": e.message}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )

@app.post("/auth/login", tags=["Auth"])
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
        
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if not res or not res.session:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid login credentials"}
            )
        session = res.session
        return {
            "access_token": session.access_token,
            "token_type": session.token_type or "bearer",
            "expires_in": session.expires_in or 3600
        }
    except AuthApiError as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": e.message or "Invalid login credentials"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": str(e) or "Invalid login credentials"}
        )

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["Auth"])
def logout(current_user: dict = Depends(get_current_user)):
    token = current_user.get("token")
    if token:
        REVOKED_TOKENS.add(token)
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/public/info", tags=["Public"])
def get_public_info():
    return {
        "access": "public",
        "message": "This endpoint requires zero authentication. Open to all clients.",
        "timestamp": int(time.time())
    }

@app.get("/protected/profile", tags=["Protected"])
def get_protected_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
        "authenticated": True
    }

@app.get("/protected/settings", tags=["Protected"])
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
