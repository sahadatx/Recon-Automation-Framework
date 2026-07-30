#!/usr/bin/env python3

"""
CDN Analyzer

Analyzes all CDN detection
results and generates the
final analysis.
"""

from __future__ import annotations

from typing import Any

from .statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze Results
# ==========================================================


def analyze(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze CDN detection results.

    Returns
    -------
    dict[str, Any]
        Complete CDN analysis.
    """

    return {
        "results": results,
        "statistics": generate_statistics(
            results,
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze",
]