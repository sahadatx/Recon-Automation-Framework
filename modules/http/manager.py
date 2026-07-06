"""
HTTP Probe Manager

Coordinates parallel HTTP probing.
"""

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

from modules.http.probe import (
    probe_host,
)


# ==========================================================
# Probe One Host
# ==========================================================

def probe_one_host(
    host: str,
):
    """
    Probe a single host.

    Returns:
        tuple[str, dict | None]
    """

    result = probe_host(
        host
    )

    return (
        host,
        result,
    )


# ==========================================================
# Probe All Hosts
# ==========================================================

def probe_hosts(
    hosts: list[str],
):
    """
    Probe all hosts in parallel.

    Returns:
        (
            alive_results,
            failed_hosts,
            elapsed
        )
    """

    info(
        "Starting HTTP Probe..."
    )

    results = {}

    failed = []

    retry_queue = []

    completed = 0

    total = len(
        hosts
    )

    start_time = time.perf_counter()

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

            host = futures[
                future
            ]

            completed += 1

            try:

                hostname, response = (
                    future.result()
                )

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

    # ------------------------------------------------------
    # Retry Queue (Future)
    # ------------------------------------------------------

    if retry_queue:

        info(
            f"Retry Queue: {len(retry_queue)} host(s)"
        )

        # Future:
        # Retry failed hosts here.

    elapsed = round(
        time.perf_counter()
        - start_time,
        2,
    )

    success(
        f"Alive Hosts : {len(results)}"
    )

    success(
        f"Dead Hosts  : {len(failed)}"
    )

    return (
        results,
        failed,
        elapsed,
    )