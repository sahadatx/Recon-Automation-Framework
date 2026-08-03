"""
Crawler Analyzer

Analyze crawler results and generate a summary.
"""

from __future__ import annotations

from typing import Any

from modules.crawler.statistics import (
    generate_statistics,
)

# ==========================================================
# Analyze Crawler Results
# ==========================================================


def analyze(
    results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze crawler results.

    Args:
        results:
            Crawled results grouped by host.

    Returns:
        Crawler analysis.
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
