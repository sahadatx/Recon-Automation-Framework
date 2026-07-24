"""
JavaScript Analyzer

Analyze JavaScript results and generate a summary.
"""

from __future__ import annotations

from modules.javascript.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze JavaScript Results
# ==========================================================

def analyze(
    results: dict[str, dict],
    elapsed: float,
) -> dict:
    """
    Analyze JavaScript results.

    Args:
        results:
            JavaScript analysis results.

        elapsed:
            Total analysis time.

    Returns:
        Complete JavaScript analysis.
    """

    statistics = generate_statistics(
        results=results,
    )

    return {

        "processed_files": statistics[
            "processed_files"
        ],

        "scan_time": elapsed,

        "results": results,

        "statistics": statistics,

    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]