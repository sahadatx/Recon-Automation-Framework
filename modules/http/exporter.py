"""
HTTP Probe Exporter

Export HTTP probe results.
"""

from __future__ import annotations

import json
from typing import Any

from modules.http.constants import (
    ALIVE_TXT,
    DEAD_TXT,
    HTTP_OUTPUT_DIR,
    RESULTS_JSON,
    RESULTS_TXT,
    SUMMARY_TXT,
)


# ==========================================================
# Helpers
# ==========================================================

def create_output_directory() -> None:
    """
    Create the HTTP output directory.
    """

    HTTP_OUTPUT_DIR.mkdir(
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
    Export HTTP results as human-readable text.
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

            for key, value in results[host].items():

                file.write(
                    f"{key:<18}: {value}\n"
                )

            file.write("\n")


# ==========================================================
# Results (JSON)
# ==========================================================

def export_results_json(
    analysis: dict[str, Any],
) -> None:
    """
    Export HTTP analysis as JSON.
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
    Export HTTP summary.
    """

    create_output_directory()

    statistics = analysis["statistics"]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "HTTP PROBE SUMMARY\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            f"Alive Hosts     : "
            f"{statistics['alive_hosts']}\n"
        )

        file.write(
            f"Dead Hosts      : "
            f"{statistics['dead_hosts']}\n"
        )

        file.write(
            f"HTTP Hosts      : "
            f"{statistics['http_hosts']}\n"
        )

        file.write(
            f"HTTPS Hosts     : "
            f"{statistics['https_hosts']}\n"
        )

        file.write(
            f"Average Response: "
            f"{statistics['average_response_time']} sec\n"
        )

        file.write("\n")

        file.write(
            "Status Codes\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        for (
            status,
            count,
        ) in statistics[
            "status_codes"
        ].items():

            file.write(
                f"{status:<10}{count}\n"
            )


# ==========================================================
# Alive Hosts
# ==========================================================

def export_alive(
    analysis: dict[str, Any],
) -> None:
    """
    Export alive hosts.
    """

    create_output_directory()

    statistics = analysis["statistics"]

    with ALIVE_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in statistics["alive"]:

            file.write(
                f"{host}\n"
            )


# ==========================================================
# Dead Hosts
# ==========================================================

def export_dead(
    analysis: dict[str, Any],
) -> None:
    """
    Export dead hosts.
    """

    create_output_directory()

    statistics = analysis["statistics"]

    with DEAD_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in statistics["dead"]:

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
    Export all HTTP output files.
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

    export_alive(
        analysis,
    )

    export_dead(
        analysis,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]