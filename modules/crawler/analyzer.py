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
    elapsed: float,
) -> dict[str, Any]:
    """
    Analyze crawler results.

    Args:
        results:
            Crawled results grouped by host.

        elapsed:
            Total crawl time.

    Returns:
        Crawler analysis.
    """

    statistics = generate_statistics(
        results=results,
    )

    statistics["elapsed"] = elapsed

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