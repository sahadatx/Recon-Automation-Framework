from __future__ import annotations

from typing import Any

from modules.tech.statistics import generate_statistics


def analyze(
    results: dict[str, dict[str, Any]],
    failed_hosts: list[str],
) -> dict[str, Any]:


    statistics = {
        **generate_statistics(
            results=results,
            failed_hosts=failed_hosts,
        ),
        "hosts_analyzed": (len(results) + len(failed_hosts)),
        "failed_hosts": len(
            failed_hosts,
        ),
        "technologies": sorted(
            {
                technology
                for data in results.values()
                for technology in data.get(
                    "technologies",
                    [],
                )
            }
        ),
    }

    return {
        "results": results,
        "statistics": statistics,
    }


__all__ = [
    "analyze",
]
