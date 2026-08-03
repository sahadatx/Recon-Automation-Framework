"""
Screenshot Analyzer

Analyze screenshot capture results
and generate final analysis report.
"""

from __future__ import annotations

from typing import Any

from modules.screenshots.statistics import (
    generate_statistics,
)

# ==========================================================
# Analyze Screenshot Results
# ==========================================================


def analyze(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze screenshot results.

    Args:
        results:
            Screenshot capture results.

    Returns:
        Screenshot analysis.
    """

    return {
        "results": results,
        "statistics": generate_statistics(
            results,
        ),
    }


# ==========================================================
# Filter Successful Screenshots
# ==========================================================


def get_successful_screenshots(
    analysis: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Return successfully captured screenshots.

    Args:
        analysis:
            Screenshot analysis.

    Returns:
        List of successful captures.
    """

    return [
        result
        for result in analysis.get(
            "results",
            [],
        )
        if result.get(
            "captured",
            False,
        )
    ]


# ==========================================================
# Filter Failed Screenshots
# ==========================================================


def get_failed_screenshots(
    analysis: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Return failed screenshot captures.

    Args:
        analysis:
            Screenshot analysis.

    Returns:
        List of failed captures.
    """

    return [
        result
        for result in analysis.get(
            "results",
            [],
        )
        if not result.get(
            "captured",
            False,
        )
    ]


# ==========================================================
# Build Dashboard Data
# ==========================================================


def dashboard_data(
    analysis: dict[str, Any],
) -> dict[str, Any]:
    """
    Prepare dashboard-friendly data.

    Args:
        analysis:
            Screenshot analysis.

    Returns:
        Dashboard data.
    """

    statistics = analysis.get(
        "statistics",
        {},
    )

    return {
        "summary": {
            "total": statistics.get(
                "total_targets",
                0,
            ),
            "captured": statistics.get(
                "captured",
                0,
            ),
            "failed": statistics.get(
                "failed",
                0,
            ),
            "success_rate": statistics.get(
                "success_rate",
                0,
            ),
        },
        "performance": {
            "average_time": statistics.get(
                "average_time",
                0,
            ),
            "average_size": statistics.get(
                "average_size",
                0,
            ),
        },
        "status_codes": statistics.get(
            "status_codes",
            {},
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
    "get_successful_screenshots",
    "get_failed_screenshots",
    "dashboard_data",
]
