"""
Dashboard Analyzer

Analyze the generated report for the Dashboard module.
"""

from __future__ import annotations

from typing import Any

from .statistics import (
    empty_statistics,
    generate_statistics,
)

# ==========================================================
# Analyze Dashboard
# ==========================================================


def analyze(
    report: dict[str, Any],
) -> dict[str, Any]:
    """
    Analyze dashboard data.

    Args:
        report:
            Generated report.

    Returns:
        Dashboard analysis.
    """

    if not report:

        return {
            "results": {},
            "statistics": empty_statistics(),
        }

    # ======================================================
    # Report Structure
    #
    # report
    #   └── modules
    #         ├── analysis
    #         ├── statistics
    #         └── performance
    #
    # Dashboard only uses analysis modules.
    # ======================================================

    report_modules = report.get(
        "modules",
        {},
    )

    modules = report_modules.get(
        "analysis",
        {},
    )

    statistics = generate_statistics(
        report,
    )

    passive = modules.get(
        "passive",
        {},
    )

    target = passive.get(
        "statistics",
        {},
    ).get(
        "target",
        "",
    )

    dashboard = {
        "target": target,
        "metadata": report.get(
            "metadata",
            {},
        ),
        "modules": modules,
        "module_count": len(
            modules,
        ),
        "module_names": sorted(
            modules.keys(),
        ),
    }

    return {
        "results": dashboard,
        "statistics": statistics,
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]
