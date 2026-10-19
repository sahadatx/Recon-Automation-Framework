from __future__ import annotations

from typing import Any

from .statistics import generate_statistics


def analyze(
    results: list[dict[str, Any]],
    failed: list[str],
) -> dict[str, Any]:


    return {
        "results": results,
        "statistics": generate_statistics(
            results,
        ),
        "failed": failed,
    }


__all__ = [
    "analyze",
]
