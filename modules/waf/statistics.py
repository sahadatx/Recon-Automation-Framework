"""
WAF Detection Statistics

Generate summary statistics
for WAF Detection.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

# ==========================================================
# Vendor Statistics
# ==========================================================


def vendor_statistics(
    results: list[dict[str, Any]],
) -> dict[str, int]:
    """
    Count detected WAF vendors.

    Args:
        results:
            WAF detection results.

    Returns:
        Vendor counts.
    """

    vendors = [result["vendor"] for result in results if result.get("vendor")]

    return dict(
        sorted(
            Counter(vendors).items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )
    )


# ==========================================================
# Confidence Statistics
# ==========================================================


def confidence_statistics(
    results: list[dict[str, Any]],
) -> dict[str, int]:
    """
    Count confidence levels.

    Args:
        results:
            WAF detection results.

    Returns:
        Confidence counts.
    """

    order = [
        "High",
        "Medium",
        "Low",
        "Unknown",
    ]

    counter = Counter(
        result.get(
            "confidence",
            "Unknown",
        )
        for result in results
    )

    return {level: counter[level] for level in order if counter[level]}


# ==========================================================
# Generate Statistics
# ==========================================================


def generate_statistics(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Generate summary statistics.

    Args:
        results:
            WAF detection results.

    Returns:
        Summary statistics.
    """

    total = len(results)

    detected = sum(
        result.get(
            "detected",
            False,
        )
        for result in results
    )

    scores = [
        result.get(
            "score",
            0,
        )
        for result in results
    ]

    average_score = (
        round(
            sum(scores) / total,
            2,
        )
        if total
        else 0.0
    )

    highest_score = max(
        scores,
        default=0,
    )

    return {
        "targets": total,
        "detected": detected,
        "not_detected": total - detected,
        "success_rate": (
            round(
                detected / total * 100,
                2,
            )
            if total
            else 0.0
        ),
        "average_score": average_score,
        "highest_score": highest_score,
        "vendors": vendor_statistics(
            results,
        ),
        "confidence": confidence_statistics(
            results,
        ),
    }


# ==========================================================
# Empty Statistics
# ==========================================================


def empty_statistics() -> dict[str, Any]:
    """
    Return empty statistics.

    Returns:
        Empty statistics dictionary.
    """

    return {
        "targets": 0,
        "detected": 0,
        "not_detected": 0,
        "success_rate": 0.0,
        "average_score": 0.0,
        "highest_score": 0,
        "vendors": {},
        "confidence": {},
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "generate_statistics",
    "empty_statistics",
]
