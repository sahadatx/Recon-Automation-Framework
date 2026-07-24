"""
Port Scanner Manager

Coordinate port scanning, analysis, and exporting.
"""

from __future__ import annotations

import time
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from config.config import (
    PORT_HOST_WORKERS,
)

from core.logger import (
    info,
    progress_status,
    success,
    warning,
)

from modules.ports.analyzer import (
    analyze,
)

from modules.ports.exporter import (
    export_all,
)

from modules.ports.scanner import (
    scan_common_ports,
)


# ==========================================================
# Scan One Host
# ==========================================================

def scan_one_host(
    host: str,
) -> tuple[
    str,
    list[dict],
]:
    """
    Scan common TCP ports for one host.

    Args:
        host: Target hostname.

    Returns:
        Hostname and open ports.
    """

    return (
        host,
        scan_common_ports(host),
    )


# ==========================================================
# Scan Hosts
# ==========================================================

def scan_hosts(
    hosts: list[str],
) -> tuple[
    dict[str, list[dict]],
    list[str],
    float,
]:
    """
    Scan multiple hosts in parallel.

    Args:
        hosts: Target hosts.

    Returns:
        Scan results,
        failed hosts,
        elapsed time.
    """

    info(
        "Starting Port Scan..."
    )

    results: dict[
        str,
        list[dict],
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
        max_workers=PORT_HOST_WORKERS,
    ) as executor:

        futures = {

            executor.submit(
                scan_one_host,
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
                    open_ports,
                ) = future.result()

                if open_ports:

                    results[
                        hostname
                    ] = open_ports

                    progress_status(
                        completed,
                        total,
                        (
                            f"✓ {hostname} "
                            f"[{len(open_ports)} open]"
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
        f"Hosts With Open Ports : {len(results)}"
    )

    success(
        f"Hosts Without Open Ports : {len(failed_hosts)}"
    )

    return (
        results,
        failed_hosts,
        elapsed,
    )


# ==========================================================
# Run Port Scanner
# ==========================================================

def run(
    hosts: list[str],
) -> dict:
    """
    Run the Port Scanner module.

    Args:
        hosts: Target hosts.

    Returns:
        Port scan analysis.
    """

    (
        results,
        failed_hosts,
        elapsed,
    ) = scan_hosts(
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