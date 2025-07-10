"""DNS Resolve queue – fill in the logic."""
import asyncio
import socket
import logging
import time

from saq.queue import Queue
from app.tasks import resolve

queue = Queue.from_url("redis://redis:6379", name="resolve")

# Logger setup
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

WORDLIST = ["www", "mail", "login", "admin", "api"]

async def resolves(hostname: str) -> bool:
    try:
        loop = asyncio.get_running_loop()
        await loop.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
        return True
    except Exception:
        return False

async def resolve_domain(ctx, *, domain: str, wildcard: bool = False):
    logger.info(f"Resolving domain: {domain} | wildcard={wildcard}")

    try:
        if await resolves(domain):
            logger.info(f"Resolved root domain: {domain}")
            await Queue.from_url("redis://redis:6379", name="http_check").enqueue("http_check", domain=domain)

            if wildcard:
                for prefix in WORDLIST:
                    sub = f"{prefix}.{domain}"
                    if await resolves(sub):
                        logger.info(f"Resolved subdomain: {sub}")
                        await Queue.from_url("redis://redis:6379", name="http_check").enqueue("http_check", domain=sub)
                    else:
                        logger.info(f"Subdomain did not resolve: {sub}")
            else:
                logger.info(f"Root domain {domain} did not resolve, retrying in 5 min")
                await queue.enqueue("resolve_domain", domain=domain, wildcard=wildcard, scheduled=time.time() + 5*60)

    except Exception as e:
        logger.error(f"Exception in resolve_domain: {e}")


settings = {
    "queue": queue,
    "functions": [resolve_domain],
}
