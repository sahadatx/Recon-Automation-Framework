from __future__ import annotations

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

from core.logger import debug, warning
from modules.screenshots.constants import HEADLESS, SCREENSHOT_HEIGHT, SCREENSHOT_WIDTH


async def start_playwright() -> Playwright:


    debug("Starting Playwright engine...")

    try:

        playwright = await async_playwright().start()

        return playwright

    except Exception as error:

        warning(f"Playwright start failed: {error}")

        raise


async def launch_browser(
    playwright: Playwright,
) -> Browser:


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


async def create_context(
    browser: Browser,
) -> BrowserContext:


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


async def create_page(
    context: BrowserContext,
) -> Page:


    page = await context.new_page()

    return page


async def close_page(
    page: Page | None,
) -> None:


    if page is None:

        return

    try:

        await page.close()

    except Exception as error:

        debug(f"Page close failed: {error}")


async def close_context(
    context: BrowserContext | None,
) -> None:


    if context is None:

        return

    try:

        await context.close()

    except Exception as error:

        debug(f"Context close failed: {error}")


async def close_browser(
    browser: Browser | None,
) -> None:


    if browser is None:

        return

    try:

        await browser.close()

    except Exception as error:

        debug(f"Browser close failed: {error}")


async def stop_playwright(
    playwright: Playwright | None,
) -> None:


    if playwright is None:

        return

    try:

        await playwright.stop()

    except Exception as error:

        debug(f"Playwright stop failed: {error}")


async def cleanup(
    playwright: Playwright | None,
    browser: Browser | None,
) -> None:


    await close_browser(browser)

    await stop_playwright(playwright)


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
