"""Browser Capture queue – fill in the logic."""

import saq

queue = saq.Queue("browser_capture")

@queue.task
def browser_capture(domain: str, wildcard: bool = False):
    """TODO: implement Playwright screenshot capture."""
    pass