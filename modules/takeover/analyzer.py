"""
Subdomain Takeover Analyzer

Analyzes takeover detection
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
) -> dict[str, Any]:
    """
    Analyze takeover
    detection results.

    Returns:
        Analysis dictionary.
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