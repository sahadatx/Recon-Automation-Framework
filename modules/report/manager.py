"""
Report Manager

Main entry point for the Report Generator module.
"""

from __future__ import annotations

from typing import Any

from .exporter import (
    export_all,
    show_summary,
)

from .generator import (
    generate_report,
)

from .statistics import (
    generate_statistics,
)


# ==========================================================
# Report Manager
# ==========================================================


def execute(
    analyses: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate and export the final report.
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
    # Export Report
    # ------------------------------------------------------

    export_all(
        report=report,
        statistics=statistics,
    )

    # ------------------------------------------------------
    # Console Summary
    # ------------------------------------------------------

    show_summary(
        statistics,
    )

    return report


# ==========================================================
# Public Entry Point
# ==========================================================

def run(
    analyses: dict[str, Any],
) -> dict[str, Any]:
    """
    Public entry point for the Report module.
    """

    return execute(
        analyses,
    )


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "run",
    "execute",
]