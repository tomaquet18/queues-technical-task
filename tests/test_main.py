from unittest.mock import patch, AsyncMock

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.anyio
async def test_scan_endpoint_success():
    fake_scan_id = "mocked-scan-id"

    # Patch the queue used in the main app with a mock that returns a fake job
    with patch("app.main.queue") as mock_queue:
        mock_queue.enqueue = AsyncMock(
            return_value=type(
                "Job", (), {"key": fake_scan_id}
            )()  # Simulate returned job with a key
        )

        # Use LifespanManager to properly start and stop the FastAPI app context
        async with LifespanManager(app):
            async with AsyncClient(
                    transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                # Send a POST request to the /scan endpoint with sample data
                response = await ac.post(
                    "/scan", json={"domain": "example.com", "wildcard": True}
                )
                # Assert successful response and correct returned data
                assert response.status_code == 200
                assert response.json() == {"status": "queued", "scan_id": fake_scan_id}
