#!/usr/bin/env python3

"""
Directory Fuzzing Manager

Coordinate parallel directory
fuzzing and analysis.
"""

from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import (
    info,
    progress_status,
    success,
    warning,
)

from modules.fuzzing.analyzer import analyze
from modules.fuzzing.filters import apply_filters
from modules.fuzzing.interesting import (
    scan as detect_interesting,
)
from modules.fuzzing.parser import parse_ffuf
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
    Scan and analyze one target.
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
            ),
        )

        interesting = detect_interesting(
            results,
        )

        analysis = analyze(
            results=results,
            interesting=interesting,
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
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Execute the complete directory
    fuzzing workflow.

        Scan
            ↓
        Analyze
            ↓
        Store Context
            ↓
        Return Analysis
    """

    info("Starting Directory Fuzzing...")

    targets = sorted(
        set(
            targets,
        ),
    )

    if not targets:

        warning("No targets supplied.")

        analysis = {
            "results": {},
            "statistics": {
                "targets": 0,
                "successful": 0,
                "failed": 0,
                "total_results": 0,
                "interesting_files": 0,
                "interesting_directories": 0,
            },
            "failed": [],
        }

        context.set_analysis(
            "fuzzing",
            analysis,
        )

        return analysis

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Shared thread pool is not initialized.")

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed: list[str] = []

    completed = 0

    total = len(
        targets,
    )

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

        target = futures[future]

        completed += 1

        try:

            (
                hostname,
                analysis,
            ) = future.result()

            if analysis is not None:

                results[hostname] = analysis

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
                f"{target}: {error}",
            )

            failed.append(
                target,
            )

            progress_status(
                completed,
                total,
                f"✗ {target}",
            )

    overall: dict[str, Any] = {
        "targets": total,
        "successful": len(results),
        "failed": len(failed),
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

    success(f"Targets                  : {overall['targets']}")

    success(f"Successful               : {overall['successful']}")

    success(f"Failed                   : {overall['failed']}")

    success(f"Discovered Paths         : {overall['total_results']}")

    success(f"Interesting Files        : {overall['interesting_files']}")

    success(f"Interesting Directories  : {overall['interesting_directories']}")

    analysis = {
        "results": results,
        "statistics": overall,
        "failed": sorted(
            failed,
        ),
    }

    context.set_analysis(
        "fuzzing",
        analysis,
    )

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================


def run(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Public entry point for the
    Directory Fuzzing module.
    """

    return run_fuzzing(
        context,
        targets,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_fuzzing",
]
