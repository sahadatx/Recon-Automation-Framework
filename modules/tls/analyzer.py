"""
TLS Security Analyzer

Analyze TLS Security results.
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
    Analyze TLS Security results.

    Args:
        results:
            TLS analysis results.

        elapsed:
            Total execution time.

    Returns:
        TLS Security analysis.
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