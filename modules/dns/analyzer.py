from __future__ import annotations

from typing import Any

from modules.dns.statistics import generate_statistics


def analyze(
    results: dict[str, dict[str, list[str]]],
    failed_hosts: list[str],
) -> dict[str, Any]:


    statistics = {
        **generate_statistics(
            results=results,
            failed_hosts=failed_hosts,
        ),
        "unresolved": sorted(
            failed_hosts,
        ),
    }

    return {
        "results": results,
        "statistics": statistics,
    }


__all__ = [
    "analyze",
]
