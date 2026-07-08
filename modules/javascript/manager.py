"""
JavaScript Manager

Coordinates parallel JavaScript downloads.
"""

import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from config.config import (
    MAX_WORKERS,
)

from core.logger import (
    info,
    success,
    warning,
    progress_status,
)

from modules.javascript.downloader import (
    download_one,
)


# ==========================================================
# Download One
# ==========================================================

def download_single(
    url: str,
):
    """
    Download a single JavaScript file.

    Args:
        url:
            JavaScript URL.

    Returns:
        tuple[str, dict | None]
    """

    result = download_one(
        url
    )

    return (

        url,

        result,

    )


# ==========================================================
# Download All
# ==========================================================

def download_javascript(
    javascript_urls: list[str],
):
    """
    Download all JavaScript files
    in parallel.

    Args:
        javascript_urls:
            List of JavaScript URLs.

    Returns:
        (
            results,
            failed,
            elapsed,
        )
    """

    info(
        "Starting JavaScript Download..."
    )

    # ------------------------------------------------------
    # Remove Duplicates
    # ------------------------------------------------------

    javascript_urls = sorted(
        set(javascript_urls)
    )

    results = {}

    failed = []

    retry_queue = []

    completed = 0

    total = len(
        javascript_urls
    )

    start_time = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {

            executor.submit(
                download_single,
                url,
            ): url

            for url in javascript_urls

        }

        for future in as_completed(
            futures
        ):

            url = futures[
                future
            ]

            completed += 1

            try:

                js_url, metadata = (

                    future.result()

                )

                if metadata:

                    results[
                        js_url
                    ] = metadata

                    progress_status(

                        completed,

                        total,

                        f"✓ {js_url}",

                    )

                else:

                    failed.append(
                        js_url
                    )

                    retry_queue.append(
                        js_url
                    )

                    progress_status(

                        completed,

                        total,

                        f"✗ {js_url}",

                    )

            except Exception as error:

                failed.append(
                    url
                )

                retry_queue.append(
                    url
                )

                warning(
                    f"{url}: {error}"
                )

                progress_status(

                    completed,

                    total,

                    f"✗ {url}",

                )

    # ------------------------------------------------------
    # Retry Queue (Future)
    # ------------------------------------------------------

    if retry_queue:

        info(

            f"Retry Queue: "

            f"{len(retry_queue)} file(s)"

        )

        # Future:
        # Retry failed JavaScript downloads.

    elapsed = round(

        time.perf_counter()

        - start_time,

        2,

    )

    success(

        f"Downloaded : "

        f"{len(results)}"

    )

    success(

        f"Failed      : "

        f"{len(failed)}"

    )

    success(

        f"Elapsed     : "

        f"{elapsed:.2f} sec"

    )

    return (

        results,

        failed,

        elapsed,

    )