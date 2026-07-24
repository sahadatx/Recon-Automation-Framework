"""
Screenshot Manager

Production Async Screenshot Manager.
"""

from __future__ import annotations

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


from modules.screenshots.helpers import (
    start_playwright,
    launch_browser,
    create_context,
    close_context,
    cleanup,
)


from modules.screenshots.capture import (
    capture_host,
)


from modules.screenshots.analyzer import (
    analyze,
)


from modules.screenshots.exporter import (
    export_all,
    show_summary,
)



# ==========================================================
# Capture One Host
# ==========================================================

async def capture_one(
    semaphore: asyncio.Semaphore,
    browser,
    host: str,
    response: dict,
) -> tuple[str, dict]:
    """
    Capture screenshot for one host.

    Each target gets isolated
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
) -> tuple[
    dict,
    list[str],
    float,
]:
    """
    Capture screenshots for
    HTTP probe results.

    Returns:

        results,
        failed,
        elapsed

    """


    info(
        "Starting Screenshot Capture..."
    )


    start = time.perf_counter()


    results: dict = {}

    failed: list[str] = []


    total = len(
        http_results
    )


    completed = 0


    if total == 0:

        warning(
            "No HTTP targets found."
        )

        return (

            {},

            [],

            0.0,

        )


    semaphore = asyncio.Semaphore(

        SCREENSHOT_WORKERS

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

        - start,

        2,

    )


    success(

        f"Captured Screenshots : {len(results)}"

    )


    warning(

        f"Failed Screenshots : {len(failed)}"

    )


    success(

        f"Elapsed : {elapsed:.2f} sec"

    )


    return (

        results,

        failed,

        elapsed,

    )



# ==========================================================
# Run Screenshot Pipeline
# ==========================================================

async def run(
    http_results: dict,
) -> dict:
    """
    Run complete screenshot workflow.

    Workflow:

        HTTP Results
              |
              v
        Screenshot Capture
              |
              v
        Analyze
              |
              v
        Export
              |
              v
        Summary

    """


    results, failed, elapsed = await capture_hosts(

        http_results

    )


    analysis = analyze(

        results=list(

            results.values()

        ),

        elapsed=elapsed,

    )


    analysis["failed_hosts"] = failed



    export_all(

        analysis

    )


    show_summary(

        analysis

    )


    return analysis



# ==========================================================
# Sync Entry Point
# ==========================================================

def execute(
    http_results: dict,
) -> dict:
    """
    Synchronous wrapper.

    """

    return asyncio.run(

        run(

            http_results

        )

    )



# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "capture_one",

    "capture_hosts",

    "run",

    "execute",

]