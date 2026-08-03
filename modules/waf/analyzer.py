"""
WAF Detection Analyzer

Analyze WAF detection results.
"""

from __future__ import annotations

from typing import Any

from .statistics import generate_statistics

# ==========================================================
# Analyze Results
# ==========================================================


def analyze(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze WAF detection results.

    Args:
        results:
            WAF detection results.

    Returns:
        WAF detection analysis.
    """

    return {
        "results": results,
        "statistics": generate_statistics(
            results,
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]
