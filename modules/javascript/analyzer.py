"""
JavaScript Analyzer

Analyze JavaScript results and generate a summary.
"""

from __future__ import annotations

from typing import Any

from modules.javascript.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze JavaScript Results
# ==========================================================


def analyze(
    results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze JavaScript results.

    Args:
        results:
            JavaScript analysis results.

    Returns:
        JavaScript analysis.
    """

    return {
        "results": results,
        "statistics": generate_statistics(
            results=results,
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]