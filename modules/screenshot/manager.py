"""
Screenshot Manager

Coordinates parallel screenshot capture.
"""

import time
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from config.config import (
    SCREENSHOT_WORKERS,
)

from core.logger import (
    info,
    success,
    warning,
    progress_status,
)

from modules.screenshot.helpers import (
    create_browser,
    create_context,
)

from modules.screenshot.capture import (
    capture_host,
)


# ==========================================================
# Capture One Host
# ==========================================================

def capture_one(
    context,
    host: str,
    response: dict,
):
    """
    Capture screenshot for one host.

    Returns:
        tuple[str, dict]
    """

    metadata = capture_host(
        context,
        response,
    )

    return (
        host,
        metadata,
    )


# ==========================================================
# Capture All Hosts
# ==========================================================

def capture_hosts(
    http_results: dict,
):
    """
    Capture screenshots for all alive hosts.

    Returns:
        (
            results,
            failed,
            elapsed
        )
    """

    info(
        "Starting Screenshot Capture..."
    )

    results = {}

    failed = []

    retry_queue = []

    completed = 0

    total = len(
        http_results
    )

    start_time = time.perf_counter()

    # ------------------------------------------------------
    # Launch Browser Once
    # ------------------------------------------------------

    playwright, browser = (
        create_browser()
    )

    context = create_context(
        browser
    )

    try:

        with ThreadPoolExecutor(
            max_workers=SCREENSHOT_WORKERS,
        ) as executor:

            futures = {

                executor.submit(
                    capture_one,
                    context,
                    host,
                    response,
                ): host

                for host, response
                in http_results.items()

            }

            for future in as_completed(
                futures
            ):

                host = futures[
                    future
                ]

                completed += 1

                try:

                    hostname, metadata = (
                        future.result()
                    )

                    if metadata.get(
                        "captured",
                        False,
                    ):

                        results[
                            hostname
                        ] = metadata

                        progress_status(
                            completed,
                            total,
                            f"✓ {hostname}",
                        )

                    else:

                        failed.append(
                            hostname
                        )

                        retry_queue.append(
                            hostname
                        )

                        progress_status(
                            completed,
                            total,
                            f"✗ {hostname}",
                        )

                except Exception as error:

                    warning(
                        f"{host}: {error}"
                    )

                    failed.append(
                        host
                    )

                    retry_queue.append(
                        host
                    )

                    progress_status(
                        completed,
                        total,
                        f"✗ {host}",
                    )

    finally:

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        try:

            context.close()

        except Exception:

            pass

        try:

            browser.close()

        except Exception:

            pass

        try:

            playwright.stop()

        except Exception:

            pass

    # ------------------------------------------------------
    # Retry Queue (Future)
    # ------------------------------------------------------

    if retry_queue:

        info(
            f"Retry Queue: "
            f"{len(retry_queue)} host(s)"
        )

        # Future:
        # Retry failed screenshots.

    elapsed = round(
        time.perf_counter()
        - start_time,
        2,
    )

    success(
        f"Screenshots Captured : {len(results)}"
    )

    success(
        f"Failed Captures : {len(failed)}"
    )

    return (
        results,
        failed,
        elapsed,
    )