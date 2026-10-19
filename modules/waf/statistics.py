from __future__ import annotations

from collections import Counter
from typing import Any


def vendor_statistics(
    results: list[dict[str, Any]],
) -> dict[str, int]:


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


def confidence_statistics(
    results: list[dict[str, Any]],
) -> dict[str, int]:


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


def generate_statistics(
    results: list[dict[str, Any]],
) -> dict[str, Any]:


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


def empty_statistics() -> dict[str, Any]:


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


__all__ = [
    "generate_statistics",
    "empty_statistics",
]
