"""
Screenshot Manager

Production Async Screenshot Manager.
"""

import asyncio
import time

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
    start_playwright,
    launch_browser,
    create_context,
    close_context,
    cleanup,
)

from modules.screenshot.capture import (
    capture_host,
)


# ==========================================================
# Capture One Host
# ==========================================================

async def capture_one(
    semaphore,
    browser,
    host: str,
    response: dict,
):
    """
    Capture one host.

    Each task gets its own
    BrowserContext.
    """

    async with semaphore:

        context = await create_context(
            browser
        )

        try:

            metadata = await capture_host(
                context,
                response,
            )

            return (

                host,

                metadata,

            )

        finally:

            await close_context(
                context
            )


# ==========================================================
# Capture Hosts
# ==========================================================

async def capture_hosts(
    http_results: dict,
):
    """
    Capture screenshots.

    Returns:
        (
            results,
            failed,
            elapsed,
        )
    """

    info(
        "Starting Screenshot Capture..."
    )

    start_time = time.perf_counter()

    semaphore = asyncio.Semaphore(
        SCREENSHOT_WORKERS
    )

    results = {}

    failed = []

    completed = 0

    total = len(
        http_results
    )

    playwright = await start_playwright()

    browser = await launch_browser(
        playwright
    )

    try:

        tasks = [

            capture_one(

                semaphore,

                browser,

                host,

                response,

            )

            for host, response

            in http_results.items()

        ]

        for task in asyncio.as_completed(
            tasks
        ):

            completed += 1

            try:

                host, metadata = await task

                if metadata.get(
                    "captured",
                    False,
                ):

                    results[
                        host
                    ] = metadata

                    progress_status(

                        completed,

                        total,

                        f"✓ {host}",

                    )

                else:

                    failed.append(
                        host
                    )

                    progress_status(

                        completed,

                        total,

                        f"✗ {host}",

                    )

            except Exception as error:

                warning(
                    str(error)
                )

    finally:

        await cleanup(

            playwright,

            browser,

        )

    elapsed = round(

        time.perf_counter()

        - start_time,

        2,

    )

    success(
        f"Screenshots : {len(results)}"
    )

    success(
        f"Failed : {len(failed)}"
    )

    success(
        f"Elapsed : {elapsed:.2f} sec"
    )

    return (

        results,

        failed,

        elapsed,

    )