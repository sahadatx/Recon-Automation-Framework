"""
Screenshot Capture

Production Async Screenshot Engine.
"""

from pathlib import Path
from time import perf_counter

from playwright.async_api import (
    BrowserContext,
    TimeoutError as PlaywrightTimeoutError,
)

from config.config import (
    SCREENSHOT_TIMEOUT,
    SCREENSHOT_FULL_PAGE,
    SCREENSHOT_OUTPUT,
)

from core.logger import (
    debug,
    warning,
)


# ==========================================================
# Ensure Output Directory
# ==========================================================

def ensure_output_directory() -> Path:
    """
    Create screenshot output directory.

    Returns:
        Path
    """

    output = Path(
        SCREENSHOT_OUTPUT
    )

    output.mkdir(

        parents=True,

        exist_ok=True,

    )

    return output


# ==========================================================
# Safe Filename
# ==========================================================

def safe_filename(
    url: str,
) -> str:
    """
    Convert URL into
    filesystem-safe filename.
    """

    invalid = (
        "https://",
        "http://",
        "/",
        ":",
        "?",
        "&",
        "=",
        "%",
        "#",
    )

    filename = url

    for item in invalid:

        filename = filename.replace(

            item,

            "_",

        )

    while "__" in filename:

        filename = filename.replace(

            "__",

            "_",

        )

    return filename.strip("_")


# ==========================================================
# Capture Host
# ==========================================================

async def capture_host(
    context: BrowserContext,
    response: dict,
) -> dict:
    """
    Capture screenshot.

    Args:
        context:
            BrowserContext

        response:
            HTTP probe result

    Returns:
        dict
    """

    url = response.get(
        "url"
    )

    if not url:

        return {

            "captured": False,

            "reason": "Missing URL",

        }

    debug(
        f"Capturing {url}"
    )

    output_dir = ensure_output_directory()

    screenshot_path = (

        output_dir

        /

        (

            safe_filename(url)

            + ".png"

        )

    )

    page = await context.new_page()

    start = perf_counter()

    try:

        # --------------------------------------------------
        # Visit Target
        # --------------------------------------------------

        await page.goto(

            url,

            wait_until="load",

            timeout=SCREENSHOT_TIMEOUT,

        )

        # Give the page a moment to finish rendering
        await page.wait_for_timeout(
            2000
        )

        # --------------------------------------------------
        # Capture Screenshot
        # --------------------------------------------------

        await page.screenshot(

            path=str(
                screenshot_path
            ),

            full_page=SCREENSHOT_FULL_PAGE,

        )

        elapsed = round(

            perf_counter()

            - start,

            2,

        )

        title = await page.title()

        viewport = page.viewport_size

        filesize = 0

        if screenshot_path.exists():

            filesize = (

                screenshot_path.stat()

                .st_size

            )

        return {

            "captured": True,

            "url": url,

            "title": title,

            "path": str(
                screenshot_path
            ),

            "status": response.get(
                "status"
            ),

            "elapsed": elapsed,

            "width": viewport.get(
                "width"
            ) if viewport else None,

            "height": viewport.get(
                "height"
            ) if viewport else None,

            "filesize": filesize,

        }

    except PlaywrightTimeoutError:

        warning(
            f"{url}: Timeout"
        )

        return {

            "captured": False,

            "url": url,

            "reason": "Timeout",

        }

    except Exception as error:

        warning(
            f"{url}: {error}"
        )

        return {

            "captured": False,

            "url": url,

            "reason": str(
                error
            ),

        }

    finally:

        try:

            await page.close()

        except Exception:

            pass