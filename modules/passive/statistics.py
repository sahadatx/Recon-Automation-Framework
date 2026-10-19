from typing import Any


def generate_statistics(
    results: dict[str, list[str]],
    timings: dict[str, float],
    failed_sources: list[str],
) -> dict[str, Any]:


    statistics: dict[str, dict[str, Any]] = {}

    successful_sources = 0
    empty_sources = 0

    for source, subdomains in results.items():

        if source in failed_sources:

            status = "FAILED"

        elif subdomains:

            status = "SUCCESS"
            successful_sources += 1

        else:

            status = "EMPTY"
            empty_sources += 1

        statistics[source] = {
            "count": len(subdomains),
            "time": round(
                timings.get(
                    source,
                    0.0,
                ),
                2,
            ),
            "status": status,
        }

    return {
        "total_sources": len(results),
        "successful_sources": successful_sources,
        "failed_sources": len(failed_sources),
        "empty_sources": empty_sources,
        "statistics": statistics,
    }


__all__ = [
    "generate_statistics",
]
