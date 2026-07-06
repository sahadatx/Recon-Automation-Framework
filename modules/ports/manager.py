"""
Port Scanner Manager

Coordinates parallel port scanning.
"""

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
    warning,
    success,
    progress_status,
)

from modules.ports.scanner import (
    scan_common_ports,
)


# ==========================================================
# Scan One Host
# ==========================================================

def scan_one_host(
    host: str,
):
    """
    Scan common TCP ports for one host.

    Returns:
        tuple[str, list]
    """

    ports = scan_common_ports(
        host
    )

    return (
        host,
        ports,
    )


# ==========================================================
# Scan All Hosts
# ==========================================================

def scan_hosts(
    hosts: list[str],
):
    """
    Scan all hosts in parallel.

    Returns:
        (
            results,
            failed,
            elapsed
        )
    """

    info(
        "Starting Port Scan..."
    )

    results = {}

    failed = []

    retry_queue = []

    completed = 0

    total = len(hosts)

    start_time = time.perf_counter()

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

            host = futures[
                future
            ]

            completed += 1

            try:

                hostname, open_ports = (
                    future.result()
                )

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

                    failed.append(
                        hostname
                    )

                    progress_status(
                        completed,
                        total,
                        f"✗ {hostname}",
                    )

            except Exception as error:

                failed.append(
                    host
                )

                retry_queue.append(
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

    # ======================================================
    # Retry Queue (Future)
    # ======================================================

    if retry_queue:

        info(
            f"Retry Queue: "
            f"{len(retry_queue)} host(s)"
        )

        # Future:
        # Retry failed hosts using
        # PORT_SCAN_RETRY.

    elapsed = round(
        time.perf_counter()
        - start_time,
        2,
    )

    # ======================================================
    # Statistics
    # ======================================================

    total_open_ports = sum(
        len(ports)
        for ports in results.values()
    )

    success(
        f"Scanned Hosts : {total}"
    )

    success(
        f"Hosts With Open Ports : {len(results)}"
    )

    success(
        f"Hosts Without Open Ports : {len(failed)}"
    )

    success(
        f"Total Open Ports : {total_open_ports}"
    )

    return (
        results,
        failed,
        elapsed,
    )