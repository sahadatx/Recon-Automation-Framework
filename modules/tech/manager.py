#!/usr/bin/env python3

"""
Technology Detection Manager

Coordinate technology
detection and analysis.
"""

from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import info, progress_status, success, warning
from modules.tech.analyzer import analyze
from modules.tech.detector import detect_technologies

# ==========================================================
# Detect One Host
# ==========================================================


def detect_one_host(
    host: str,
    response: dict[str, Any],
) -> tuple[
    str,
    dict[str, Any],
]:
    """
    Detect technologies
    for one host.
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
    context: ExecutionContext,
    http_results: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    list[str],
]:
    """
    Detect technologies
    for all hosts.
    """

    info("Starting Technology Detection...")

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed_hosts: list[str] = []

    total = len(
        http_results,
    )

    completed = 0

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Shared thread pool is not initialized.")

    futures = {
        executor.submit(
            detect_one_host,
            host,
            response,
        ): host
        for (
            host,
            response,
        ) in http_results.items()
    }

    for future in as_completed(
        futures,
    ):

        host = futures[future]

        completed += 1

        try:

            (
                hostname,
                technologies,
            ) = future.result()

            results[hostname] = technologies

            progress_status(
                completed,
                total,
                (
                    f"✓ {hostname} "
                    f"[{len(technologies.get('technologies', []))} tech]"
                ),
            )

        except Exception as error:

            failed_hosts.append(
                host,
            )

            warning(f"{host}: {error}")

            progress_status(
                completed,
                total,
                f"✗ {host}",
            )

    success(f"Technology Detection Completed: {len(results)}")

    success(f"Failed Hosts: {len(failed_hosts)}")

    return (
        results,
        sorted(
            failed_hosts,
        ),
    )


# ==========================================================
# Run Technology Detection
# ==========================================================


def run(
    context: ExecutionContext,
    http_results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Execute the complete
    technology detection workflow.

        Detect
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
    ) = detect_hosts(
        context,
        http_results,
    )

    analysis = analyze(
        results=results,
        failed_hosts=failed_hosts,
    )

    context.set_analysis(
        "technology",
        analysis,
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
]
