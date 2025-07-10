"""HTTP Check queue – fill in the logic."""

from saq.queue import Queue

queue = Queue.from_url("redis://redis:6379")

async def http_check(ctx, *, domain: str, wildcard: bool = False):
    """TODO: implement HTTP request using curl_cffi."""
    pass


settings = {
    "queue": queue,
    "functions": [http_check],
}
