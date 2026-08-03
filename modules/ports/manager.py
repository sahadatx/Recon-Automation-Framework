#!/usr/bin/env python3

"""
Port Scanner Manager

Coordinate port scanning
and analysis.
"""

from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import info, progress_status, success, warning
from modules.ports.analyzer import analyze
from modules.ports.scanner import scan_common_ports

# ==========================================================
# Scan One Host
# ==========================================================


def scan_one_host(
    context: ExecutionContext,
    host: str,
) -> tuple[
    str,
    list[dict[str, Any]],
]:
    """
    Scan common TCP ports
    for one host.
    """

    return (
        host,
        scan_common_ports(
            context,
            host,
        ),
    )


# ==========================================================
# Scan Hosts
# ==========================================================


def scan_hosts(
    context: ExecutionContext,
    hosts: list[str],
) -> tuple[
    dict[str, list[dict[str, Any]]],
    list[str],
]:
    """
    Scan multiple hosts using
    the shared thread pool.
    """

    info("Starting Port Scan...")

    results: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    failed_hosts: list[str] = []

    total = len(
        hosts,
    )

    completed = 0

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Shared thread pool " "is not initialized.")

    futures = {
        executor.submit(
            scan_one_host,
            context,
            host,
        ): host
        for host in hosts
    }

    for future in as_completed(
        futures,
    ):

        host = futures[future]

        completed += 1

        try:

            (
                hostname,
                open_ports,
            ) = future.result()

            if open_ports:

                results[hostname] = open_ports

                progress_status(
                    completed,
                    total,
                    (f"✓ {hostname} " f"[{len(open_ports)} open]"),
                )

            else:

                failed_hosts.append(
                    hostname,
                )

                progress_status(
                    completed,
                    total,
                    f"✗ {hostname}",
                )

        except Exception as error:

            failed_hosts.append(
                host,
            )

            warning(
                f"{host}: {error}",
            )

            progress_status(
                completed,
                total,
                f"✗ {host}",
            )

    success(f"Hosts With Open Ports : {len(results)}")

    success(("Hosts Without Open Ports : " f"{len(failed_hosts)}"))

    return (
        results,
        sorted(
            failed_hosts,
        ),
    )


# ==========================================================
# Run Port Scanner
# ==========================================================


def run(
    context: ExecutionContext,
    hosts: list[str],
) -> dict[str, Any]:
    """
    Execute the complete
    port scanning workflow.

        Scan
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
    ) = scan_hosts(
        context,
        hosts,
    )

    analysis = analyze(
        results=results,
        failed_hosts=failed_hosts,
    )

    context.set_analysis(
        "ports",
        analysis,
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
]
