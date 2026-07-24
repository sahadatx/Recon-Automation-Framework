"""
HTTP Probe Exporter

Export HTTP probe results.
"""

from __future__ import annotations

import json

from modules.http.constants import (
    ALIVE_TXT,
    DEAD_TXT,
    HTTP_OUTPUT_DIR,
    RESULTS_JSON,
    RESULTS_TXT,
    SUMMARY_TXT,
)


# ==========================================================
# Create Output Directory
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
# Export Results (TXT)
# ==========================================================

def export_results_txt(
    analysis: dict,
) -> None:
    """
    Export HTTP results as text.
    """

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(
            analysis["results"]
        ):

            data = analysis["results"][
                host
            ]

            file.write(
                "=" * 70 + "\n"
            )

            file.write(
                f"{host}\n"
            )

            file.write(
                "=" * 70 + "\n"
            )

            for (
                key,
                value,
            ) in data.items():

                file.write(
                    f"{key:<18}: {value}\n"
                )

            file.write("\n")


# ==========================================================
# Export Results (JSON)
# ==========================================================

def export_results_json(
    analysis: dict,
) -> None:
    """
    Export HTTP results as JSON.
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
    Export HTTP summary.
    """

    statistics = analysis[
        "statistics"
    ]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "HTTP Probe Summary\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )

        file.write(
            f"Alive Hosts     : "
            f"{analysis['alive_hosts']}\n"
        )

        file.write(
            f"Dead Hosts      : "
            f"{analysis['dead_hosts']}\n"
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

        file.write(
            f"Scan Time       : "
            f"{analysis['scan_time']} sec\n\n"
        )

        file.write(
            "Status Codes\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for (
            status,
            count,
        ) in statistics[
            "status_codes"
        ].items():

            file.write(
                f"{status:<10}"
                f"{count}\n"
            )


# ==========================================================
# Export Alive Hosts
# ==========================================================

def export_alive(
    analysis: dict,
) -> None:
    """
    Export alive hosts.
    """

    with ALIVE_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in analysis[
            "alive"
        ]:

            file.write(
                f"{host}\n"
            )


# ==========================================================
# Export Dead Hosts
# ==========================================================

def export_dead(
    analysis: dict,
) -> None:
    """
    Export dead hosts.
    """

    with DEAD_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in analysis[
            "dead"
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
    Export all HTTP output files.
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
    "create_output_directory",
    "export_results_txt",
    "export_results_json",
    "export_summary",
    "export_alive",
    "export_dead",
    "export_all",
]