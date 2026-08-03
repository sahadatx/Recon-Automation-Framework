"""
Screenshot Capture

Production Async Screenshot Engine.
"""

from __future__ import annotations

from pathlib import Path
from time import perf_counter

from playwright.async_api import BrowserContext
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from core.logger import debug, warning
from modules.screenshots.constants import (
    IMAGES_DIR,
    SCREENSHOT_FULL_PAGE,
    SCREENSHOT_TIMEOUT,
)

# ==========================================================
# Ensure Image Directory
# ==========================================================


def ensure_output_directory() -> Path:
    """
    Create screenshot image directory.

    Returns:
        Path
    """

    IMAGES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return IMAGES_DIR


# ==========================================================
# Safe Filename
# ==========================================================


def safe_filename(
    url: str,
) -> str:
    """
    Convert URL into safe filename.

    Returns:
        str
    """

    filename = url

    for char in (
        "https://",
        "http://",
        "/",
        "\\",
        ":",
        "?",
        "&",
        "=",
        "%",
        "#",
    ):

        filename = filename.replace(
            char,
            "_",
        )

    while "__" in filename:

        filename = filename.replace(
            "__",
            "_",
        )

    return filename.strip("_")


# ==========================================================
# Build Screenshot Path
# ==========================================================


def screenshot_path(
    url: str,
) -> Path:
    """
    Generate screenshot path.

    Returns:
        Path
    """

    directory = ensure_output_directory()

    return directory / f"{safe_filename(url)}.png"


# ==========================================================
# Capture One Host
# ==========================================================


async def capture_host(
    context: BrowserContext,
    target: dict,
) -> dict:
    """
    Capture screenshot for one target.

    Args:
        context:
            BrowserContext

        target:
            HTTP probe result

    Returns:
        dict
    """

    url = target.get("url")

    if not url:

        return {
            "captured": False,
            "reason": "Missing URL",
        }

    debug(f"Screenshot: {url}")

    page = None

    output = screenshot_path(url)

    start = perf_counter()

    try:

        page = await context.new_page()

        # --------------------------------------------------
        # Load Page
        # --------------------------------------------------

        response = await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=SCREENSHOT_TIMEOUT,
        )

        await page.wait_for_timeout(1000)

        # --------------------------------------------------
        # Screenshot
        # --------------------------------------------------

        await page.screenshot(
            path=str(output),
            full_page=SCREENSHOT_FULL_PAGE,
        )

        elapsed = round(
            perf_counter() - start,
            2,
        )

        title = await page.title()

        file_size = output.stat().st_size if output.exists() else 0

        return {
            "captured": True,
            "url": url,
            "title": title,
            "path": str(output),
            "status": (response.status if response else target.get("status")),
            "elapsed": elapsed,
            "filesize": file_size,
        }

    except PlaywrightTimeoutError:

        warning(f"{url}: Screenshot timeout")

        return {
            "captured": False,
            "url": url,
            "reason": "Timeout",
        }

    except Exception as error:

        warning(f"{url}: {error}")

        return {
            "captured": False,
            "url": url,
            "reason": str(error),
        }

    finally:

        if page:

            try:

                await page.close()

            except Exception:

                pass


# ==========================================================
# Capture Multiple
# ==========================================================


async def capture_multiple(
    context: BrowserContext,
    targets: list[dict],
) -> list[dict]:
    """
    Capture multiple screenshots.

    Returns:
        list[dict]
    """

    results = []

    for target in targets:

        result = await capture_host(
            context,
            target,
        )

        results.append(result)

    return results


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "ensure_output_directory",
    "safe_filename",
    "screenshot_path",
    "capture_host",
    "capture_multiple",
]
