"""
CDN Analyzer

Analyzes all CDN detection
results and generates the
final analysis.
"""

from __future__ import annotations

from typing import Any

from .statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze Results
# ==========================================================

def analyze(
    results: list[dict[str, Any]],
    elapsed: float,
) -> dict[str, Any]:
    """
    Analyze CDN detection results.

    Returns:
        dict[str, Any]
    """

    statistics = {
        **generate_statistics(results),
        "elapsed": round(elapsed, 2),
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