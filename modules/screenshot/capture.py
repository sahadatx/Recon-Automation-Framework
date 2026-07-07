"""
Screenshot Capture Engine

Captures screenshots of alive web applications.
"""

from datetime import datetime

from playwright.sync_api import (
    BrowserContext,
    TimeoutError as PlaywrightTimeoutError,
)

from config.config import (
    SCREENSHOT_TIMEOUT,
    SCREENSHOT_FULL_PAGE,
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT,
)

from core.logger import (
    warning,
)

from modules.screenshot.helpers import (
    ensure_directory,
    normalize_filename,
    show_capture,
)


# ==========================================================
# Capture URL
# ==========================================================

def capture_url(
    context: BrowserContext,
    url: str,
):
    """
    Capture screenshot using a shared browser context.

    Args:
        context:
            Shared Playwright BrowserContext.

        url:
            Target URL.

    Returns:
        dict
    """

    output_dir = ensure_directory()

    filename = normalize_filename(
        url
    )

    output_file = (
        output_dir / filename
    )

    show_capture(
        url
    )

    page = None

    try:

        page = context.new_page()

        page.set_default_navigation_timeout(
            SCREENSHOT_TIMEOUT
        )

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=SCREENSHOT_TIMEOUT,
        )

        # Allow JavaScript to finish rendering
        page.wait_for_timeout(
            2000
        )

        page.screenshot(
            path=str(output_file),
            full_page=SCREENSHOT_FULL_PAGE,
        )

        try:

            title = page.title()

        except Exception:

            title = ""

        return {

            "url": url,

            "final_url": page.url,

            "title": title,

            "status": None,

            "screenshot": str(
                output_file
            ),

            "captured": True,

            "timestamp": (
                datetime.utcnow().isoformat()
                + "Z"
            ),

            "width": SCREENSHOT_WIDTH,

            "height": SCREENSHOT_HEIGHT,

        }

    except PlaywrightTimeoutError:

        warning(
            f"Timeout: {url}"
        )

        return {

            "url": url,

            "captured": False,

            "error": "Timeout",

        }

    except Exception as error:

        warning(
            f"{url}: {error}"
        )

        return {

            "url": url,

            "captured": False,

            "error": str(error),

        }

    finally:

        if page:

            try:

                page.close()

            except Exception:

                pass


# ==========================================================
# Capture Host
# ==========================================================

def capture_host(
    context: BrowserContext,
    response: dict,
):
    """
    Capture screenshot using HTTP probe results.

    Args:
        context:
            Shared BrowserContext.

        response:
            HTTP probe result.

    Returns:
        dict
    """

    url = response.get(
        "url"
    )

    if not url:

        return {

            "captured": False,

            "error": "Missing URL",

        }

    metadata = capture_url(
        context,
        url,
    )

    # Merge HTTP probe metadata for future reports
    if metadata.get(
        "captured"
    ):

        metadata["status"] = response.get(
            "status"
        )

        metadata["response_time"] = response.get(
            "response_time"
        )

        metadata["server"] = response.get(
            "server"
        )

        metadata["content_type"] = response.get(
            "content_type"
        )

    return metadata