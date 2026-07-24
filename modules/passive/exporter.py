"""
Passive Enumeration Exporter

Export passive enumeration results.
"""

from __future__ import annotations

import json

from modules.passive.constants import (
    PASSIVE_OUTPUT_DIR,
    RAW_RESULTS_TXT,
    RESULTS_JSON,
    RESULTS_TXT,
    SUBDOMAINS_TXT,
    SUMMARY_TXT,
)


def create_output_directory() -> None:
    """
    Create passive output directory.
    """

    PASSIVE_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def export_results_txt(
    analysis: dict,
) -> None:
    """
    Export human-readable results.
    """

    create_output_directory()

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("PASSIVE ENUMERATION RESULTS\n")
        file.write("=" * 70 + "\n\n")

        file.write(
            f"Target : {analysis['target']}\n"
        )

        file.write(
            f"Unique Subdomains : "
            f"{analysis['total_subdomains']}\n\n"
        )

        file.write("Subdomains\n")
        file.write("-" * 70 + "\n")

        for subdomain in analysis["subdomains"]:
            file.write(f"{subdomain}\n")


def export_results_json(
    analysis: dict,
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


def export_summary(
    analysis: dict,
) -> None:
    """
    Export summary.
    """

    create_output_directory()

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("PASSIVE ENUMERATION SUMMARY\n")
        file.write("=" * 70 + "\n\n")

        file.write(
            f"Target              : {analysis['target']}\n"
        )

        file.write(
            f"Sources             : {analysis['total_sources']}\n"
        )

        file.write(
            f"Successful Sources  : "
            f"{analysis['successful_sources']}\n"
        )

        file.write(
            f"Failed Sources      : "
            f"{analysis['failed_sources']}\n"
        )

        file.write(
            f"Empty Sources       : "
            f"{analysis['empty_sources']}\n"
        )

        file.write(
            f"Unique Subdomains   : "
            f"{analysis['total_subdomains']}\n"
        )

        file.write(
            f"Scan Time           : "
            f"{analysis['scan_time']} sec\n"
        )


def export_subdomains(
    subdomains: list[str],
) -> None:
    """
    Export unique subdomains.
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


def export_raw_results(
    results: dict[str, list[str]],
) -> None:
    """
    Export raw results grouped by source.
    """

    create_output_directory()

    with RAW_RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for source, subdomains in results.items():

            file.write("=" * 70 + "\n")
            file.write(f"{source}\n")
            file.write("=" * 70 + "\n")

            for subdomain in subdomains:
                file.write(
                    f"{subdomain}\n"
                )

            file.write("\n")


def export_all(
    analysis: dict,
) -> None:
    """
    Export all passive enumeration outputs.
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
        analysis["subdomains"],
    )

    export_raw_results(
        analysis["results"],
    )