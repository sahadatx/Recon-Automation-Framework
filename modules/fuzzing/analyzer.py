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
) -> dict[str, Any]:
    """
    Analyze Directory Fuzzing results.

    Args:
        results:
            Parsed fuzzing results.

        interesting:
            Interesting findings.

    Returns:
        Analysis results.
    """

    return {
        "results": results,
        "interesting": interesting,
        "statistics": generate_statistics(
            results,
            interesting,
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]
