import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase_auth.errors import AuthApiError

# Load environment variables from .env
load_dotenv()

# In-memory denylist for revoked tokens upon logout
REVOKED_TOKENS = set()

def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL", "").strip()
    if "/rest/v1" in url:
        url = url.split("/rest/v1")[0].rstrip("/")
    key = os.getenv("SUPABASE_KEY", "").strip()

    if not url or not key:
        url = url or "https://placeholder.supabase.co"
        key = key or "placeholder-publishable-key"

    return create_client(url, key)

# Initialize Supabase Client instance with publishable key
supabase: Client = get_supabase_client()
