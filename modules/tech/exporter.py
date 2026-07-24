"""
Technology Detection Exporter

Export technology detection results.
"""

from __future__ import annotations

import csv
import json

from modules.tech.constants import (
    RESULTS_CSV,
    RESULTS_JSON,
    RESULTS_TXT,
    SUMMARY_TXT,
    TECH_OUTPUT_DIR,
    TECHNOLOGIES_TXT,
)


# ==========================================================
# Create Output Directory
# ==========================================================

def create_output_directory() -> None:
    """
    Create output directory.
    """

    TECH_OUTPUT_DIR.mkdir(
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
    Export detailed technology results.
    """

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(
            analysis["results"]
        ):

            data = analysis[
                "results"
            ][host]

            file.write(
                "=" * 70 + "\n"
            )

            file.write(
                f"{host}\n"
            )

            file.write(
                "=" * 70 + "\n\n"
            )

            file.write(
                "Technologies\n"
            )

            file.write(
                "-" * 70 + "\n"
            )

            technologies = data.get(
                "technologies",
                [],
            )

            if technologies:

                for technology in technologies:

                    file.write(
                        f"- {technology}\n"
                    )

            else:

                file.write(
                    "None\n"
                )

            file.write("\n")

            file.write(
                "Security Headers\n"
            )

            file.write(
                "-" * 70 + "\n"
            )

            headers = data.get(
                "security_headers",
                [],
            )

            if headers:

                for header in headers:

                    file.write(
                        f"- {header}\n"
                    )

            else:

                file.write(
                    "None\n"
                )

            file.write("\n")


# ==========================================================
# Export Results (JSON)
# ==========================================================

def export_results_json(
    analysis: dict,
) -> None:
    """
    Export results as JSON.
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
# Export Results (CSV)
# ==========================================================

def export_results_csv(
    analysis: dict,
) -> None:
    """
    Export results as CSV.
    """

    with RESULTS_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "Host",
                "Technologies",
                "Security Headers",
            ]
        )

        for host in sorted(
            analysis["results"]
        ):

            data = analysis[
                "results"
            ][host]

            writer.writerow(
                [
                    host,
                    ", ".join(
                        data.get(
                            "technologies",
                            [],
                        )
                    ),
                    ", ".join(
                        data.get(
                            "security_headers",
                            [],
                        )
                    ),
                ]
            )


# ==========================================================
# Export Summary
# ==========================================================

def export_summary(
    analysis: dict,
) -> None:
    """
    Export summary.
    """

    statistics = analysis[
        "statistics"
    ]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "Technology Detection Summary\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )

        file.write(
            f"Hosts Analyzed          : "
            f"{statistics['hosts_analyzed']}\n"
        )

        file.write(
            f"Failed Hosts            : "
            f"{statistics['failed_hosts']}\n"
        )

        file.write(
            f"Detected Technologies   : "
            f"{statistics['technology_count']}\n"
        )

        file.write(
            f"Security Headers        : "
            f"{statistics['security_header_count']}\n"
        )

        file.write(
            f"Scan Time               : "
            f"{analysis['scan_time']} sec\n\n"
        )

        file.write(
            "Technology Breakdown\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for (
            technology,
            count,
        ) in statistics[
            "technology_counts"
        ].items():

            file.write(
                f"{technology:<30}"
                f"{count}\n"
            )

        file.write("\n")

        file.write(
            "Security Header Breakdown\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for (
            header,
            count,
        ) in statistics[
            "security_header_counts"
        ].items():

            file.write(
                f"{header:<30}"
                f"{count}\n"
            )


# ==========================================================
# Export Technologies
# ==========================================================

def export_technologies(
    analysis: dict,
) -> None:
    """
    Export unique technologies.
    """

    with TECHNOLOGIES_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for technology in analysis[
            "technologies"
        ]:

            file.write(
                f"{technology}\n"
            )


# ==========================================================
# Export All
# ==========================================================

def export_all(
    analysis: dict,
) -> None:
    """
    Export all output files.
    """

    create_output_directory()

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

    export_technologies(
        analysis,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "create_output_directory",
    "export_results_txt",
    "export_results_json",
    "export_results_csv",
    "export_summary",
    "export_technologies",
    "export_all",
]