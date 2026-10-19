from __future__ import annotations

import csv
import json
from typing import Any

from modules.tech.constants import (
    RESULTS_CSV,
    RESULTS_JSON,
    RESULTS_TXT,
    SUMMARY_TXT,
    TECH_OUTPUT_DIR,
    TECHNOLOGIES_TXT,
)


def create_output_directory() -> None:


    TECH_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def export_results_txt(
    analysis: dict[str, Any],
) -> None:


    create_output_directory()

    results = analysis["results"]

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(results):

            data = results[host]

            file.write("=" * 70 + "\n")
            file.write(f"{host}\n")
            file.write("=" * 70 + "\n\n")

            file.write("Technologies\n")
            file.write("-" * 70 + "\n")

            technologies = data.get(
                "technologies",
                [],
            )

            if technologies:

                for technology in technologies:

                    file.write(f"- {technology}\n")

            else:

                file.write("None\n")

            file.write("\n")

            file.write("Security Headers\n")

            file.write("-" * 70 + "\n")

            headers = data.get(
                "security_headers",
                [],
            )

            if headers:

                for header in headers:

                    file.write(f"- {header}\n")

            else:

                file.write("None\n")

            file.write("\n")


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
            sort_keys=True,
        )


def export_results_csv(
    analysis: dict[str, Any],
) -> None:


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
                "Technologies",
                "Security Headers",
            ]
        )

        for host in sorted(results):

            data = results[host]

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


def export_summary(
    analysis: dict[str, Any],
) -> None:


    create_output_directory()

    statistics = analysis["statistics"]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("TECHNOLOGY DETECTION SUMMARY\n")

        file.write("=" * 70 + "\n\n")

        file.write(f"Hosts Analyzed        : " f"{statistics['hosts_analyzed']}\n")

        file.write(f"Failed Hosts          : " f"{statistics['failed_hosts']}\n")

        file.write(f"Detected Technologies : " f"{statistics['technology_count']}\n")

        file.write(
            f"Security Headers      : " f"{statistics['security_header_count']}\n"
        )

        file.write("Technology Breakdown\n")

        file.write("-" * 70 + "\n")

        for (
            technology,
            count,
        ) in statistics["technology_counts"].items():

            file.write(f"{technology:<30}{count}\n")

        file.write("\n")

        file.write("Security Header Breakdown\n")

        file.write("-" * 70 + "\n")

        for (
            header,
            count,
        ) in statistics["security_header_counts"].items():

            file.write(f"{header:<30}{count}\n")


def export_technologies(
    analysis: dict[str, Any],
) -> None:


    create_output_directory()

    statistics = analysis["statistics"]

    with TECHNOLOGIES_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for technology in statistics["technologies"]:

            file.write(f"{technology}\n")


def export_all(
    analysis: dict[str, Any],
) -> None:


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


__all__ = [
    "export_all",
]
