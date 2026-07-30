#!/usr/bin/env python3

"""
DNS Resolution Manager

Coordinate DNS resolution and analysis.
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

from modules.dns.analyzer import analyze
from modules.dns.records import resolve_all_records


# ==========================================================
# Resolve One Subdomain
# ==========================================================


def resolve_subdomain(
    context: ExecutionContext,
    subdomain: str,
) -> tuple[str, dict[str, list[str]]]:
    """
    Resolve every supported DNS record
    for a single subdomain.

    Cached results are reused whenever
    available.
    """

    if context.has_dns_cache(subdomain):

        return (
            subdomain,
            context.get_dns_cache(
                subdomain,
            ),
        )

    records = resolve_all_records(
        subdomain,
    )

    context.set_dns_cache(
        subdomain,
        records,
    )

    return (
        subdomain,
        records,
    )


# ==========================================================
# Resolve All Subdomains
# ==========================================================


def resolve_subdomains(
    context: ExecutionContext,
    subdomains: list[str],
) -> tuple[
    dict[str, dict[str, list[str]]],
    list[str],
]:
    """
    Resolve DNS records for every
    discovered subdomain.
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
        subdomains,
    )

    completed = 0

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError(
            "Shared thread pool is not initialized."
        )

    futures = {

        executor.submit(
            resolve_subdomain,
            context,
            subdomain,
        ): subdomain

        for subdomain in subdomains

    }

    for future in as_completed(
        futures,
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
                f"{subdomain}: {error}"
            )

            failed_hosts.append(
                subdomain,
            )

        progress_status(
            completed,
            total,
            f"✓ {subdomain} resolved",
        )

    success(
        f"Resolved {len(results)} hosts."
    )

    return (
        results,
        sorted(
            failed_hosts,
        ),
    )


# ==========================================================
# Run DNS Resolution
# ==========================================================


def run(
    context: ExecutionContext,
    subdomains: list[str],
) -> dict[str, Any]:
    """
    Execute the complete DNS
    resolution workflow.

        Resolve
            ↓
        Analyze
            ↓
        Store Context
            ↓
        Return Analysis
    """

    (
        results,
        failed_hosts,
    ) = resolve_subdomains(
        context,
        subdomains,
    )

    analysis = analyze(
        results=results,
        failed_hosts=failed_hosts,
    )

    context.set_analysis(
        "dns",
        analysis,
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
]