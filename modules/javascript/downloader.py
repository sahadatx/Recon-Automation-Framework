"""
JavaScript Downloader

Downloads JavaScript files discovered
by the URL Discovery module.
"""

from modules.javascript.helpers import (

    download_file,

    safe_filename,

    save_javascript,

    is_valid_url,

)

from core.logger import (

    debug,

    info,

    warning,

)


# ==========================================================
# Download One JavaScript File
# ==========================================================

def download_one(
    url: str,
):
    """
    Download one JavaScript file.

    Returns:
        dict | None
    """

    if not is_valid_url(

        url

    ):

        warning(

            f"Invalid JavaScript URL: {url}"

        )

        return None

    debug(

        f"Downloading {url}"

    )

    try:

        response = download_file(

            url

        )

    except Exception as error:

        warning(

            f"{url}: {error}"

        )

        return None

    if response is None:

        warning(

            f"Failed: {url}"

        )

        return None

    try:

        filename = safe_filename(

            url

        )

        filepath = save_javascript(

            filename,

            response.text,

        )

    except Exception as error:

        warning(

            f"{url}: {error}"

        )

        return None

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
    Download multiple
    JavaScript files.

    Returns:
        tuple(
            results,
            failed,
        )
    """

    info(

        "Downloading JavaScript files..."

    )

    urls = sorted({

        url

        for url in urls

        if is_valid_url(

            url

        )

    })

    results = []

    failed = []

    for url in urls:

        metadata = download_one(

            url

        )

        if metadata is None:

            failed.append(

                url

            )

            continue

        results.append(

            metadata

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
# Entry Point
# ==========================================================

def download_javascript(
    javascript_urls: list[str],
):
    """
    JavaScript downloader
    entry point.
    """

    return download_multiple(

        javascript_urls

    )