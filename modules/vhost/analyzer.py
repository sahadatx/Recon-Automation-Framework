from __future__ import annotations

from typing import Any

from .statistics import generate_statistics


def analyze(
    results: list[dict[str, Any]],
    interesting: list[dict[str, Any]],
) -> dict[str, Any]:


    statistics = {
        **generate_statistics(
            results=results,
            interesting=interesting,
        ),
        "interesting": interesting,
    }

    return {
        "results": results,
        "statistics": statistics,
    }


__all__ = [
    "analyze",
]
