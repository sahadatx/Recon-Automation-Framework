"""
Technology Detection Analyzer

Analyze technology detection results.
"""

from __future__ import annotations

from modules.tech.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze Results
# ==========================================================

def analyze(
    results: dict,
    failed_hosts: list[str],
    elapsed: float,
) -> dict:
    """
    Analyze technology detection results.

    Args:
        results: Successful detection results.
        failed_hosts: Failed hosts.
        elapsed: Total execution time.

    Returns:
        Analysis dictionary.
    """

    statistics = generate_statistics(
        results=results,
        failed_hosts=failed_hosts,
    )

    technologies = sorted(
        {
            technology
            for data in results.values()
            for technology in data.get(
                "technologies",
                [],
            )
        }
    )

    return {
        "hosts_analyzed": (
            len(results)
            + len(failed_hosts)
        ),
        "failed_hosts": len(
            failed_hosts
        ),
        "scan_time": elapsed,
        "results": results,
        "statistics": statistics,
        "technologies": technologies,
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]