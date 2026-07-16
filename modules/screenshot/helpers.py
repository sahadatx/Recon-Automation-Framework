"""
Screenshot Helper Functions

Production Async Playwright Browser Engine.
"""

from playwright.async_api import (
    async_playwright,
    Playwright,
    Browser,
    BrowserContext,
    Page,
)

from config.config import (
    SCREENSHOT_HEADLESS,
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT,
)

from core.logger import (
    debug,
)


# ==========================================================
# Start Playwright
# ==========================================================

async def start_playwright() -> Playwright:
    """
    Start Playwright engine.

    Returns:
        Playwright
    """

    debug(
        "Starting Playwright..."
    )

    return await async_playwright().start()


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
        Browser
    """

    debug(
        "Launching Chromium..."
    )

    browser = await playwright.chromium.launch(

        headless=SCREENSHOT_HEADLESS,

        args=[

            "--disable-dev-shm-usage",

            "--disable-gpu",

            "--disable-setuid-sandbox",

            "--no-sandbox",

        ],

    )

    return browser


# ==========================================================
# Create Browser Context
# ==========================================================

async def create_context(
    browser: Browser,
) -> BrowserContext:
    """
    Create isolated browser context.

    Args:
        browser:
            Browser instance.

    Returns:
        BrowserContext
    """

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

    return await context.new_page()


# ==========================================================
# Close Page
# ==========================================================

async def close_page(
    page: Page,
):
    """
    Close page.
    """

    try:

        await page.close()

    except Exception:

        pass


# ==========================================================
# Close Context
# ==========================================================

async def close_context(
    context: BrowserContext,
):
    """
    Close browser context.
    """

    try:

        await context.close()

    except Exception:

        pass


# ==========================================================
# Close Browser
# ==========================================================

async def close_browser(
    browser: Browser,
):
    """
    Close browser.
    """

    try:

        await browser.close()

    except Exception:

        pass


# ==========================================================
# Stop Playwright
# ==========================================================

async def stop_playwright(
    playwright: Playwright,
):
    """
    Stop Playwright.
    """

    try:

        await playwright.stop()

    except Exception:

        pass


# ==========================================================
# Cleanup
# ==========================================================

async def cleanup(
    playwright: Playwright,
    browser: Browser,
):
    """
    Cleanup Playwright resources.

    BrowserContext cleanup is handled
    by each capture task individually.
    """

    await close_browser(
        browser
    )

    await stop_playwright(
        playwright
    )