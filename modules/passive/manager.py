#!/usr/bin/env python3

"""
Passive Enumeration Manager

Coordinate passive enumeration.
"""

from __future__ import annotations

import re
import time

from concurrent.futures import (
    as_completed,
)

from typing import (
    Any,
    Callable,
)

from core.context import (
    ExecutionContext,
)

from core.logger import (
    info,
    warning,
)

from modules.passive.analyzer import (
    analyze,
)

from modules.passive.assetfinder import (
    run_assetfinder,
)

from modules.passive.chaos import (
    run_chaos,
)

from modules.passive.crtsh import (
    run_crtsh,
)

from modules.passive.findomain import (
    run_findomain,
)

from modules.passive.securitytrails import (
    run_securitytrails,
)

from modules.passive.subfinder import (
    run_subfinder,
)


# ==========================================================
# Type Definitions
# ==========================================================

PassiveSource = Callable[
    [
        ExecutionContext,
        str,
    ],
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
    context: ExecutionContext,
    function: PassiveSource,
    domain: str,
) -> tuple[
    list[str],
    float,
]:
    """
    Execute one passive source and
    measure execution time.
    """

    start_time = time.perf_counter()

    results = function(
        context,
        domain,
    )

    elapsed = round(
        time.perf_counter()
        - start_time,
        2,
    )

    return (
        results,
        elapsed,
    )


# ==========================================================
# Collect Passive Enumeration
# ==========================================================


def collect_subdomains(
    context: ExecutionContext,
    domain: str,
) -> tuple[
    dict[str, list[str]],
    dict[str, float],
    list[str],
]:
    """
    Run all passive sources
    concurrently.
    """

    info(
        "Starting Passive Enumeration..."
    )

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError(
            "Thread pool not initialized."
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
        PASSIVE_SOURCES,
    )

    completed_sources = 0

    futures = {

        executor.submit(
            timed_runner,
            context,
            function,
            domain,
        ): (
            name,
            function,
        )

        for (
            name,
            function,
        ) in PASSIVE_SOURCES

    }

    for future in as_completed(
        futures,
    ):

        (
            name,
            function,
        ) = futures[
            future
        ]

        completed_sources += 1

        try:

            (
                subdomains,
                elapsed,
            ) = future.result()

        except Exception as exc:

            warning(
                f"{name} crashed: {exc}"
            )

            subdomains = []

            elapsed = 0.0

            failed_sources.append(
                name,
            )

        results[
            name
        ] = subdomains

        timings[
            name
        ] = elapsed

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
                    context,
                    domain,
                )

                if retry_results:

                    results[
                        name
                    ] = retry_results

                    if (
                        name
                        in failed_sources
                    ):

                        failed_sources.remove(
                            name,
                        )

            except Exception as exc:

                warning(
                    f"{name} retry failed: {exc}"
                )

    return (
        results,
        timings,
        sorted(
            failed_sources,
        ),
    )


# ==========================================================
# Merge Results
# ==========================================================


def merge_results(
    results: dict[str, list[str]],
    domain: str,
) -> list[str]:
    """
    Merge, normalize and validate
    discovered subdomains.
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
                    suffix,
                )
            ):

                continue

            if not DOMAIN_RE.fullmatch(
                normalized,
            ):

                continue

            unique_subdomains.add(
                normalized,
            )

    return sorted(
        unique_subdomains,
    )


# ==========================================================
# Run Passive Enumeration
# ==========================================================


def run(
    context: ExecutionContext,
    domain: str,
) -> dict[str, Any]:
    """
    Execute the complete passive
    enumeration workflow.

        Collect
            ↓
        Merge
            ↓
        Analyze
            ↓
        Store Context
            ↓
        Return Analysis
    """

    (
        results,
        timings,
        failed_sources,
    ) = collect_subdomains(
        context=context,
        domain=domain,
    )

    unique_subdomains = merge_results(
        results=results,
        domain=domain,
    )

    analysis = analyze(
        target=domain,
        results=results,
        unique_subdomains=unique_subdomains,
        timings=timings,
        failed_sources=failed_sources,
    )

    context.set_analysis(
        "passive",
        analysis,
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
]