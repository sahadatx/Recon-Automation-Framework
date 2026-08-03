"""
Screenshot Helper Functions

Production Async Playwright Browser Engine.
"""

from __future__ import annotations

from playwright.async_api import (
    async_playwright,
    Playwright,
    Browser,
    BrowserContext,
    Page,
)

from modules.screenshots.constants import (
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT,
    HEADLESS,
)

from core.logger import (
    debug,
    warning,
)

# ==========================================================
# Start Playwright
# ==========================================================


async def start_playwright() -> Playwright:
    """
    Initialize Playwright engine.

    Returns:
        Playwright instance
    """

    debug("Starting Playwright engine...")

    try:

        playwright = await async_playwright().start()

        return playwright

    except Exception as error:

        warning(f"Playwright start failed: {error}")

        raise


# ==========================================================
# Launch Browser
# ==========================================================


async def launch_browser(
    playwright: Playwright,
) -> Browser:
    """
    Launch Chromium browser.

    Args:
        playwright:
            Playwright instance.

    Returns:
        Browser instance
    """

    debug("Launching Chromium browser...")

    try:

        browser = await playwright.chromium.launch(
            headless=HEADLESS,
            args=[
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ],
        )

        return browser

    except Exception as error:

        warning(f"Browser launch failed: {error}")

        raise


# ==========================================================
# Create Context
# ==========================================================


async def create_context(
    browser: Browser,
) -> BrowserContext:
    """
    Create isolated browser context.

    Returns:
        BrowserContext
    """

    debug("Creating browser context...")

    context = await browser.new_context(
        viewport={
            "width": SCREENSHOT_WIDTH,
            "height": SCREENSHOT_HEIGHT,
        },
        ignore_https_errors=True,
        java_script_enabled=True,
    )

    return context


# ==========================================================
# Create Page
# ==========================================================


async def create_page(
    context: BrowserContext,
) -> Page:
    """
    Create browser page.

    Returns:
        Page
    """

    page = await context.new_page()

    return page


# ==========================================================
# Close Page
# ==========================================================


async def close_page(
    page: Page | None,
) -> None:
    """
    Close browser page.
    """

    if page is None:

        return

    try:

        await page.close()

    except Exception as error:

        debug(f"Page close failed: {error}")


# ==========================================================
# Close Context
# ==========================================================


async def close_context(
    context: BrowserContext | None,
) -> None:
    """
    Close browser context.
    """

    if context is None:

        return

    try:

        await context.close()

    except Exception as error:

        debug(f"Context close failed: {error}")


# ==========================================================
# Close Browser
# ==========================================================


async def close_browser(
    browser: Browser | None,
) -> None:
    """
    Close browser instance.
    """

    if browser is None:

        return

    try:

        await browser.close()

    except Exception as error:

        debug(f"Browser close failed: {error}")


# ==========================================================
# Stop Playwright
# ==========================================================


async def stop_playwright(
    playwright: Playwright | None,
) -> None:
    """
    Stop Playwright engine.
    """

    if playwright is None:

        return

    try:

        await playwright.stop()

    except Exception as error:

        debug(f"Playwright stop failed: {error}")


# ==========================================================
# Cleanup
# ==========================================================


async def cleanup(
    playwright: Playwright | None,
    browser: Browser | None,
) -> None:
    """
    Cleanup Playwright resources.

    Context and page cleanup should
    happen inside capture workflow.
    """

    await close_browser(browser)

    await stop_playwright(playwright)


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "start_playwright",
    "launch_browser",
    "create_context",
    "create_page",
    "close_page",
    "close_context",
    "close_browser",
    "stop_playwright",
    "cleanup",
]
