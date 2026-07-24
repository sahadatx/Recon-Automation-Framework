"""
Directory Fuzzing Analyzer

Analyze Directory
Fuzzing results.
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
    interesting: dict[str, Any],
    elapsed: float,
) -> dict[str, Any]:
    """
    Analyze Directory Fuzzing results.

    Args:
        results:
            Parsed fuzzing results.

        interesting:
            Interesting findings.

        elapsed:
            Execution time.

    Returns:
        Analysis results.
    """

    statistics = {
        **generate_statistics(
            results,
            interesting,
        ),
        "elapsed": round(
            elapsed,
            2,
        ),
    }

    return {
        "results": results,
        "interesting": interesting,
        "statistics": statistics,
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]