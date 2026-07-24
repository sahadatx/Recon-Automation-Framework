"""
Virtual Host Discovery Manager
"""

from __future__ import annotations

import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from typing import Any

from config.config import MAX_WORKERS

from core.logger import (
    info,
    progress_status,
    success,
    warning,
)

from .analyzer import analyze
from .filters import apply_filters
from .interesting import (
    scan as detect_interesting,
)
from .parser import parse_ffuf
from .scanner import (
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
    Scan a single target.

    Returns:
        (target, result)
    """

    scan = scan_target(target)

    if not scan["success"]:
        return (
            target,
            None,
        )

    output = scan["output"]

    try:

        parsed = parse_ffuf(output)

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

        return (
            target,
            {
                "results": results,
                "interesting": interesting,
            },
        )

    finally:

        # cleanup(output)
        pass


# ==========================================================
# Collect Results
# ==========================================================

def collect_results(
    results: dict[
        str,
        dict[str, Any],
    ],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """
    Merge all results.
    """

    findings: list[
        dict[str, Any]
    ] = []

    interesting: list[
        dict[str, Any]
    ] = []

    for data in results.values():

        findings.extend(
            data.get(
                "results",
                [],
            )
        )

        interesting.extend(
            data.get(
                "interesting",
                [],
            )
        )

    return (
        findings,
        interesting,
    )


# ==========================================================
# Run Virtual Host Discovery
# ==========================================================

def run_vhosts(
    targets: list[str],
) -> dict[str, Any]:
    """
    Run Virtual Host Discovery.
    """

    if not targets:

        warning(
            "No targets supplied."
        )

        return analyze(
            results=[],
            interesting=[],
            elapsed=0,
        )

    info(
        "Starting Virtual Host Discovery..."
    )

    targets = sorted(
        set(targets)
    )

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed: list[str] = []

    completed = 0

    total = len(targets)

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

            target = futures[future]

            completed += 1

            try:

                hostname, data = (
                    future.result()
                )

                if data is not None:

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

    elapsed = (
        time.perf_counter()
        - start_time
    )

    findings, interesting = (
        collect_results(
            results
        )
    )

    analysis = analyze(
        results=findings,
        interesting=interesting,
        elapsed=elapsed,
    )

    statistics = analysis[
        "statistics"
    ]

    statistics.update(
        {
            "total_targets": total,
            "successful": len(results),
            "failed": len(failed),
        }
    )

    success(
        f"Targets             : {total}"
    )

    success(
        f"Successful          : {len(results)}"
    )

    success(
        f"Failed              : {len(failed)}"
    )

    success(
        f"Discovered Hosts    : "
        f"{statistics['total_results']}"
    )

    success(
        f"Interesting Hosts   : "
        f"{statistics['interesting_hosts']}"
    )

    success(
        f"Elapsed             : "
        f"{statistics['elapsed']:.2f} sec"
    )

    analysis["failed"] = failed

    return analysis


# ==========================================================
# Successful Targets
# ==========================================================

def successful_targets(
    analysis: dict[str, Any],
) -> list[str]:
    """
    Return successful targets.
    """

    results = analysis.get(
        "results",
        [],
    )

    return sorted(
        {
            result.get(
                "target",
                "",
            )
            for result in results
            if result.get("target")
        }
    )


# ==========================================================
# Failed Targets
# ==========================================================

def failed_targets(
    analysis: dict[str, Any],
) -> list[str]:
    """
    Return failed targets.
    """

    return sorted(
        analysis.get(
            "failed",
            [],
        )
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run_vhosts",
    "successful_targets",
    "failed_targets",
]
