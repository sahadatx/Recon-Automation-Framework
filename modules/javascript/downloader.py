from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.logger import debug, info, warning
from modules.javascript.helpers import (
    download_file,
    is_valid_url,
    safe_filename,
    save_javascript,
)


def download_one(
    context: ExecutionContext,
    url: str,
) -> dict[str, Any] | None:


    if not is_valid_url(
        url,
    ):

        warning(f"Invalid JavaScript URL: {url}")

        return None

    debug(f"Downloading {url}")

    try:

        response = download_file(
            context,
            url,
        )

    except Exception as error:

        warning(f"{url}: {error}")

        return None

    if response is None:

        warning(f"Failed: {url}")

        return None

    try:

        filename = safe_filename(
            url,
        )

        filepath = save_javascript(
            filename,
            response.text,
        )

    except Exception as error:

        warning(f"{url}: {error}")

        return None

    return {
        "url": url,
        "filename": filename,
        "path": str(
            filepath,
        ),
        "status": response.status_code,
        "size": len(
            response.text,
        ),
        "content_type": response.headers.get(
            "Content-Type",
            "",
        ),
    }


def download_multiple(
    context: ExecutionContext,
    urls: list[str],
) -> tuple[
    list[dict[str, Any]],
    list[str],
]:


    info("Downloading JavaScript files...")

    urls = sorted(
        {
            url
            for url in urls
            if is_valid_url(
                url,
            )
        }
    )

    results: list[dict[str, Any]] = []

    failed: list[str] = []

    for url in urls:

        metadata = download_one(
            context,
            url,
        )

        if metadata is None:

            failed.append(
                url,
            )

            continue

        results.append(
            metadata,
        )

    info(f"Downloaded {len(results)} " "JavaScript file(s).")

    if failed:

        warning(f"Failed {len(failed)} " "JavaScript file(s).")

    return (
        results,
        failed,
    )


def download_javascript(
    context: ExecutionContext,
    javascript_urls: list[str],
) -> tuple[
    list[dict[str, Any]],
    list[str],
]:


    return download_multiple(
        context,
        javascript_urls,
    )


__all__ = [
    "download_one",
    "download_multiple",
    "download_javascript",
]
