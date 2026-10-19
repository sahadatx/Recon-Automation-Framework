from __future__ import annotations

from typing import Any

from .statistics import generate_statistics


def analyze(
    results: list[dict[str, Any]],
    interesting: dict[str, Any],
) -> dict[str, Any]:


    return {
        "results": results,
        "interesting": interesting,
        "statistics": generate_statistics(
            results,
            interesting,
        ),
    }


__all__ = [
    "analyze",
]
