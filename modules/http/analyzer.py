"""
HTTP Probe Analyzer

Analyze HTTP probe results
and generate a summary.
"""

from __future__ import annotations

from typing import Any

from modules.http.statistics import (
    generate_statistics,
)

# ==========================================================
# Analyze HTTP Results
# ==========================================================


def analyze(
    results: dict[str, dict[str, Any]],
    failed_hosts: list[str],
) -> dict[str, Any]:
    """
    Analyze HTTP probe results.

    Args:
        results:
            Successful HTTP probe results.

        failed_hosts:
            Hosts that failed to respond.

    Returns:
        HTTP analysis.
    """

    statistics = {
        **generate_statistics(
            results=results,
            failed_hosts=failed_hosts,
        ),
        "alive": sorted(
            results,
        ),
        "dead": sorted(
            failed_hosts,
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
