"""
Passive Enumeration Analyzer

Analyze passive enumeration results.
"""

from __future__ import annotations

from typing import Any


# ==========================================================
# Analyze Results
# ==========================================================


def analyze(
    target: str,
    results: dict[str, list[str]],
    unique_subdomains: list[str],
    timings: dict[str, float],
    failed_sources: list[str],
) -> dict[str, Any]:
    """
    Analyze passive enumeration results.
    """

    total_sources = len(
        results,
    )

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

    source_statistics: dict[
        str,
        dict[str, Any],
    ] = {}

    for (
        source,
        subdomains,
    ) in results.items():

        status = (
            "FAILED"
            if source in failed_sources
            else (
                "SUCCESS"
                if subdomains
                else "EMPTY"
            )
        )

        source_statistics[
            source
        ] = {
            "count": len(
                subdomains,
            ),
            "time": timings.get(
                source,
                0.0,
            ),
            "status": status,
        }

    statistics = {
        "target": target,
        "total_sources": total_sources,
        "successful_sources": successful_sources,
        "failed_sources": len(
            failed_sources,
        ),
        "empty_sources": empty_sources,
        "total_subdomains": len(
            unique_subdomains,
        ),
        "sources": source_statistics,
    }

    return {
        "results": unique_subdomains,
        "statistics": statistics,
        "sources": results,
        "failed": sorted(
            failed_sources,
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]