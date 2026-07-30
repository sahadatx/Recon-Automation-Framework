"""
Nuclei Analyzer
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
    failed: list[str],
) -> dict[str, Any]:
    """
    Analyze Nuclei scan results.

    Args:
        results:
            Parsed findings.

        failed:
            Failed targets.

    Returns:
        Analysis dictionary.
    """

    return {
        "results": results,
        "statistics": generate_statistics(
            results,
        ),
        "failed": failed,
    }


# ==========================================================
# Exports
# ==========================================================

__all__ = [
    "analyze",
]