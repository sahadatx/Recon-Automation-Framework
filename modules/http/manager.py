#!/usr/bin/env python3

"""
HTTP Probe Manager

Coordinate HTTP probing
and analysis.
"""

from __future__ import annotations

from concurrent.futures import (
    as_completed,
)

from typing import Any

from core.context import (
    ExecutionContext,
)

from core.logger import (
    info,
    progress_status,
    success,
    warning,
)

from modules.http.analyzer import (
    analyze,
)

from modules.http.probe import (
    probe_host,
)


# ==========================================================
# Probe One Host
# ==========================================================


def probe_one_host(
    context: ExecutionContext,
    host: str,
) -> tuple[
    str,
    dict[str, Any] | None,
]:
    """
    Probe one host.

    Shared HTTP session is reused
    across every request.
    """

    session = context.get_http_session()

    if session is None:

        raise RuntimeError(
            "Shared HTTP session "
            "is not initialized."
        )

    return (
        host,
        probe_host(
            session=session,
            host=host,
        ),
    )


# ==========================================================
# Probe Hosts
# ==========================================================


def probe_hosts(
    context: ExecutionContext,
    hosts: list[str],
) -> tuple[
    dict[str, dict[str, Any]],
    list[str],
]:
    """
    Probe all hosts in parallel.
    """

    info(
        "Starting HTTP Probe..."
    )

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed_hosts: list[str] = []

    completed = 0

    total = len(
        hosts,
    )

    executor = (
        context.get_thread_pool()
    )

    if executor is None:

        raise RuntimeError(
            "Shared thread pool "
            "is not initialized."
        )

    futures = {

        executor.submit(
            probe_one_host,
            context,
            host,
        ): host

        for host in hosts

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
                response,
            ) = future.result()

            if response:

                results[
                    hostname
                ] = response

                progress_status(
                    completed,
                    total,
                    (
                        f"✓ {hostname} "
                        f"({response['status']} "
                        f"{response['scheme'].upper()})"
                    ),
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

    success(
        f"Alive Hosts : {len(results)}"
    )

    success(
        f"Dead Hosts  : {len(failed_hosts)}"
    )

    return (
        results,
        sorted(
            failed_hosts,
        ),
    )


# ==========================================================
# Run HTTP Probe
# ==========================================================


def run(
    context: ExecutionContext,
    hosts: list[str],
) -> dict[str, Any]:
    """
    Execute the complete HTTP
    probing workflow.

        Probe
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
    ) = probe_hosts(
        context,
        hosts,
    )

    analysis = analyze(
        results=results,
        failed_hosts=failed_hosts,
    )

    context.set_analysis(
        "http",
        analysis,
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
]