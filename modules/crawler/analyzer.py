from __future__ import annotations

from typing import Any

from modules.crawler.statistics import generate_statistics


def analyze(
    results: dict[str, dict[str, Any]],
) -> dict[str, Any]:


    return {
        "results": results,
        "statistics": generate_statistics(
            results=results,
        ),
    }


__all__ = [
    "analyze",
]
