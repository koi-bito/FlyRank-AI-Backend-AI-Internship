import os
import datetime
from fastapi import FastAPI
import uvicorn
import inngest
from inngest.fast_api import serve

app = FastAPI(title="Report Background Jobs API", version="1.0.0")

# Inngest Client setup
inngest_client = inngest.Inngest(app_id="report-api")

@inngest_client.create_function(
    fn_id="say-hello",
    trigger=inngest.TriggerEvent(event="test/hello"),
)
async def say_hello(ctx: inngest.Context, step: inngest.StepSync) -> str:
    # 5s sleep step
    await step.sleep("wait-a-bit", datetime.timedelta(seconds=5))
    return "Hello from the background!"

# Serve Inngest endpoint at /api/inngest
serve(app, inngest_client, [say_hello])

@app.get("/health")
def get_health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
