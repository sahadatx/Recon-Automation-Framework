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


def create_output_directory() -> None:


    PASSIVE_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def export_results_txt(
    analysis: dict[str, Any],
) -> None:


    create_output_directory()

    statistics = analysis["statistics"]
    results = analysis["results"]

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("PASSIVE ENUMERATION RESULTS\n")

        file.write("=" * 70 + "\n\n")

        file.write(f"Target : {statistics['target']}\n")

        file.write(f"Unique Subdomains : " f"{statistics['total_subdomains']}\n\n")

        file.write("Subdomains\n")

        file.write("-" * 70 + "\n")

        for subdomain in results:

            file.write(f"{subdomain}\n")


def export_results_json(
    analysis: dict[str, Any],
) -> None:


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
    analysis: dict[str, Any],
) -> None:


    create_output_directory()

    statistics = analysis["statistics"]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("PASSIVE ENUMERATION SUMMARY\n")

        file.write("=" * 70 + "\n\n")

        file.write(f"Target              : {statistics['target']}\n")

        file.write(f"Sources             : {statistics['total_sources']}\n")

        file.write(f"Successful Sources  : {statistics['successful_sources']}\n")

        file.write(f"Failed Sources      : {statistics['failed_sources']}\n")

        file.write(f"Empty Sources       : {statistics['empty_sources']}\n")

        file.write(f"Unique Subdomains   : {statistics['total_subdomains']}\n")


def export_subdomains(
    subdomains: list[str],
) -> None:


    create_output_directory()

    with SUBDOMAINS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for subdomain in subdomains:

            file.write(f"{subdomain}\n")


def export_raw_results(
    sources: dict[str, list[str]],
) -> None:


    create_output_directory()

    with RAW_RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for source, subdomains in sources.items():

            file.write("=" * 70 + "\n")

            file.write(f"{source}\n")

            file.write("=" * 70 + "\n")

            for subdomain in subdomains:

                file.write(f"{subdomain}\n")

            file.write("\n")


def export_all(
    analysis: dict[str, Any],
) -> None:


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


__all__ = [
    "export_all",
]
