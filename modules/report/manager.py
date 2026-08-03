#!/usr/bin/env python3

"""
Report Manager

Coordinate report generation.
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext

from .generator import generate_report
from .statistics import generate_statistics

# ==========================================================
# Report Manager
# ==========================================================


def execute(
    context: ExecutionContext,
    analyses: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute the complete
    report workflow.

        Generate Report
              ↓
        Generate Statistics
              ↓
        Store Context
              ↓
        Return Report
    """

    # ------------------------------------------------------
    # Generate Report
    # ------------------------------------------------------

    report = generate_report(
        analyses,
    )

    # ------------------------------------------------------
    # Generate Statistics
    # ------------------------------------------------------

    statistics = generate_statistics(
        report,
    )

    report["statistics"] = statistics

    # ------------------------------------------------------
    # Store Analysis
    # ------------------------------------------------------

    context.set_analysis(
        "report",
        report,
    )

    return report


# ==========================================================
# Public Entry Point
# ==========================================================


def run(
    context: ExecutionContext,
    analyses: dict[str, Any],
) -> dict[str, Any]:
    """
    Public entry point for the
    Report module.
    """

    return execute(
        context,
        analyses,
    )


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "run",
    "execute",
]
