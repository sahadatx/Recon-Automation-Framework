"""
WAF Manager

Coordinates the complete
WAF Detection pipeline.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import (
    info,
    success,
)

from .analyzer import analyze
from .detector import detect_all
from .filters import filter_results
from .scanner import scan_targets


# ==========================================================
# Run WAF Detection
# ==========================================================

def run_waf_detection(
    targets: list[str],
) -> dict[str, Any]:
    """
    Run the complete WAF Detection pipeline.

    Returns:
        WAF analysis.
    """

    if not targets:

        return analyze(
            results=[],
            elapsed=0,
        )

    info(
        "Starting WAF Detection..."
    )

    start = perf_counter()

    # ------------------------------------------------------
    # Scan Targets
    # ------------------------------------------------------

    info(
        "Scanning targets..."
    )

    scans = scan_targets(
        targets
    )

    # ------------------------------------------------------
    # Detect WAF
    # ------------------------------------------------------

    info(
        "Matching fingerprints..."
    )

    results = detect_all(
        scans
    )

    # ------------------------------------------------------
    # Filter Results
    # ------------------------------------------------------

    info(
        "Filtering results..."
    )

    results = filter_results(
        results
    )

    # ------------------------------------------------------
    # Analyze
    # ------------------------------------------------------

    elapsed = (
        perf_counter()
        - start
    )

    analysis = analyze(
        results=results,
        elapsed=elapsed,
    )

    statistics = analysis[
        "statistics"
    ]

    success(
        f"Targets          : {statistics['targets']}"
    )

    success(
        f"WAF Detected     : {statistics['detected']}"
    )

    success(
        f"Not Detected     : {statistics['not_detected']}"
    )

    success(
        f"Success Rate     : {statistics['success_rate']}%"
    )

    success(
        f"Average Score    : {statistics['average_score']}"
    )

    success(
        f"Highest Score    : {statistics['highest_score']}"
    )

    success(
        f"Elapsed          : {statistics['elapsed']:.2f} sec"
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run_waf_detection",
]