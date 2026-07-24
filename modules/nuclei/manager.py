"""
Nuclei Manager
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
from .parser import parse_nuclei
from .scanner import (
    cleanup,
    scan_target,
)


# ==========================================================
# Process Target
# ==========================================================

def process_target(
    target: str,
) -> tuple[str, list[dict[str, Any]] | None]:
    """
    Scan and process one target.
    """

    scan = scan_target(target)

    if not scan["success"]:
        return target, None

    output = scan["output"]

    parsed = parse_nuclei(output)

    cleanup(output)

    if parsed is None:
        return target, None

    findings = apply_filters(
        parsed.get(
            "findings",
            [],
        )
    )

    return target, findings


# ==========================================================
# Collect Findings
# ==========================================================

def collect_findings(
    results: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """
    Merge findings from all targets.
    """

    findings: list[dict[str, Any]] = []

    for target_findings in results.values():
        findings.extend(target_findings)

    return findings


# ==========================================================
# Run Nuclei
# ==========================================================

def run_nuclei(
    targets: list[str],
) -> dict[str, Any]:
    """
    Run Nuclei against targets.
    """

    if not targets:

        warning("No targets supplied.")

        return analyze(
            results=[],
            failed=[],
            elapsed=0,
        )

    info(
        "Starting Nuclei Scan..."
    )

    targets = sorted(
        set(targets)
    )

    results: dict[
        str,
        list[dict[str, Any]],
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

                hostname, findings = (
                    future.result()
                )

                if findings is not None:

                    results[
                        hostname
                    ] = findings

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



            except KeyboardInterrupt:

                warning(
                    "Scan interrupted."
                )

                raise

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

    findings = collect_findings(
        results
    )

    analysis = analyze(
        results=findings,
        failed=failed,
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
        f"Targets      : {statistics['total_targets']}"
    )

    success(
        f"Successful   : {statistics['successful']}"
    )

    success(
        f"Failed       : {statistics['failed']}"
    )

    success(
        f"Findings     : {statistics['total_findings']}"
    )

    success(
        f"Elapsed      : {statistics['elapsed']:.2f} sec"
    )

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

    target_statistics = analysis[
        "statistics"
    ].get(
        "target_statistics",
        {},
    )

    return sorted(
        target_statistics.keys()
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
# Exports
# ==========================================================

__all__ = [
    "run_nuclei",
    "successful_targets",
    "failed_targets",
]