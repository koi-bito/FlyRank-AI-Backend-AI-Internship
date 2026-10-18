import os
from fastapi import FastAPI
import uvicorn
from auth import JWT_SECRET

app = FastAPI(title="Auth & Protected API", version="1.0.0")

@app.get("/")
def get_root():
    return {
        "name": "Auth & Protected Routes API",
        "version": "1.0.0",
        "auth_provider": "JWT Bearer",
        "status": "ready"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
