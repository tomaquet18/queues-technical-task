"""HTTP Check queue – fill in the logic."""
import logging
from curl_cffi.requests import get

from saq.queue import Queue
from app.tasks import resolve


# Define Redis queues:
# - 'http_check' handles basic HTTP checks
# - 'browser_capture' will be triggered on success for deeper inspection
queue = Queue.from_url("redis://redis:6379", name="http_check")
browser_capture_queue = Queue.from_url("redis://redis:6379", name="browser_capture")

# Set up logging
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Default headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Upgrade-Insecure-Requests": "1",
}


async def http_check(ctx, *, domain: str, wildcard: bool = False):
    logger.info(f"Running http_check for {domain}")

    try:
        # Attempt to fetch the HTTP version of the domain (port 80)
        response = get(f"http://{domain}", headers=HEADERS, allow_redirects=True, timeout=10)

        # Consider the request successful if status code is 2xx or 3xx
        if 200 <= response.status_code < 400:
            logger.info(f"HTTP check succeeded for {domain} with status {response.status_code}")

            # Enqueue a browser capture task for the domain
            await browser_capture_queue.enqueue("browser_capture", domain=domain)
        else:
            logger.info(f"HTTP check failed for {domain} with status {response.status_code}")

    except Exception as e:
        logger.error(f"Exception during http_check for {domain}: {e}")

settings = {
    "queue": queue,
    "functions": [http_check],
}
