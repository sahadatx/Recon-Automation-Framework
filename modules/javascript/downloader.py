"""
JavaScript Downloader

Downloads JavaScript files discovered
by the URL Discovery module.
"""

from core.logger import (
    debug,
    info,
    warning,
)

from modules.javascript.helpers import (
    download_file,
    safe_filename,
    save_javascript,
)


# ==========================================================
# Download One JavaScript File
# ==========================================================

def download_one(
    url: str,
):
    """
    Download a single JavaScript file.

    Args:
        url:
            JavaScript URL.

    Returns:
        dict | None
    """

    debug(
        f"Downloading {url}"
    )

    response = download_file(
        url
    )

    if response is None:

        warning(
            f"Failed: {url}"
        )

        return None

    filename = safe_filename(
        url
    )

    filepath = save_javascript(

        filename,

        response.text,

    )

    return {

        "url": url,

        "filename": filename,

        "path": str(
            filepath
        ),

        "status": response.status_code,

        "size": len(
            response.text
        ),

        "content_type": response.headers.get(
            "Content-Type",
            "",
        ),

    }


# ==========================================================
# Download Multiple JavaScript Files
# ==========================================================

def download_multiple(
    urls: list[str],
):
    """
    Download multiple JavaScript files.

    Args:
        urls:
            List of JavaScript URLs.

    Returns:
        tuple(
            results,
            failed,
        )
    """

    info(
        "Downloading JavaScript files..."
    )

    results = []

    failed = []

    # ------------------------------------------
    # Remove Duplicates
    # ------------------------------------------

    urls = sorted(
        set(urls)
    )

    for url in urls:

        metadata = download_one(
            url
        )

        if metadata:

            results.append(
                metadata
            )

        else:

            failed.append(
                url
            )

    info(

        f"Downloaded "

        f"{len(results)} "

        f"JavaScript file(s)."

    )

    if failed:

        warning(

            f"Failed "

            f"{len(failed)} "

            f"JavaScript file(s)."

        )

    return (

        results,

        failed,

    )


# ==========================================================
# Download JavaScript
# ==========================================================

def download_javascript(
    javascript_urls: list[str],
):
    """
    Entry point for downloading
    JavaScript files.

    Args:
        javascript_urls:
            List of discovered JS URLs.

    Returns:
        tuple(
            results,
            failed,
        )
    """

    return download_multiple(
        javascript_urls
    )