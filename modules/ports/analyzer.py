"""
Port Scanner Analyzer

Analyze port scan results.
"""

from __future__ import annotations

from typing import Any

from modules.ports.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze Results
# ==========================================================


def analyze(
    results: dict[str, list[dict[str, Any]]],
    failed_hosts: list[str],
) -> dict[str, Any]:
    """
    Analyze port scan results.

    Args:
        results:
            Successful scan results.

        failed_hosts:
            Hosts without open ports.

    Returns:
        Port scan analysis.
    """

    statistics = {
        **generate_statistics(
            results=results,
            failed_hosts=failed_hosts,
        ),
        "open_hosts": sorted(
            results,
        ),
        "closed_hosts": sorted(
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