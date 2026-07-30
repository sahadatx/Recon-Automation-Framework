"""
Memory Analyzer

Analyze memory usage and generate
optimization recommendations.
"""

from __future__ import annotations

from typing import Any


# ==========================================================
# Memory Thresholds (MB)
# ==========================================================

LOW_MEMORY = 100.0
MEDIUM_MEMORY = 250.0
HIGH_MEMORY = 500.0


# ==========================================================
# Analyze Memory
# ==========================================================


def analyze_memory(
    snapshot: dict[str, float],
) -> dict[str, Any]:
    """
    Analyze memory usage.

    Args:
        snapshot:
            Memory snapshot from MemoryProfiler.

    Returns:
        Memory analysis.
    """

    current = snapshot.get(
        "current_mb",
        0.0,
    )

    peak = snapshot.get(
        "peak_mb",
        0.0,
    )

    difference = peak - current

    status = "Excellent"
    grade = "A"
    recommendations: list[str] = []

    if peak >= HIGH_MEMORY:

        status = "High"
        grade = "D"

        recommendations.extend(
            [
                "Reduce large in-memory collections.",
                "Process data in smaller batches.",
                "Use generators instead of large lists.",
                "Release temporary objects as early as possible.",
            ]
        )

    elif peak >= MEDIUM_MEMORY:

        status = "Moderate"
        grade = "B"

        recommendations.extend(
            [
                "Review large dictionaries and lists.",
                "Consider lazy loading where possible.",
                "Reuse objects instead of recreating them.",
            ]
        )

    elif peak >= LOW_MEMORY:

        status = "Good"
        grade = "A"

        recommendations.append(
            "Memory usage is healthy."
        )

    else:

        status = "Excellent"
        grade = "A+"

        recommendations.append(
            "Memory usage is excellent."
        )

    return {
        "memory": {
            "current_mb": round(
                current,
                2,
            ),
            "peak_mb": round(
                peak,
                2,
            ),
            "difference_mb": round(
                difference,
                2,
            ),
        },
        "analysis": {
            "status": status,
            "grade": grade,
            "recommendations": recommendations,
        },
    }


# ==========================================================
# Summary
# ==========================================================


def summary(
    analysis: dict[str, Any],
) -> str:
    """
    Return a human-readable summary.
    """

    memory = analysis[
        "memory"
    ]

    result = analysis[
        "analysis"
    ]

    return (
        f"Status: {result['status']} | "
        f"Grade: {result['grade']} | "
        f"Current: {memory['current_mb']:.2f} MB | "
        f"Peak: {memory['peak_mb']:.2f} MB"
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze_memory",
    "summary",
]