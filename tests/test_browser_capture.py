from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.tasks.browser_capture import browser_capture


@pytest.mark.asyncio
async def test_browser_capture_success():
    # Mock the Page object returned by playwright
    page = AsyncMock()
    page.url = "http://example.com"
    page.title = AsyncMock(return_value="Example Domain")
    page.screenshot = AsyncMock()

    # Mock the Browser Context and Browser
    context = AsyncMock()
    context.new_page = AsyncMock(return_value=page)
    browser = AsyncMock()
    browser.new_context = AsyncMock(return_value=context)
    browser.close = AsyncMock()

    # Mock the Playwright chromium launcher
    chromium = AsyncMock()
    chromium.launch = AsyncMock(return_value=browser)

    # Assemble the full mocked playwright object
    playwright = MagicMock()
    playwright.chromium = chromium

    # Mock async context manager for async_playwright
    async_playwright_cm = AsyncMock()
    async_playwright_cm.__aenter__.return_value = playwright
    async_playwright_cm.__aexit__.return_value = AsyncMock()

    # Patch both async_playwright and the DB insert method
    with patch(
            "app.tasks.browser_capture.async_playwright", return_value=async_playwright_cm
    ):
        with patch(
                "app.tasks.browser_capture.scans_collection.insert_one",
                new_callable=AsyncMock,
        ) as mock_insert:
            await browser_capture(None, domain="example.com")
            # Assert that a document was inserted to the database
            assert mock_insert.call_count == 1
