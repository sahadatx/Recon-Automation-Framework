"""
DNS Resolution Exporter

Export DNS resolution results.
"""

from __future__ import annotations

import json
from typing import Any

from modules.dns.constants import (
    DNS_OUTPUT_DIR,
    RESULTS_JSON,
    RESULTS_TXT,
    SUMMARY_TXT,
    UNRESOLVED_TXT,
)

# ==========================================================
# Helpers
# ==========================================================

def create_output_directory() -> None:
    """
    Create DNS output directory.
    """

    DNS_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# Results (TXT)
# ==========================================================

def export_results_txt(
    analysis: dict[str, Any],
) -> None:
    """
    Export DNS results as human-readable text.
    """

    create_output_directory()

    results = analysis["results"]

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(results):

            file.write(f"{host}\n")
            file.write("=" * 70 + "\n")

            records = results[host]

            for (
                record_type,
                values,
            ) in records.items():

                file.write(f"\n{record_type}\n")

                if values:

                    for value in values:

                        file.write(
                            f"  - {value}\n"
                        )

                else:

                    file.write(
                        "  No Record\n"
                    )

            file.write("\n")


# ==========================================================
# Results (JSON)
# ==========================================================

def export_results_json(
    analysis: dict[str, Any],
) -> None:
    """
    Export DNS analysis as JSON.
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
            sort_keys=True,
        )


# ==========================================================
# Summary
# ==========================================================

def export_summary(
    analysis: dict[str, Any],
) -> None:
    """
    Export DNS summary.
    """

    create_output_directory()

    statistics = analysis["statistics"]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "DNS RESOLUTION SUMMARY\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            f"Resolved Hosts : "
            f"{statistics['resolved_hosts']}\n"
        )

        file.write(
            f"Failed Hosts   : "
            f"{statistics['failed_hosts']}\n"
        )

        file.write(
            f"Total Records  : "
            f"{statistics['total_records']}\n"
        )

        file.write(
            f"Scan Time      : "
            f"{statistics['elapsed']} sec\n\n"
        )

        file.write(
            "Record Counts\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        for (
            record_type,
            count,
        ) in statistics[
            "record_counts"
        ].items():

            file.write(
                f"{record_type:<10}{count}\n"
            )

        file.write("\n")

        file.write(
            "Hosts Containing Records\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        for (
            record_type,
            count,
        ) in statistics[
            "enabled_hosts"
        ].items():

            file.write(
                f"{record_type:<10}{count}\n"
            )


# ==========================================================
# Unresolved Hosts
# ==========================================================

def export_unresolved(
    analysis: dict[str, Any],
) -> None:
    """
    Export unresolved hosts.
    """

    create_output_directory()

    statistics = analysis["statistics"]

    with UNRESOLVED_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in statistics["unresolved"]:

            file.write(
                f"{host}\n"
            )


# ==========================================================
# Export Everything
# ==========================================================

def export_all(
    analysis: dict[str, Any],
) -> None:
    """
    Export all DNS output files.
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

    export_unresolved(
        analysis,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]