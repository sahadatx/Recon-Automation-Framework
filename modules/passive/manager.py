"""
Passive Enumeration Manager

Coordinates all passive enumeration sources.
"""

from __future__ import annotations

import re
import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from typing import Callable

from config.config import MAX_WORKERS

from core.logger import (
    info,
    warning,
)

from modules.passive.analyzer import analyze
from modules.passive.exporter import export_all

from modules.passive.assetfinder import run_assetfinder
from modules.passive.chaos import run_chaos
from modules.passive.crtsh import run_crtsh
from modules.passive.findomain import run_findomain
from modules.passive.securitytrails import run_securitytrails
from modules.passive.subfinder import run_subfinder

PassiveSource = Callable[
    [str],
    list[str],
]

# ==========================================================
# Tool Registry
# ==========================================================

PASSIVE_SOURCES: list[
    tuple[
        str,
       PassiveSource,
    ]
] = [
    (
        "Subfinder",
        run_subfinder,
    ),
    (
        "Assetfinder",
        run_assetfinder,
    ),
    (
        "crt.sh",
        run_crtsh,
    ),
    (
        "Chaos",
        run_chaos,
    ),
    (
        "Findomain",
        run_findomain,
    ),
    (
        "SecurityTrails",
        run_securitytrails,
    ),
]

RETRYABLE_TOOLS: frozenset[str] = frozenset(
    {
        "crt.sh",
    }
)

DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
)


# ==========================================================
# Timed Runner
# ==========================================================

def timed_runner(
    function: PassiveSource,
    domain: str,
) -> tuple[list[str], float]:
    """
    Execute a passive source and measure execution time.

    Args:
        function: Passive enumeration function.
        domain: Target domain.

    Returns:
        Tuple containing discovered subdomains and
        execution time.
    """

    start_time = time.perf_counter()

    results = function(domain)

    elapsed_time = round(
        time.perf_counter() - start_time,
        2,
    )

    return (
        results,
        elapsed_time,
    )


# ==========================================================
# Collect Passive Enumeration
# ==========================================================

def collect_subdomains(
    domain: str,
) -> tuple[
    dict[str, list[str]],
    dict[str, float],
    list[str],
    float,
]:
    """
    Run all passive enumeration sources concurrently.

    Args:
        domain: Target domain.

    Returns:
        Tuple containing:
            - Results grouped by source.
            - Execution time per source.
            - Failed sources.
            - Total scan time.
    """

    info(
        "Starting Passive Enumeration..."
    )

    results: dict[
        str,
        list[str],
    ] = {}

    timings: dict[
        str,
        float,
    ] = {}

    failed_sources: list[str] = []

    retry_queue: list[
        tuple[
            str,
            PassiveSource,
        ]
    ] = []

    total_sources = len(
        PASSIVE_SOURCES
    )

    completed_sources = 0

    scan_start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {
            executor.submit(
                timed_runner,
                function,
                domain,
            ): (
                name,
                function,
            )
            for name, function in PASSIVE_SOURCES
        }

        for future in as_completed(
            futures,
        ):

            name, function = futures[
                future
            ]

            completed_sources += 1

            try:

                subdomains, elapsed = (
                    future.result()
                )

            except Exception as error:

                warning(
                    f"{name} crashed: {error}"
                )

                subdomains = []
                elapsed = 0.0

                failed_sources.append(
                    name,
                )

            results[name] = subdomains

            timings[name] = elapsed

            info(
                f"[{completed_sources}/{total_sources}] "
                f"{name} completed."
            )

            if (
                not subdomains
                and name in RETRYABLE_TOOLS
            ):

                retry_queue.append(
                    (
                        name,
                        function,
                    )
                )

    # ------------------------------------------------------
    # Retry Failed Sources
    # ------------------------------------------------------

    if retry_queue:

        info(
            "Retrying failed sources..."
        )

        for (
            name,
            function,
        ) in retry_queue:

            try:

                retry_results = function(
                    domain,
                )

                if retry_results:

                    results[name] = retry_results

                    if (
                        name
                        in failed_sources
                    ):

                        failed_sources.remove(
                            name,
                        )

            except Exception as error:

                warning(
                    f"{name} retry failed: {error}"
                )

    total_scan_time = round(
        time.perf_counter() - scan_start,
        2,
    )

    return (
        results,
        timings,
        failed_sources,
        total_scan_time,
    )


# ==========================================================
# Merge Results
# ==========================================================

def merge_results(
    results: dict[str, list[str]],
    domain: str,
) -> list[str]:
    """
    Merge, normalize, validate and deduplicate subdomains.

    Args:
        results: Raw results grouped by source.
        domain: Target domain.

    Returns:
        Sorted list of unique subdomains.
    """

    target_domain = domain.lower()

    suffix = f".{target_domain}"

    unique_subdomains: set[str] = set()

    for subdomains in results.values():

        for subdomain in subdomains:

            if not subdomain:
                continue

            normalized = (
                subdomain
                .strip()
                .lower()
                .rstrip(".")
            )

            if (
                normalized != target_domain
                and not normalized.endswith(
                    suffix
                )
            ):
                continue

            if not DOMAIN_RE.fullmatch(
                normalized
            ):
                continue

            unique_subdomains.add(
                normalized
            )

    return sorted(
        unique_subdomains,
    )


# ==========================================================
# Run Passive Enumeration
# ==========================================================

def run(
    domain: str,
) -> dict[str, object]:
    """
    Execute the complete passive enumeration workflow.

    Workflow:
        Collect
            ↓
        Merge
            ↓
        Analyze
            ↓
        Export

    Args:
        domain: Target domain.

    Returns:
        Analysis dictionary.
    """

    (
        results,
        timings,
        failed_sources,
        total_scan_time,
    ) = collect_subdomains(
        domain,
    )

    unique_subdomains = merge_results(
        results,
        domain,
    )

    analysis = analyze(
        target=domain,
        results=results,
        unique_subdomains=unique_subdomains,
        timings=timings,
        failed_sources=failed_sources,
        total_scan_time=total_scan_time,
    )

    export_all(
        analysis,
    )

    return analysis


__all__ = [
    "run",
]