"""
DNS Resolution Manager

Coordinate DNS resolution, analysis, and exporting.
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

from modules.dns.analyzer import (
    analyze,
)

from modules.dns.exporter import (
    export_all,
)

from modules.dns.records import (
    resolve_all_records,
)


# ==========================================================
# Resolve One Subdomain
# ==========================================================

def resolve_subdomain(
    subdomain: str,
) -> tuple[
    str,
    dict[str, list[str]],
]:
    """
    Resolve every supported DNS record
    for one subdomain.
    """

    return (
        subdomain,
        resolve_all_records(
            subdomain,
        ),
    )


# ==========================================================
# Resolve All Subdomains
# ==========================================================

def resolve_subdomains(
    subdomains: list[str],
) -> tuple[
    dict[str, dict[str, list[str]]],
    list[str],
    float,
]:
    """
    Resolve DNS records for every subdomain.
    """

    info(
        "Starting DNS Resolution..."
    )

    results: dict[
        str,
        dict[str, list[str]],
    ] = {}

    failed_hosts: list[str] = []

    total = len(
        subdomains
    )

    completed = 0

    start_time = (
        time.perf_counter()
    )

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {
            executor.submit(
                resolve_subdomain,
                subdomain,
            ): subdomain
            for subdomain in subdomains
        }

        for future in as_completed(
            futures
        ):

            subdomain = futures[
                future
            ]

            completed += 1

            try:

                (
                    hostname,
                    records,
                ) = future.result()

                results[
                    hostname
                ] = records

            except Exception as error:

                warning(
                    f"{subdomain}: "
                    f"{error}"
                )

                failed_hosts.append(
                    subdomain
                )

            progress_status(
                completed,
                total,
                f"✓ {subdomain} resolved",
            )

    elapsed = round(
        time.perf_counter()
        - start_time,
        2,
    )

    success(
        f"Resolved "
        f"{len(results)} hosts."
    )

    return (
        results,
        sorted(
            failed_hosts
        ),
        elapsed,
    )


# ==========================================================
# Run DNS Resolution
# ==========================================================

def run(
    subdomains: list[str],
) -> dict:
    """
    Execute the complete DNS
    resolution workflow.

    Workflow:
        Resolve
        -> Analyze
        -> Export
        -> Return
    """

    (
        results,
        failed_hosts,
        elapsed,
    ) = resolve_subdomains(
        subdomains,
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