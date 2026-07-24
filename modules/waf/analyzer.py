"""
WAF Detection Analyzer

Analyze WAF detection results.
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
    Analyze WAF detection results.

    Args:
        results:
            WAF detection results.

        elapsed:
            Total execution time.

    Returns:
        WAF detection analysis.
    """

    statistics = {
        **generate_statistics(
            results,
        ),
        "elapsed": round(
            elapsed,
            2,
        ),
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