"""HTTP Check queue – fill in the logic."""

import saq

queue = saq.Queue("http_check")

@queue.task
def http_check(domain: str, wildcard: bool = False):
    """TODO: implement HTTP request using curl_cffi."""
    pass