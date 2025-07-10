"""DNS Resolve queue – fill in the logic."""

from saq.queue import Queue

queue = Queue.from_url("redis://redis:6379")


async def resolve_domain(ctx, *, domain: str, wildcard: bool = False):
    """TODO: implement DNS resolution with optional wildcard fuzzing."""
    pass


settings = {
    "queue": queue,
    "functions": [resolve_domain],
}
