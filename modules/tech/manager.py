"""
Technology Detection Manager

Coordinates technology detection.
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
    progress_status,
    success,
    warning,
)

from modules.tech.analyzer import (
    analyze,
)
from modules.tech.detector import (
    detect_technologies,
)
from modules.tech.exporter import (
    export_all,
)


# ==========================================================
# Detect One Host
# ==========================================================

def detect_one_host(
    host: str,
    response: dict,
) -> tuple[str, dict]:
    """
    Detect technologies for one host.
    """

    return (
        host,
        detect_technologies(
            response,
        ),
    )


# ==========================================================
# Detect Hosts
# ==========================================================

def detect_hosts(
    http_results: dict,
) -> tuple[
    dict,
    list[str],
    float,
]:
    """
    Detect technologies for all hosts.

    Returns:
        (
            results,
            failed_hosts,
            elapsed,
        )
    """

    info(
        "Starting Technology Detection..."
    )

    results: dict = {}

    failed_hosts: list[str] = []

    completed = 0

    total = len(
        http_results
    )

    start_time = (
        time.perf_counter()
    )

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {

            executor.submit(
                detect_one_host,
                host,
                response,
            ): host

            for host, response
            in http_results.items()

        }

        for future in as_completed(
            futures,
        ):

            host = futures[
                future
            ]

            completed += 1

            try:

                (
                    hostname,
                    technologies,
                ) = future.result()

                results[
                    hostname
                ] = technologies

                progress_status(
                    completed,
                    total,
                    (
                        f"✓ {hostname} "
                        f"["
                        f"{len(technologies.get('technologies', []))}"
                        f" tech]"
                    ),
                )

            except Exception as error:

                failed_hosts.append(
                    host,
                )

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
        f"Technology Detection Completed: "
        f"{len(results)}"
    )

    success(
        f"Failed Hosts: "
        f"{len(failed_hosts)}"
    )

    return (
        results,
        failed_hosts,
        elapsed,
    )


# ==========================================================
# Run
# ==========================================================

def run(
    http_results: dict,
) -> dict:
    """
    Run technology detection workflow.

    Returns:
        Analysis dictionary.
    """

    (
        results,
        failed_hosts,
        elapsed,
    ) = detect_hosts(
        http_results,
    )

    analysis = analyze(
        results=results,
        failed_hosts=failed_hosts,
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