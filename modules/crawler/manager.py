"""
Crawler Manager

Coordinate URL crawling, analysis, and exporting.
"""

from __future__ import annotations

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
    warning,
    success,
    progress_status,
)

from modules.crawler.analyzer import (
    analyze,
)

from modules.crawler.exporter import (
    export_all,
)

from modules.crawler.crawler import (
    crawl_host,
)


# ==========================================================
# Crawl One Host
# ==========================================================

def crawl_one_host(
    host: str,
) -> tuple[
    str,
    dict | None,
]:
    """
    Crawl a single host.

    Args:
        host:
            Target hostname.

    Returns:
        Hostname and crawl result.
    """

    return (
        host,
        crawl_host(
            host,
        ),
    )


# ==========================================================
# Crawl Hosts
# ==========================================================

def crawl_hosts(
    hosts: list[str],
) -> tuple[
    dict[str, dict],
    float,
]:
    """
    Crawl multiple hosts in parallel.

    Args:
        hosts:
            Target hosts.

    Returns:
        Crawl results and elapsed time.
    """

    info(
        "Starting URL Crawling..."
    )

    results: dict[
        str,
        dict,
    ] = {}

    completed = 0

    total = len(
        hosts
    )

    start_time = (
        time.perf_counter()
    )

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {

            executor.submit(
                crawl_one_host,
                host,
            ): host

            for host in hosts
        }

        for future in as_completed(
            futures
        ):

            completed += 1

            host = futures[
                future
            ]

            try:

                (
                    hostname,
                    result,
                ) = future.result()

                if result is not None:

                    results[
                        hostname
                    ] = result

                    pages = result[
                        "statistics"
                    ][
                        "pages"
                    ]

                    progress_status(
                        completed,
                        total,
                        (
                            f"✓ {hostname} "
                            f"({pages} pages)"
                        ),
                    )

                else:

                    progress_status(
                        completed,
                        total,
                        f"✗ {hostname}",
                    )

            except Exception as error:

                warning(
                    f"{host}: {error}"
                )

                progress_status(
                    completed,
                    total,
                    f"✗ {host}",
                )

    elapsed = round(
        time.perf_counter()
        - start_time,
        2,
    )

    success(
        f"Hosts Crawled : {len(results)}"
    )

    return (
        results,
        elapsed,
    )


# ==========================================================
# Run Crawler
# ==========================================================

def run(
    hosts: list[str],
) -> dict:
    """
    Run the URL Discovery module.

    Args:
        hosts:
            Target hosts.

    Returns:
        Crawl analysis.
    """

    (
        results,
        elapsed,
    ) = crawl_hosts(
        hosts,
    )

    analysis = analyze(
        results=results,
        elapsed=elapsed,
    )

    export_all(
        analysis,
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
]