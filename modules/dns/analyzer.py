"""
DNS Resolution Analyzer

Analyze DNS resolution results and generate a summary.
"""

from __future__ import annotations

from typing import Any

from modules.dns.statistics import (
    generate_statistics,
)

# ==========================================================
# Analyze DNS Results
# ==========================================================


def analyze(
    results: dict[str, dict[str, list[str]]],
    failed_hosts: list[str],
) -> dict[str, Any]:
    """
    Analyze DNS resolution results.

    Args:
        results:
            DNS resolution results.

        failed_hosts:
            Hosts that failed to resolve.

    Returns:
        DNS analysis.
    """

    statistics = {
        **generate_statistics(
            results=results,
            failed_hosts=failed_hosts,
        ),
        "unresolved": sorted(
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
