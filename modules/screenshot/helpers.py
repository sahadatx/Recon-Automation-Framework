"""
Screenshot Helper Functions

Shared helper functions used by the
Screenshot Capture module.
"""

import hashlib
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import (
    sync_playwright,
)

from config.config import (
    SCREENSHOT_OUTPUT,
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT,
    HEADLESS_BROWSER,
)

from core.logger import (
    debug,
)


# ==========================================================
# Ensure Output Directory
# ==========================================================

def ensure_directory() -> Path:
    """
    Create screenshot output directory.

    Returns:
        Path
    """

    output_dir = Path(
        SCREENSHOT_OUTPUT
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return output_dir


# ==========================================================
# Normalize Filename
# ==========================================================

def normalize_filename(
    url: str,
) -> str:
    """
    Generate a safe screenshot filename.

    Examples
    --------
    https://app.syfe.com/login?id=123

        ↓

    app.syfe.com_a1b2c3d4.png
    """

    parsed = urlparse(
        url
    )

    host = parsed.netloc

    host = host.replace(
        ":",
        "_",
    )

    digest = hashlib.sha1(
        url.encode(
            "utf-8"
        )
    ).hexdigest()[:8]

    return (
        f"{host}_{digest}.png"
    )


# ==========================================================
# Create Browser
# ==========================================================

def create_browser():
    """
    Launch Chromium browser.

    Returns:
        tuple(playwright, browser)
    """

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(

        headless=HEADLESS_BROWSER,

    )

    return (

        playwright,

        browser,

    )


# ==========================================================
# Create Browser Context
# ==========================================================

def create_context(
    browser,
):
    """
    Create browser context.

    Returns:
        BrowserContext
    """

    return browser.new_context(

        viewport={

            "width":
                SCREENSHOT_WIDTH,

            "height":
                SCREENSHOT_HEIGHT,

        },

        ignore_https_errors=True,

    )


# ==========================================================
# Create Page
# ==========================================================

def create_page(
    context,
):
    """
    Create a new page.

    Returns:
        Page
    """

    page = context.new_page()

    page.set_default_navigation_timeout(
        30000
    )

    return page


# ==========================================================
# Show Capture
# ==========================================================

def show_capture(
    url: str,
):
    """
    Display capture information.
    """

    debug(
        f"Capturing {url}"
    )