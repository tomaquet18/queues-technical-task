import pytest

from app.tasks.resolve import resolves


@pytest.mark.asyncio
async def test_resolves_success():
    # A known resolvable domain should return True
    assert await resolves("examples.com") is True


@pytest.mark.asyncio
async def test_resolves_failure():
    # A non-existent domain should return False
    assert await resolves("nonexistent.subdomain.random") is False
