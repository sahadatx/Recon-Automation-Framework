"""
Port Scanner Analyzer

Analyze port scan results.
"""

from __future__ import annotations

from modules.ports.statistics import (
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
    Analyze port scan results.

    Args:
        results: Successful scan results.
        failed_hosts: Hosts without open ports.
        elapsed: Total scan time.

    Returns:
        Analysis dictionary.
    """

    statistics = generate_statistics(
        results=results,
        failed_hosts=failed_hosts,
    )

    return {
        "hosts_scanned": (
            len(results)
            + len(failed_hosts)
        ),
        "hosts_with_open_ports": len(
            results
        ),
        "hosts_without_open_ports": len(
            failed_hosts
        ),
        "scan_time": elapsed,
        "results": results,
        "statistics": statistics,
        "open_hosts": sorted(
            results.keys()
        ),
        "closed_hosts": sorted(
            failed_hosts
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]