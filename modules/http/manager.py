"""
HTTP Probe Manager

Coordinate HTTP probing, analysis, and exporting.
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

from modules.http.analyzer import (
    analyze,
)

from modules.http.exporter import (
    export_all,
)

from modules.http.probe import (
    probe_host,
)


# ==========================================================
# Probe One Host
# ==========================================================

def probe_one_host(
    host: str,
) -> tuple[str, dict | None]:
    """
    Probe a single host.

    Args:
        host: Target hostname.

    Returns:
        Hostname and probe result.
    """

    return (
        host,
        probe_host(host),
    )


# ==========================================================
# Probe Hosts
# ==========================================================

def probe_hosts(
    hosts: list[str],
) -> tuple[
    dict[str, dict],
    list[str],
    float,
]:
    """
    Probe multiple hosts in parallel.

    Args:
        hosts: Target hosts.

    Returns:
        Probe results,
        failed hosts,
        elapsed time.
    """

    info(
        "Starting HTTP Probe..."
    )

    results: dict[
        str,
        dict,
    ] = {}

    failed_hosts: list[
        str
    ] = []

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
                probe_one_host,
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
                        hostname
                    )

                    progress_status(
                        completed,
                        total,
                        f"✗ {hostname}",
                    )

            except Exception as error:

                failed_hosts.append(
                    host
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
        f"Alive Hosts : {len(results)}"
    )

    success(
        f"Dead Hosts  : {len(failed_hosts)}"
    )

    return (
        results,
        failed_hosts,
        elapsed,
    )


# ==========================================================
# Run HTTP Probe
# ==========================================================

def run(
    hosts: list[str],
) -> dict:
    """
    Run the HTTP Probe module.

    Args:
        hosts: Target hosts.

    Returns:
        HTTP analysis.
    """

    (
        results,
        failed_hosts,
        elapsed,
    ) = probe_hosts(
        hosts,
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