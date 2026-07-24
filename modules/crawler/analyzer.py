"""
Crawler Analyzer

Analyze crawler results and generate a summary.
"""

from __future__ import annotations

from modules.crawler.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze Crawler Results
# ==========================================================

def analyze(
    results: dict[str, dict],
    elapsed: float,
) -> dict:
    """
    Analyze crawler results.

    Args:
        results:
            Crawled results grouped by host.

        elapsed:
            Total crawl time.

    Returns:
        Complete crawler analysis.
    """

    statistics = generate_statistics(
        results=results,
    )

    return {

        "hosts": statistics[
            "hosts"
        ],

        "total_urls": statistics[
            "total_urls"
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