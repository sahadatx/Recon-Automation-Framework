from __future__ import annotations

from typing import Any


def empty_statistics() -> dict[str, Any]:


    return {
        "total_results": 0,
        "status_codes": {},
        "responses": {
            "minimum": 0,
            "maximum": 0,
            "average": 0,
        },
        "interesting_files": 0,
        "interesting_directories": 0,
        "interesting_total": 0,
    }


def status_statistics(
    results: list[dict[str, Any]],
) -> dict[str, int]:


    statistics: dict[str, int] = {}

    for result in results:

        status = str(
            result.get(
                "status",
                0,
            )
        )

        statistics[status] = statistics.get(status, 0) + 1

    return dict(
        sorted(
            statistics.items(),
        )
    )


def response_statistics(
    results: list[dict[str, Any]],
) -> dict[str, float]:


    if not results:

        return {
            "minimum": 0,
            "maximum": 0,
            "average": 0,
        }

    sizes = [
        result.get(
            "length",
            0,
        )
        for result in results
    ]

    return {
        "minimum": min(sizes),
        "maximum": max(sizes),
        "average": round(
            sum(sizes) / len(sizes),
            2,
        ),
    }


def generate_statistics(
    results: list[dict[str, Any]],
    interesting: dict[str, Any],
) -> dict[str, Any]:


    statistics = empty_statistics()

    interesting_statistics = interesting.get(
        "statistics",
        {},
    )

    statistics.update(
        {
            "total_results": len(results),
            "status_codes": status_statistics(results),
            "responses": response_statistics(results),
            "interesting_files": interesting_statistics.get(
                "interesting_files",
                0,
            ),
            "interesting_directories": interesting_statistics.get(
                "interesting_directories",
                0,
            ),
            "interesting_total": interesting_statistics.get(
                "total",
                0,
            ),
        }
    )

    return statistics


__all__ = [
    "empty_statistics",
    "status_statistics",
    "response_statistics",
    "generate_statistics",
]
