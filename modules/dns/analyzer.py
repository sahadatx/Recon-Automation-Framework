"""
DNS Resolution Analyzer

Analyze DNS resolution results and generate a summary.
"""

from __future__ import annotations

from modules.dns.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze DNS Results
# ==========================================================

def analyze(
    results: dict[str, dict[str, list[str]]],
    failed_hosts: list[str],
    elapsed: float,
) -> dict:
    """
    Analyze DNS resolution results.

    Args:
        results: DNS resolution results.
        failed_hosts: Hosts that failed to resolve.
        elapsed: Total scan time.

    Returns:
        DNS analysis.
    """

    statistics = generate_statistics(
        results=results,
        failed_hosts=failed_hosts,
    )

    return {
        "resolved_hosts": statistics[
            "resolved_hosts"
        ],
        "failed_hosts": statistics[
            "failed_hosts"
        ],
        "scan_time": elapsed,
        "results": results,
        "statistics": statistics,
        "unresolved": sorted(
            failed_hosts
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]