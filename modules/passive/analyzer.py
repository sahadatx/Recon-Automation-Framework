"""
Passive Enumeration Analyzer

Analyze passive enumeration results.
"""

from typing import Any


def analyze(
    target: str,
    results: dict[str, list[str]],
    unique_subdomains: list[str],
    timings: dict[str, float],
    failed_sources: list[str],
    total_scan_time: float,
) -> dict[str, Any]:
    """
    Analyze passive enumeration results.

    Args:
        target: Target domain.
        results: Raw results grouped by source.
        unique_subdomains: Unique discovered subdomains.
        timings: Execution time per source.
        failed_sources: Failed source names.
        total_scan_time: Total scan duration.

    Returns:
        Passive enumeration analysis.
    """

    total_sources = len(results)

    successful_sources = sum(
        1
        for subdomains in results.values()
        if subdomains
    )

    empty_sources = sum(
        1
        for subdomains in results.values()
        if not subdomains
    )

    source_statistics = {}

    for source, subdomains in results.items():

        status = (
            "FAILED"
            if source in failed_sources
            else (
                "SUCCESS"
                if subdomains
                else "EMPTY"
            )
        )

        source_statistics[source] = {
            "count": len(subdomains),
            "time": timings.get(source, 0.0),
            "status": status,
        }

    return {
        "target": target,
        "total_sources": total_sources,
        "successful_sources": successful_sources,
        "failed_sources": len(failed_sources),
        "empty_sources": empty_sources,
        "total_subdomains": len(unique_subdomains),
        "scan_time": total_scan_time,
        "subdomains": unique_subdomains,
        "results": results,
        "statistics": source_statistics,
    }