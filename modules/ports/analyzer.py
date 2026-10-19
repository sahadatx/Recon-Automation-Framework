from __future__ import annotations

from typing import Any

from modules.ports.statistics import generate_statistics


def analyze(
    results: dict[str, list[dict[str, Any]]],
    failed_hosts: list[str],
) -> dict[str, Any]:


    statistics = {
        **generate_statistics(
            results=results,
            failed_hosts=failed_hosts,
        ),
        "open_hosts": sorted(
            results,
        ),
        "closed_hosts": sorted(
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
