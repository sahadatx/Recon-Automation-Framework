"""
HTTP Probe Analyzer

Analyze HTTP probe results and generate a summary.
"""

from __future__ import annotations

from modules.http.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze HTTP Results
# ==========================================================

def analyze(
    results: dict[str, dict],
    failed_hosts: list[str],
    elapsed: float,
) -> dict:
    """
    Analyze HTTP probe results.

    Args:
        results: Successful HTTP probe results.
        failed_hosts: Hosts that failed to respond.
        elapsed: Total probe time.

    Returns:
        HTTP analysis.
    """

    statistics = generate_statistics(
        results=results,
        failed_hosts=failed_hosts,
    )

    return {
        "alive_hosts": statistics[
            "alive_hosts"
        ],
        "dead_hosts": statistics[
            "dead_hosts"
        ],
        "scan_time": elapsed,
        "results": results,
        "statistics": statistics,
        "alive": sorted(
            results.keys()
        ),
        "dead": sorted(
            failed_hosts
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]