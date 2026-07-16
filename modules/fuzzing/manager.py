"""
Directory Fuzzing Manager

Coordinates parallel directory fuzzing,
parsing, filtering and reporting.
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
    progress_status,
)

from modules.fuzzing.scanner import (
    scan_target,
    cleanup,
)

from modules.fuzzing.parser import (
    parse_ffuf,
)

from modules.fuzzing.filters import (
    apply_filters,
)

from modules.fuzzing.interesting import (
    scan as detect_interesting,
)

from modules.fuzzing.statistics import (
    generate,
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

            print("[DEBUG] Parser returned None")

            return (
                target,
                None,
            )

        print(
            "[DEBUG] Raw Results:",
            len(
                parsed.get(
                    "results",
                    [],
                )
            )
        )

        results = apply_filters(

            parsed.get(
                "results",
                [],
            )

        )

        print(

            "[DEBUG] Filtered Results:",

            len(results)

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

        pass


# ==========================================================
# Run Directory Fuzzing
# ==========================================================

def run_fuzzing(
    targets: list[str],
):
    """
    Run directory fuzzing against
    multiple targets.

    Returns:
        (
            results,
            overall,
            failed,
            elapsed,
        )
    """

    info(
        "Starting Directory Fuzzing..."
    )

    targets = sorted(
        set(targets)
    )

    results = {}

    failed = []

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

        "interesting_files": 0,

        "interesting_directories": 0,

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

        overall["interesting_files"] += stats.get(

            "interesting_files",

            0,

        )

        overall["interesting_directories"] += stats.get(

            "interesting_directories",

            0,

        )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    from core.logger import (
        success,
    )

    success(
        f"Targets                  : {overall['targets']}"
    )

    success(
        f"Successful               : {overall['successful']}"
    )

    success(
        f"Failed                   : {overall['failed']}"
    )

    success(
        f"Discovered Paths         : {overall['total_results']}"
    )

    success(
        f"Interesting Files        : {overall['interesting_files']}"
    )

    success(
        f"Interesting Directories  : {overall['interesting_directories']}"
    )

    success(
        f"Elapsed                  : {elapsed:.2f} sec"
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