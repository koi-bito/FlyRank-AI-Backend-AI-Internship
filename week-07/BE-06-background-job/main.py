import os
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Report Background Jobs API", version="1.0.0")

@app.get("/health")
def get_health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
