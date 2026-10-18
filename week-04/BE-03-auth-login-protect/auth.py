import os
import hashlib
import hmac
import time
import jwt
from typing import Optional, Dict, Any

JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-flyrank-jwt-key-2026")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_SECONDS = 3600 # 1 hour

# In-memory user store: email -> {id, email, password_hash, salt, created_at}
USERS_DB: Dict[str, Dict[str, Any]] = {}
REVOKED_TOKENS = set()

def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return pwd_hash, salt

def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    pwd_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(pwd_hash, expected_hash)

def create_access_token(user_id: int, email: str) -> str:
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": now + JWT_EXPIRATION_SECONDS
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> Dict[str, Any]:
    if token in REVOKED_TOKENS:
        raise jwt.InvalidTokenError("Token has been revoked via logout")
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
