#!/usr/bin/env python3

"""
Crawler Manager

Coordinate URL crawling and analysis.
"""

from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import (
    info,
    progress_status,
    success,
    warning,
)

from modules.crawler.analyzer import analyze
from modules.crawler.crawler import crawl_host

# ==========================================================
# Crawl One Host
# ==========================================================


def crawl_one_host(
    context: ExecutionContext,
    host: str,
) -> tuple[str, dict[str, Any] | None]:
    """
    Crawl a single host.
    """

    return (
        host,
        crawl_host(
            context=context,
            host=host,
        ),
    )


# ==========================================================
# Crawl Hosts
# ==========================================================


def crawl_hosts(
    context: ExecutionContext,
    hosts: list[str],
) -> dict[str, dict[str, Any]]:
    """
    Crawl multiple hosts in parallel.
    """

    info("Starting URL Crawling...")

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Thread pool not initialized.")

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    completed = 0

    total = len(
        hosts,
    )

    futures = {
        executor.submit(
            crawl_one_host,
            context,
            host,
        ): host
        for host in hosts
    }

    for future in as_completed(
        futures,
    ):

        completed += 1

        host = futures[future]

        try:

            (
                hostname,
                result,
            ) = future.result()

            if result is not None:

                results[hostname] = result

                pages = result["statistics"]["pages"]

                progress_status(
                    completed,
                    total,
                    (f"✓ {hostname} " f"({pages} pages)"),
                )

            else:

                progress_status(
                    completed,
                    total,
                    f"✗ {hostname}",
                )

        except Exception as exception:

            warning(
                f"{host}: {exception}",
            )

            progress_status(
                completed,
                total,
                f"✗ {host}",
            )

    success(
        f"Hosts Crawled : {len(results)}",
    )

    return results


# ==========================================================
# Run Crawler
# ==========================================================


def run(
    context: ExecutionContext,
    hosts: list[str],
) -> dict[str, Any]:
    """
    Execute the complete crawler workflow.

        Crawl
           ↓
        Analyze
           ↓
        Store Context
           ↓
        Return Analysis
    """

    results = crawl_hosts(
        context=context,
        hosts=hosts,
    )

    analysis = analyze(
        results=results,
    )

    context.set_analysis(
        "crawler",
        analysis,
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
]
