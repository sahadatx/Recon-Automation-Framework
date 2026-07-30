"""
Port Scanner Exporter

Export port scan results.
"""

from __future__ import annotations

import csv
import json
from typing import Any

from modules.ports.constants import (
    OPEN_PORTS_TXT,
    PORT_OUTPUT_DIR,
    RESULTS_CSV,
    RESULTS_JSON,
    RESULTS_TXT,
    SUMMARY_TXT,
)


# ==========================================================
# Helpers
# ==========================================================

def create_output_directory() -> None:
    """
    Create output directory.
    """

    PORT_OUTPUT_DIR.mkdir(
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
    Export detailed port scan results.
    """

    create_output_directory()

    results = analysis["results"]

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(results):

            file.write("=" * 70 + "\n")
            file.write(f"{host}\n")
            file.write("=" * 70 + "\n")

            for port in results[host]:

                file.write(
                    f"{port['port']:>5}/tcp   "
                    f"{port['state']:<6}   "
                    f"{port['service']}\n"
                )

            file.write("\n")


# ==========================================================
# Results (JSON)
# ==========================================================

def export_results_json(
    analysis: dict[str, Any],
) -> None:
    """
    Export results as JSON.
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
# Results (CSV)
# ==========================================================

def export_results_csv(
    analysis: dict[str, Any],
) -> None:
    """
    Export results as CSV.
    """

    create_output_directory()

    results = analysis["results"]

    with RESULTS_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Host",
                "Port",
                "Service",
                "State",
            ]
        )

        for host in sorted(results):

            for port in results[host]:

                writer.writerow(
                    [
                        host,
                        port["port"],
                        port["service"],
                        port["state"],
                    ]
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
            "PORT SCAN SUMMARY\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            f"Hosts Scanned            : "
            f"{statistics['hosts_scanned']}\n"
        )

        file.write(
            f"Hosts With Open Ports    : "
            f"{statistics['hosts_with_open_ports']}\n"
        )

        file.write(
            f"Hosts Without Open Ports : "
            f"{statistics['hosts_without_open_ports']}\n"
        )

        file.write(
            f"Total Open Ports         : "
            f"{statistics['total_open_ports']}\n"
        )

        file.write(
            f"Average Open Ports       : "
            f"{statistics['average_open_ports']}\n"
        )

        file.write(
            "Service Breakdown\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        for (
            service,
            count,
        ) in statistics[
            "service_counts"
        ].items():

            file.write(
                f"{service:<20}{count}\n"
            )


# ==========================================================
# Open Hosts
# ==========================================================

def export_open_ports(
    analysis: dict[str, Any],
) -> None:
    """
    Export hosts with open ports.
    """

    create_output_directory()

    statistics = analysis["statistics"]

    with OPEN_PORTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in statistics[
            "open_hosts"
        ]:

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
    Export all output files.
    """

    export_results_txt(
        analysis,
    )

    export_results_json(
        analysis,
    )

    export_results_csv(
        analysis,
    )

    export_summary(
        analysis,
    )

    export_open_ports(
        analysis,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]