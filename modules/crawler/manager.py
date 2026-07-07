"""
Crawler Manager

Coordinates parallel URL discovery.
"""

import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from config.config import (
    CRAWLER_WORKERS,
)

from core.logger import (
    info,
    success,
    warning,
)

from modules.crawler.crawler import (
    crawl_host,
)


# ==========================================================
# Retry Count
# ==========================================================

RETRY_COUNT = 2


# ==========================================================
# Crawl One Host
# ==========================================================

def crawl_one(
    host: str,
):
    """
    Crawl a single host.

    Returns:
        tuple[str, dict | None]
    """

    for attempt in range(

        RETRY_COUNT + 1

    ):

        try:

            result = crawl_host(
                host
            )

            return (

                host,

                result,

            )

        except Exception as error:

            warning(

                f"{host} "

                f"(Attempt {attempt + 1}) "

                f"{error}"

            )

    return (

        host,

        None,

    )


# ==========================================================
# Create Summary
# ==========================================================

def create_summary():
    """
    Initialize manager statistics.
    """

    return {

        "hosts": 0,

        "success": 0,

        "failed": 0,

        "pages": 0,

        "elapsed": 0.0,

    }


# ==========================================================
# Crawl Multiple Hosts
# ==========================================================

def crawl_hosts(
    hosts: list[str],
):
    """
    Crawl multiple hosts.

    Returns:
        dict
    """

    info(
        "Starting URL Discovery..."
    )

    start_time = time.perf_counter()

    results = {}

    failed = []

    summary = create_summary()

    summary["hosts"] = len(
        hosts
    )

    completed = 0

    with ThreadPoolExecutor(

        max_workers=CRAWLER_WORKERS,

    ) as executor:

        futures = {

            executor.submit(

                crawl_one,

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

                hostname, result = (

                    future.result()

                )

                if result:

                    results[
                        hostname
                    ] = result

                    summary[
                        "success"
                    ] += 1

                    summary[
                        "pages"
                    ] += result[
                        "statistics"
                    ][
                        "pages"
                    ]

                    info(

                        f"[{completed}/"

                        f"{summary['hosts']}] "

                        f"✓ {hostname}"

                    )

                else:

                    failed.append(
                        hostname
                    )

                    summary[
                        "failed"
                    ] += 1

                    warning(

                        f"[{completed}/"

                        f"{summary['hosts']}] "

                        f"✗ {hostname}"

                    )

            except Exception as error:

                failed.append(
                    host
                )

                summary[
                    "failed"
                ] += 1

                warning(

                    f"{host}: {error}"

                )

    summary["elapsed"] = round(

        time.perf_counter()

        - start_time,

        2,

    )

    success(
        "-" * 50
    )

    success(
        "URL Discovery Completed"
    )

    success(
        "-" * 50
    )

    success(

        f"Hosts      : "

        f"{summary['hosts']}"

    )

    success(

        f"Success    : "

        f"{summary['success']}"

    )

    success(

        f"Failed     : "

        f"{summary['failed']}"

    )

    success(

        f"Pages      : "

        f"{summary['pages']}"

    )

    success(

        f"Elapsed    : "

        f"{summary['elapsed']} sec"

    )

    success(
        "-" * 50
    )

    return {

        "results": results,

        "failed": failed,

        "summary": summary,

    }