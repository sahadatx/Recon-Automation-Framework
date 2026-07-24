"""
DNS Resolution Exporter

Export DNS resolution results to output files.
"""

from __future__ import annotations

import json

from modules.dns.constants import (
    DNS_OUTPUT_DIR,
    RESULTS_JSON,
    RESULTS_TXT,
    SUMMARY_TXT,
    UNRESOLVED_TXT,
)


# ==========================================================
# Create Output Directory
# ==========================================================

def create_output_directory() -> None:
    """
    Create the DNS output directory.
    """

    DNS_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# Export Results (TXT)
# ==========================================================

def export_results_txt(
    analysis: dict,
) -> None:
    """
    Export DNS results as text.
    """

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(
            analysis["results"]
        ):

            file.write(
                f"{host}\n"
            )

            file.write(
                "=" * 70 + "\n"
            )

            records = analysis[
                "results"
            ][host]

            for (
                record_type,
                values,
            ) in records.items():

                file.write(
                    f"\n{record_type}\n"
                )

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
# Export Results (JSON)
# ==========================================================

def export_results_json(
    analysis: dict,
) -> None:
    """
    Export DNS results as JSON.
    """

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
# Export Summary
# ==========================================================

def export_summary(
    analysis: dict,
) -> None:
    """
    Export DNS summary.
    """

    statistics = analysis[
        "statistics"
    ]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "DNS Resolution Summary\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )

        file.write(
            f"Resolved Hosts : "
            f"{analysis['resolved_hosts']}\n"
        )

        file.write(
            f"Failed Hosts   : "
            f"{analysis['failed_hosts']}\n"
        )

        file.write(
            f"Total Records  : "
            f"{statistics['total_records']}\n"
        )

        file.write(
            f"Scan Time      : "
            f"{analysis['scan_time']} sec\n\n"
        )

        file.write(
            "Record Counts\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for (
            record_type,
            count,
        ) in statistics[
            "record_counts"
        ].items():

            file.write(
                f"{record_type:<10}"
                f"{count}\n"
            )

        file.write("\n")

        file.write(
            "Hosts Containing Records\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for (
            record_type,
            count,
        ) in statistics[
            "enabled_hosts"
        ].items():

            file.write(
                f"{record_type:<10}"
                f"{count}\n"
            )


# ==========================================================
# Export Unresolved Hosts
# ==========================================================

def export_unresolved(
    analysis: dict,
) -> None:
    """
    Export unresolved hosts.
    """

    with UNRESOLVED_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in analysis[
            "unresolved"
        ]:

            file.write(
                f"{host}\n"
            )


# ==========================================================
# Export All
# ==========================================================

def export_all(
    analysis: dict,
) -> None:
    """
    Export all DNS output files.
    """

    create_output_directory()

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
    "create_output_directory",
    "export_results_txt",
    "export_results_json",
    "export_summary",
    "export_unresolved",
    "export_all",
]