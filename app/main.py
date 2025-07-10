from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import saq
from saq.queue import Queue

from app.tasks import resolve  # noqa: F401 – imported for side‑effects

app = FastAPI(title="Domain Scanner")
queue = Queue.from_url("redis://redis:6379", name="resolve")

class ScanRequest(BaseModel):
    domain: str
    wildcard: bool = False

@app.post("/scan")
async def scan_domain(req: ScanRequest):
    try:
        await queue.enqueue("resolve_domain", domain=req.domain, wildcard=req.wildcard)
        return {"status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))