from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import saq

from app.tasks import resolve  # noqa: F401 – imported for side‑effects

app = FastAPI(title="Domain Scanner")

class ScanRequest(BaseModel):
    domain: str
    wildcard: bool = False

@app.post("/scan")
async def scan_domain(req: ScanRequest):
    try:
        saq.enqueue("resolve", req.domain, req.wildcard)
        return {"status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))