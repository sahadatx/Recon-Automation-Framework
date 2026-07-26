"""
Directory Fuzzing Manager

Coordinates parallel directory
fuzzing, parsing, analysis
and reporting.
"""

from __future__ import annotations

import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from typing import Any

from config.config import (
    MAX_WORKERS,
)

from core.logger import (
    info,
    success,
    warning,
    progress_status,
)

from modules.fuzzing.analyzer import (
    analyze,
)

from modules.fuzzing.filters import (
    apply_filters,
)

from modules.fuzzing.interesting import (
    scan as detect_interesting,
)

from modules.fuzzing.parser import (
    parse_ffuf,
)

from modules.fuzzing.scanner import (
    cleanup,
    scan_target,
)


# ==========================================================
# Process Target
# ==========================================================

def process_target(
    target: str,
) -> tuple[
    str,
    dict[str, Any] | None,
]:
    """
    Scan and analyze
    one target.

    Args:
        target:
            Target URL.

    Returns:
        (
            target,
            analysis,
        )
    """

    scan = scan_target(
        target,
    )

    if not scan["success"]:

        return (
            target,
            None,
        )

    output = scan["output"]

    try:

        parsed = parse_ffuf(
            output,
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
            results,
        )

        analysis = analyze(
            results=results,
            interesting=interesting,
            elapsed=0,
        )

        return (
            target,
            analysis,
        )

    finally:

        cleanup(
            output,
        )


# ==========================================================
# Run Directory Fuzzing
# ==========================================================

def run_fuzzing(
    targets: list[str],
) -> dict[str, Any]:
    """
    Run directory
    fuzzing.

    Args:
        targets:
            Target URLs.

    Returns:
        Analysis dictionary.
    """

    info(
        "Starting Directory Fuzzing..."
    )

    targets = sorted(
        set(targets),
    )

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed: list[str] = []

    completed = 0

    total = len(
        targets,
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
            futures,
        ):

            target = futures[
                future
            ]

            completed += 1

            try:

                hostname, analysis = (
                    future.result()
                )

                if analysis:

                    results[
                        hostname
                    ] = analysis

                    progress_status(
                        completed,
                        total,
                        f"✓ {hostname}",
                    )

                else:

                    failed.append(
                        hostname,
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
                    target,
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

    # ======================================================
    # Overall Statistics
    # ======================================================

    overall: dict[str, Any] = {

        "targets": total,

        "successful": len(
            results,
        ),

        "failed": len(
            failed,
        ),

        "total_results": 0,

        "interesting_files": 0,

        "interesting_directories": 0,

    }

    for analysis in results.values():

        statistics = analysis.get(
            "statistics",
            {},
        )

        overall["total_results"] += statistics.get(
            "total_results",
            0,
        )

        overall["interesting_files"] += statistics.get(
            "interesting_files",
            0,
        )

        overall["interesting_directories"] += statistics.get(
            "interesting_directories",
            0,
        )

    # ======================================================
    # Summary
    # ======================================================

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

    # ======================================================
    # Analysis
    # ======================================================

    analysis = {

        "results": results,

        "statistics": {

            **overall,

            "elapsed": elapsed,

        },

        "failed": failed,

    }

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================

def run(
    targets: list[str],
) -> dict[str, Any]:
    """
    Public entry point for the Directory Fuzzing module.
    """

    return run_fuzzing(
        targets,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_fuzzing",
]