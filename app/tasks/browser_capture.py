"""Browser Capture queue – fill in the logic."""
import os
import logging
from saq.queue import Queue
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from motor.motor_asyncio import AsyncIOMotorClient
import time

# Register this task to the "browser_capture" queue
queue = Queue.from_url("redis://redis:6379", name="browser_capture")

# Setup MongoDB connection
mongo = AsyncIOMotorClient("mongodb://mongodb:27017")
db = mongo["scanning"]
scans_collection = db["scans"]

# Logger setup
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Directory to store screenshots
EVIDENCE_DIR = "/evidence"
os.makedirs(EVIDENCE_DIR, exist_ok=True)


async def browser_capture(ctx, *, domain: str, wildcard: bool = False):
    logger.info(f"Running browser_capture for {domain}")

    url = f"http://{domain}"
    screenshot_path = os.path.join(EVIDENCE_DIR, f"{domain}.png")

    try:
        # Launch Playwright with Chromium in headless mode
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # Load the URL and wait for the page to fully load (or timeout after 15s)
            await page.goto(url, wait_until="load", timeout=15000)

            # Take a full-page screenshot and save it
            await page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"Screenshot saved: {screenshot_path}")

            # Extract metadata
            final_url = page.url
            title = await page.title()
            scanned_at = int(time.time())

            # Insert scan result into MongoDB
            logger.info(f"Inserting scan result into Mongo for {domain}")
            await scans_collection.insert_one({
                "hostname": domain,
                "screenshot_path": screenshot_path,
                "title": title,
                "final_url": final_url,
                "scanned_at": scanned_at
            })

            await browser.close()

    except PlaywrightTimeoutError:
        logger.error(f"Timeout while loading {url}")
    except Exception as e:
        logger.error(f"Exception in browser_capture for {domain}: {e}")

settings = {
    "queue": queue,
    "functions": [browser_capture],
}
