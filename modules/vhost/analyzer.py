"""
Virtual Host Discovery Analyzer

Analyze Virtual Host Discovery results.
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
    interesting: list[dict[str, Any]],
    elapsed: float,
) -> dict[str, Any]:
    """
    Analyze Virtual Host Discovery results.
    """

    statistics = {
        **generate_statistics(
            results=results,
            interesting=interesting,
        ),
        "interesting": interesting,
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