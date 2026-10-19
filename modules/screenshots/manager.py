from __future__ import annotations

import asyncio
from typing import Any

from config.config import SCREENSHOT_WORKERS
from core.context import ExecutionContext
from core.logger import info, progress_status, success, warning
from modules.screenshots.analyzer import analyze
from modules.screenshots.capture import capture_host
from modules.screenshots.helpers import (
    cleanup,
    close_context,
    create_context,
    launch_browser,
    start_playwright,
)


async def capture_one(
    semaphore: asyncio.Semaphore,
    browser: Any,
    host: str,
    response: dict[str, Any],
) -> tuple[str, dict[str, Any]]:


    async with semaphore:

        browser_context = await create_context(
            browser,
        )

        try:

            metadata = await capture_host(
                browser_context,
                response,
            )

            return (
                host,
                metadata,
            )

        finally:

            await close_context(
                browser_context,
            )


async def capture_hosts(
    context: ExecutionContext,
    http_results: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    list[str],
]:


    _ = context

    info("Starting Screenshot Capture...")

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed: list[str] = []

    total = len(
        http_results,
    )

    completed = 0

    if total == 0:

        warning("No HTTP targets found.")

        return (
            {},
            [],
        )

    semaphore = asyncio.Semaphore(
        SCREENSHOT_WORKERS,
    )

    playwright = await start_playwright()

    browser = await launch_browser(
        playwright,
    )

    try:

        tasks = [
            capture_one(
                semaphore,
                browser,
                host,
                response,
            )
            for (
                host,
                response,
            ) in http_results.items()
        ]

        for task in asyncio.as_completed(
            tasks,
        ):

            completed += 1

            try:

                (
                    host,
                    metadata,
                ) = await task

                if metadata.get(
                    "captured",
                    False,
                ):

                    results[host] = metadata

                    progress_status(
                        completed,
                        total,
                        f"✓ {host}",
                    )

                else:

                    failed.append(
                        host,
                    )

                    progress_status(
                        completed,
                        total,
                        f"✗ {host}",
                    )

            except Exception as error:

                warning(
                    str(error),
                )

    finally:

        await cleanup(
            playwright,
            browser,
        )

    success(f"Captured Screenshots : {len(results)}")

    warning(f"Failed Screenshots : {len(failed)}")

    return (
        results,
        sorted(
            failed,
        ),
    )


async def run_async(
    context: ExecutionContext,
    http_results: dict[str, dict[str, Any]],
) -> dict[str, Any]:


    (
        results,
        failed,
    ) = await capture_hosts(
        context,
        http_results,
    )

    analysis = analyze(
        results=list(
            results.values(),
        ),
    )

    analysis["failed_hosts"] = failed

    context.set_analysis(
        "screenshots",
        analysis,
    )

    return analysis


def run(
    context: ExecutionContext,
    http_results: dict[str, dict[str, Any]],
) -> dict[str, Any]:


    return asyncio.run(
        run_async(
            context,
            http_results,
        )
    )


__all__ = [
    "capture_one",
    "capture_hosts",
    "run_async",
    "run",
]
