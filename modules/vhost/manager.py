"""
Virtual Host Discovery Manager

Coordinates parallel virtual host
discovery, parsing, filtering,
statistics and reporting.
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

from modules.vhost.scanner import (
    scan_target,
    cleanup,
)

from modules.vhost.parser import (
    parse_ffuf,
)

from modules.vhost.filters import (
    apply_filters,
)

from modules.vhost.interesting import (
    scan as detect_interesting,
)

from modules.vhost.statistics import (
    generate,
)

from modules.vhost.exporter import (
    export,
)


# ==========================================================
# Process One Target
# ==========================================================

def process_target(
    target: str,
):
    """
    Scan and analyze one target.

    Returns:
        tuple(
            target,
            result | None,
        )
    """

    scan = scan_target(
        target
    )

    if not scan["success"]:

        return (

            target,

            None,

        )

    output = scan["output"]

    try:

        parsed = parse_ffuf(
            output
        )

        if parsed is None:

            return (

                target,

                None,

            )

        results = apply_filters(

            parsed.get(

                "results",

                [],

            )

        )

        interesting = detect_interesting(

            results

        )

        statistics = generate(

            results,

            interesting,

        )

        return (

            target,

            {

                "results": results,

                "interesting": interesting,

                "statistics": statistics,

            },

        )

    finally:

        # cleanup(
        #     output
        # )
        pass



# ==========================================================
# Run Virtual Host Discovery
# ==========================================================

def run_vhosts(
    targets: list[str],
):
    """
    Run Virtual Host Discovery
    against multiple targets.

    Returns:
        (
            results,
            overall,
            failed,
            elapsed,
        )
    """

    info(
        "Starting Virtual Host Discovery..."
    )

    targets = sorted(
        set(targets)
    )

    results = {}

    failed = []

    all_results = []

    all_interesting = []

    completed = 0

    total = len(
        targets
    )

    start_time = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {

            executor.submit(
                process_target,
                target,
            ): target

            for target in targets

        }

        for future in as_completed(
            futures
        ):

            target = futures[
                future
            ]

            completed += 1

            try:

                hostname, data = (
                    future.result()
                )

                if data:

                    results[
                        hostname
                    ] = data

                    all_results.extend(

                        data[
                            "results"
                        ]

                    )

                    all_interesting.extend(

                        data[
                            "interesting"
                        ]

                    )

                    progress_status(

                        completed,

                        total,

                        f"✓ {hostname}",

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

                warning(

                    f"{target}: {error}"

                )

                failed.append(
                    target
                )

                progress_status(

                    completed,

                    total,

                    f"✗ {target}",

                )

    elapsed = round(

        time.perf_counter()

        - start_time,

        2,

    )

    # ------------------------------------------------------
    # Overall Statistics
    # ------------------------------------------------------

    overall = {

        "targets": total,

        "successful": len(
            results
        ),

        "failed": len(
            failed
        ),

        "total_results": 0,

        "interesting_hosts": 0,

        "status_200": 0,

        "status_204": 0,

        "status_301": 0,

        "status_302": 0,

        "status_307": 0,

        "status_401": 0,

        "status_403": 0,

    }

    for data in results.values():

        stats = data.get(

            "statistics",

            {},

        )

        overall["total_results"] += stats.get(

            "total_results",

            0,

        )

        overall["interesting_hosts"] += stats.get(

            "interesting_hosts",

            0,

        )

        overall["status_200"] += stats.get(

            "status_200",

            0,

        )

        overall["status_204"] += stats.get(

            "status_204",

            0,

        )

        overall["status_301"] += stats.get(

            "status_301",

            0,

        )

        overall["status_302"] += stats.get(

            "status_302",

            0,

        )

        overall["status_307"] += stats.get(

            "status_307",

            0,

        )

        overall["status_401"] += stats.get(

            "status_401",

            0,

        )

        overall["status_403"] += stats.get(

            "status_403",

            0,

        )

    # ------------------------------------------------------
    # Export
    # ------------------------------------------------------

    if all_results:

        export(

            all_results,

            all_interesting,

            overall,

        )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    success(

        f"Targets                : {overall['targets']}"

    )

    success(

        f"Successful             : {overall['successful']}"

    )

    success(

        f"Failed                 : {overall['failed']}"

    )

    success(

        f"Discovered Hosts       : {overall['total_results']}"

    )

    success(

        f"Interesting Hosts      : {overall['interesting_hosts']}"

    )

    success(

        f"Elapsed                : {elapsed:.2f} sec"

    )

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return (

        results,

        overall,

        failed,

        elapsed,

    )