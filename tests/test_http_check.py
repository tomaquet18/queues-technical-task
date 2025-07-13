from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.tasks.http_check import http_check


@pytest.mark.asyncio
async def test_http_check_success():
    # Simulate a successful HTTP GET response
    mock_get = MagicMock()
    mock_get.return_value.status_code = 200

    # Patch the get function and mock the browser_capture_queue
    with patch("app.tasks.http_check.get", mock_get):
        with patch(
                "app.tasks.http_check.browser_capture_queue.enqueue", new_callable=AsyncMock
        ) as mock_enqueue:
            await http_check(None, domain="example.com")
            # Assert that the browser_capture task is enqueued correctly
            mock_enqueue.assert_called_once_with(
                "browser_capture", domain="example.com"
            )
