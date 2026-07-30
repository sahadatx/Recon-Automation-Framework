#!/usr/bin/env python3

"""
WAF Manager

Coordinate WAF detection
and analysis.
"""

from __future__ import annotations

from core.context import ExecutionContext

from core.logger import (
    info,
    success,
)

from .analyzer import (
    analyze,
)

from .detector import (
    detect_all,
)

from .filters import (
    filter_results,
)

from .scanner import (
    scan_targets,
)


# ==========================================================
# Run WAF Detection
# ==========================================================


def run_waf_detection(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, object]:
    """
    Execute the complete
    WAF detection workflow.

        Scan
            ↓
        Detect
            ↓
        Filter
            ↓
        Analyze
            ↓
        Store Context
            ↓
        Return Analysis
    """

    if not targets:

        analysis = analyze(
            results=[],
        )

        context.set_analysis(
            "waf",
            analysis,
        )

        return analysis

    info(
        "Starting WAF Detection...",
    )

    # ------------------------------------------------------
    # Scan Targets
    # ------------------------------------------------------

    scans = scan_targets(
        context,
        targets,
    )

    # ------------------------------------------------------
    # Detect WAF
    # ------------------------------------------------------

    results = detect_all(
        scans,
    )

    # ------------------------------------------------------
    # Filter Results
    # ------------------------------------------------------

    results = filter_results(
        results,
    )

    # ------------------------------------------------------
    # Analyze
    # ------------------------------------------------------

    analysis = analyze(
        results=results,
    )

    context.set_analysis(
        "waf",
        analysis,
    )

    statistics = analysis[
        "statistics"
    ]

    success(
        f"Targets          : {statistics['targets']}",
    )

    success(
        f"WAF Detected     : {statistics['detected']}",
    )

    success(
        f"Not Detected     : {statistics['not_detected']}",
    )

    success(
        f"Success Rate     : {statistics['success_rate']}%",
    )

    success(
        f"Average Score    : {statistics['average_score']}",
    )

    success(
        f"Highest Score    : {statistics['highest_score']}",
    )

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================


def run(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, object]:
    """
    Public entry point for the
    WAF module.
    """

    return run_waf_detection(
        context,
        targets,
    )


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "run",
    "run_waf_detection",
]