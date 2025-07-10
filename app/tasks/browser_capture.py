"""Browser Capture queue – fill in the logic."""

from saq.queue import Queue

queue = Queue.from_url("redis://redis:6379")

async def browser_capture(ctx, *, domain: str, wildcard: bool = False):
    """TODO: implement Playwright screenshot capture."""
    pass


settings = {
    "queue": queue,
    "functions": [browser_capture],
}
