"""
Technology Detection Manager

Coordinates parallel technology detection.
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
    success,
    warning,
    progress_status,
)

from modules.tech.detector import (
    detect_technologies,
)


# ==========================================================
# Detect One Host
# ==========================================================

def detect_one_host(
    host: str,
    response: dict,
):
    """
    Detect technologies for one host.

    Returns:
        tuple[str, dict]
    """

    technologies = detect_technologies(
        response
    )

    return (
        host,
        technologies,
    )


# ==========================================================
# Detect All Hosts
# ==========================================================

def detect_hosts(
    http_results: dict,
):
    """
    Detect technologies for every alive host.

    Args:
        http_results:
            Output of HTTP Probe module.

    Returns:
        (
            results,
            failed,
            elapsed
        )
    """

    info(
        "Starting Technology Detection..."
    )

    results = {}

    failed = []

    completed = 0

    total = len(http_results)

    start_time = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {

            executor.submit(
                detect_one_host,
                host,
                response,
            ): host

            for host, response
            in http_results.items()

        }

        for future in as_completed(
            futures
        ):

            host = futures[
                future
            ]

            completed += 1

            try:

                hostname, technologies = (
                    future.result()
                )

                results[
                    hostname
                ] = technologies

                tech_count = len(
                    technologies.get(
                        "technologies",
                        [],
                    )
                )

                progress_status(
                    completed,
                    total,
                    (
                        f"✓ {hostname} "
                        f"[{tech_count} tech]"
                    ),
                )

            except Exception as error:

                failed.append(
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
        f"Technology Detection Completed : {len(results)}"
    )

    success(
        f"Failed Hosts : {len(failed)}"
    )

    return (
        results,
        failed,
        elapsed,
    )


# ==========================================================
# Statistics
# ==========================================================

def get_statistics(
    results: dict,
):
    """
    Generate technology statistics.

    Returns:
        dict
    """

    technologies = {}

    security_headers = {}

    for data in results.values():

        # -------------------------------------
        # Technologies
        # -------------------------------------

        for tech in data.get(
            "technologies",
            [],
        ):

            technologies[
                tech
            ] = technologies.get(
                tech,
                0,
            ) + 1

        # -------------------------------------
        # Security Headers
        # -------------------------------------

        for header in data.get(
            "security_headers",
            [],
        ):

            security_headers[
                header
            ] = security_headers.get(
                header,
                0,
            ) + 1

    return {

        "technologies":

            dict(

                sorted(

                    technologies.items(),

                    key=lambda item: item[1],

                    reverse=True,

                )

            ),

        "security_headers":

            dict(

                sorted(

                    security_headers.items(),

                    key=lambda item: item[1],

                    reverse=True,

                )

            ),

    }