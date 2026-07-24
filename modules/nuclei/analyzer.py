"""
Nuclei Analyzer
"""

from __future__ import annotations

from typing import Any

from .statistics import generate_statistics


# ==========================================================
# Analyze Results
# ==========================================================

def analyze(
    results: list[dict[str, Any]],
    failed: list[str],
    elapsed: float,
) -> dict[str, Any]:
    """
    Analyze Nuclei scan results.

    Args:
        results:
            Parsed findings.

        failed:
            Failed targets.

        elapsed:
            Total execution time.

    Returns:
        Analysis dictionary.
    """

    statistics = {
        **generate_statistics(results),
        "elapsed": round(elapsed, 2),
    }

    return {
        "results": results,
        "statistics": statistics,
        "failed": failed,
    }


# ==========================================================
# Exports
# ==========================================================

__all__ = [
    "analyze",
]