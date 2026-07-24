"""
JavaScript Statistics

Generate statistics for JavaScript analysis results.
"""

from __future__ import annotations


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    results: dict[str, dict],
) -> dict:
    """
    Generate JavaScript statistics.

    Args:
        results:
            JavaScript analysis results.

    Returns:
        Aggregated JavaScript statistics.
    """

    processed_files = len(
        results
    )

    total_urls = 0

    total_comments = 0

    total_strings = 0

    total_source_maps = 0

    total_endpoints = 0

    total_interesting_files = 0

    total_interesting_directories = 0

    total_secret_types = 0

    total_secrets = 0

    urls_per_file: dict[
        str,
        int,
    ] = {}

    for (
        javascript,
        metadata,
    ) in sorted(
        results.items()
    ):

        analysis = metadata.get(
            "analysis",
            {},
        )

        statistics = analysis.get(
            "statistics",
            {},
        )

        interesting = metadata.get(
            "interesting",
            {},
        )

        interesting_statistics = (
            interesting.get(
                "statistics",
                {},
            )
        )

        secrets = metadata.get(
            "secrets",
            {},
        )

        secret_statistics = (
            secrets.get(
                "statistics",
                {},
            )
        )

        count = len(
            analysis.get(
                "urls",
                [],
            )
        )

        urls_per_file[
            javascript
        ] = count

        total_urls += statistics.get(
            "urls",
            0,
        )

        total_comments += statistics.get(
            "comments",
            0,
        )

        total_strings += statistics.get(
            "strings",
            0,
        )

        total_source_maps += statistics.get(
            "source_maps",
            0,
        )

        total_endpoints += statistics.get(
            "endpoints",
            0,
        )

        total_interesting_files += (
            interesting_statistics.get(
                "interesting_files",
                0,
            )
        )

        total_interesting_directories += (
            interesting_statistics.get(
                "interesting_directories",
                0,
            )
        )

        total_secret_types += (
            secret_statistics.get(
                "secret_types",
                0,
            )
        )

        total_secrets += (
            secret_statistics.get(
                "total_secrets",
                0,
            )
        )

    average_urls_per_file = 0.0

    if processed_files:

        average_urls_per_file = round(

            total_urls
            / processed_files,

            2,

        )

    return {

        "processed_files": processed_files,

        "urls": total_urls,

        "average_urls_per_file": (
            average_urls_per_file
        ),

        "comments": total_comments,

        "strings": total_strings,

        "source_maps": total_source_maps,

        "endpoints": total_endpoints,

        "interesting_files": (
            total_interesting_files
        ),

        "interesting_directories": (
            total_interesting_directories
        ),

        "secret_types": (
            total_secret_types
        ),

        "total_secrets": (
            total_secrets
        ),

        "urls_per_file": (
            urls_per_file
        ),

    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "generate_statistics",
]