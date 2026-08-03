"""
Crawler Statistics

Generate statistics for crawler results.
"""

from __future__ import annotations

# ==========================================================
# Generate Statistics
# ==========================================================


def generate_statistics(
    results: dict[str, dict],
) -> dict:
    """
    Generate crawler statistics.

    Args:
        results:
            Crawled results grouped by host.

    Returns:
        Aggregated crawler statistics.
    """

    hosts = len(results)

    total_urls = 0

    total_failed = 0

    total_internal = 0

    total_external = 0

    total_javascript = 0

    total_css = 0

    total_forms = 0

    total_emails = 0

    urls_per_host: dict[
        str,
        int,
    ] = {}

    for (
        host,
        result,
    ) in sorted(results.items()):

        statistics = result["statistics"]

        count = len(result["pages"])

        urls_per_host[host] = count

        total_urls += count

        total_failed += statistics["failed"]

        total_internal += statistics["internal_urls"]

        total_external += statistics["external_urls"]

        total_javascript += statistics["javascript"]

        total_css += statistics["css"]

        total_forms += statistics["forms"]

        total_emails += statistics["emails"]

    average_urls_per_host = 0.0

    if hosts:

        average_urls_per_host = round(
            total_urls / hosts,
            2,
        )

    return {
        "hosts": hosts,
        "total_urls": total_urls,
        "average_urls_per_host": (average_urls_per_host),
        "failed": total_failed,
        "internal_urls": total_internal,
        "external_urls": total_external,
        "javascript": total_javascript,
        "css": total_css,
        "forms": total_forms,
        "emails": total_emails,
        "urls_per_host": urls_per_host,
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "generate_statistics",
]
