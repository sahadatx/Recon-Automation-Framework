"""
Technology Detection Analyzer

Analyze technology detection results.
"""

from __future__ import annotations

from typing import Any

from modules.tech.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze Results
# ==========================================================


def analyze(
    results: dict[str, dict[str, Any]],
    failed_hosts: list[str],
) -> dict[str, Any]:
    """
    Analyze technology detection results.

    Args:
        results:
            Successful detection results.

        failed_hosts:
            Failed hosts.

    Returns:
        Technology detection analysis.
    """

    statistics = {
        **generate_statistics(
            results=results,
            failed_hosts=failed_hosts,
        ),
        "hosts_analyzed": (
            len(results)
            + len(failed_hosts)
        ),
        "failed_hosts": len(
            failed_hosts,
        ),
        "technologies": sorted(
            {
                technology
                for data in results.values()
                for technology in data.get(
                    "technologies",
                    [],
                )
            }
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