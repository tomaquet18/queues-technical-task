from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import saq
from saq.queue import Queue

from app.tasks import resolve  # noqa: F401 – imported for side‑effects

# Create FastAPI instance
app = FastAPI(title="Domain Scanner")

# Define the Redis-backend queue for domain resolution tasks
queue = Queue.from_url("redis://redis:6379", name="resolve")


# Define the request body model for the /scan endpoint
class ScanRequest(BaseModel):
    domain: str
    wildcard: bool = False

@app.post("/scan")
async def scan_domain(req: ScanRequest):
    try:
        # Enqueue the domain resolution job with the given parameters
        job = await queue.enqueue("resolve_domain", domain=req.domain, wildcard=req.wildcard)
        return {
            "status": "queued",
            "scan_id": job.key
        }
    except Exception as e:
        # Return HTTP 500 if enqueueing fails
        raise HTTPException(status_code=500, detail=str(e))
