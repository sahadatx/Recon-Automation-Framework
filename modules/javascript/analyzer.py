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
    elapsed: float,
) -> dict[str, Any]:
    """
    Analyze JavaScript results.

    Args:
        results:
            JavaScript analysis results.

        elapsed:
            Total analysis time.

    Returns:
        JavaScript analysis.
    """

    statistics = {
        **generate_statistics(
            results=results,
        ),
        "elapsed": elapsed,
    }

    return {

        "results": results,

        "statistics": statistics,

    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]