"""
Passive Enumeration Exporter

Export passive enumeration results.
"""

from __future__ import annotations

import json

from typing import Any

from .constants import (
    PASSIVE_OUTPUT_DIR,
    RAW_RESULTS_TXT,
    RESULTS_JSON,
    RESULTS_TXT,
    SUBDOMAINS_TXT,
    SUMMARY_TXT,
)


# ==========================================================
# Helpers
# ==========================================================

def create_output_directory() -> None:
    """
    Create output directory.
    """

    PASSIVE_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# Human Readable Results
# ==========================================================

def export_results_txt(
    analysis: dict[str, Any],
) -> None:
    """
    Export human-readable results.
    """

    create_output_directory()

    statistics = analysis["statistics"]
    results = analysis["results"]

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "PASSIVE ENUMERATION RESULTS\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            f"Target : {statistics['target']}\n"
        )

        file.write(
            f"Unique Subdomains : "
            f"{statistics['total_subdomains']}\n\n"
        )

        file.write(
            "Subdomains\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        for subdomain in results:

            file.write(
                f"{subdomain}\n"
            )


# ==========================================================
# JSON Export
# ==========================================================

def export_results_json(
    analysis: dict[str, Any],
) -> None:
    """
    Export JSON results.
    """

    create_output_directory()

    with RESULTS_JSON.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            analysis,
            file,
            indent=4,
        )


# ==========================================================
# Summary
# ==========================================================

def export_summary(
    analysis: dict[str, Any],
) -> None:
    """
    Export summary.
    """

    create_output_directory()

    statistics = analysis["statistics"]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "PASSIVE ENUMERATION SUMMARY\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            f"Target              : {statistics['target']}\n"
        )

        file.write(
            f"Sources             : {statistics['total_sources']}\n"
        )

        file.write(
            f"Successful Sources  : {statistics['successful_sources']}\n"
        )

        file.write(
            f"Failed Sources      : {statistics['failed_sources']}\n"
        )

        file.write(
            f"Empty Sources       : {statistics['empty_sources']}\n"
        )

        file.write(
            f"Unique Subdomains   : {statistics['total_subdomains']}\n"
        )

        file.write(
            f"Scan Time           : {statistics['elapsed']} sec\n"
        )


# ==========================================================
# Subdomains
# ==========================================================

def export_subdomains(
    subdomains: list[str],
) -> None:
    """
    Export merged subdomains.
    """

    create_output_directory()

    with SUBDOMAINS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for subdomain in subdomains:

            file.write(
                f"{subdomain}\n"
            )


# ==========================================================
# Raw Results
# ==========================================================

def export_raw_results(
    sources: dict[str, list[str]],
) -> None:
    """
    Export raw source results.
    """

    create_output_directory()

    with RAW_RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for source, subdomains in sources.items():

            file.write(
                "=" * 70 + "\n"
            )

            file.write(
                f"{source}\n"
            )

            file.write(
                "=" * 70 + "\n"
            )

            for subdomain in subdomains:

                file.write(
                    f"{subdomain}\n"
                )

            file.write(
                "\n"
            )


# ==========================================================
# Export All
# ==========================================================

def export_all(
    analysis: dict[str, Any],
) -> None:
    """
    Export all passive
    enumeration outputs.
    """

    export_results_txt(
        analysis,
    )

    export_results_json(
        analysis,
    )

    export_summary(
        analysis,
    )

    export_subdomains(
        analysis["results"],
    )

    export_raw_results(
        analysis["sources"],
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]