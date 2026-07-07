"""
Technology Detection Exporter

Exports technology detection results.
"""

import csv
import json
from pathlib import Path

from core.logger import (
    success,
    section,
)


# ==========================================================
# Save Technologies
# ==========================================================

def save_technologies(
    results: dict,
    filename: str = "technologies.txt",
) -> Path:
    """
    Save detected technologies only.
    """

    output_dir = Path("output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / filename

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(results):

            technologies = results[
                host
            ].get(
                "technologies",
                [],
            )

            if not technologies:
                continue

            file.write(
                f"{host}\n"
            )

            for technology in technologies:

                file.write(
                    f"  - {technology}\n"
                )

            file.write("\n")

    success(
        f"Technologies saved to {output_file}"
    )

    return output_file


# ==========================================================
# Save Technology Results
# ==========================================================

def save_technology_results(
    results: dict,
    filename: str = "technology_results.txt",
) -> Path:
    """
    Save complete technology detection results.
    """

    output_dir = Path("output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / filename

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(results):

            file.write("=" * 70 + "\n")
            file.write(f"{host}\n")
            file.write("=" * 70 + "\n\n")

            technologies = results[
                host
            ].get(
                "technologies",
                [],
            )

            security = results[
                host
            ].get(
                "security_headers",
                [],
            )

            file.write(
                "Technologies\n"
            )

            if technologies:

                for tech in technologies:

                    file.write(
                        f"  - {tech}\n"
                    )

            else:

                file.write(
                    "  None\n"
                )

            file.write("\n")

            file.write(
                "Security Headers\n"
            )

            if security:

                for header in security:

                    file.write(
                        f"  - {header}\n"
                    )

            else:

                file.write(
                    "  None\n"
                )

            file.write("\n")

    success(
        f"Technology results saved to {output_file}"
    )

    return output_file


# ==========================================================
# Export JSON
# ==========================================================

def export_technology_json(
    results: dict,
    filename: str = "technology_results.json",
) -> Path:
    """
    Export JSON results.
    """

    output_dir = Path("output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / filename

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            sort_keys=True,
        )

    success(
        f"JSON exported to {output_file}"
    )

    return output_file


# ==========================================================
# Export CSV
# ==========================================================

def export_technology_csv(
    results: dict,
    filename: str = "technologies.csv",
) -> Path:
    """
    Export CSV report.
    """

    output_dir = Path("output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / filename

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:

        writer = csv.writer(
            csvfile
        )

        writer.writerow(
            [
                "Host",
                "Technologies",
                "Security Headers",
            ]
        )

        for host in sorted(results):

            writer.writerow(

                [

                    host,

                    ", ".join(

                        results[host].get(
                            "technologies",
                            [],
                        )

                    ),

                    ", ".join(

                        results[host].get(
                            "security_headers",
                            [],
                        )

                    ),

                ]

            )

    success(
        f"CSV exported to {output_file}"
    )

    return output_file


# ==========================================================
# Summary
# ==========================================================

def show_summary(
    results: dict,
    failed: list,
    elapsed: float,
):
    """
    Display technology detection summary.
    """

    section(
        "Technology Detection Summary"
    )

    hosts = len(results)

    technology_total = 0

    security_total = 0

    technology_counts = {}

    for data in results.values():

        technologies = data.get(
            "technologies",
            [],
        )

        security = data.get(
            "security_headers",
            [],
        )

        technology_total += len(
            technologies
        )

        security_total += len(
            security
        )

        for technology in technologies:

            technology_counts[
                technology
            ] = technology_counts.get(
                technology,
                0,
            ) + 1

    print(
        f"{'Hosts Analysed':<25}{hosts}"
    )

    print(
        f"{'Failed Hosts':<25}{len(failed)}"
    )

    print("-" * 75)

    print(
        f"{'Detected Technologies':<25}{technology_total}"
    )

    print(
        f"{'Security Headers':<25}{security_total}"
    )

    print("-" * 75)

    print(
        "Top Technologies"
    )

    print("-" * 75)

    for technology, count in sorted(

        technology_counts.items(),

        key=lambda item: item[1],

        reverse=True,

    ):

        print(
            f"{technology:<30}{count}"
        )

    print("-" * 75)

    print(
        f"{'Total Time':<25}{elapsed:.2f} sec"
    )

    print("=" * 75)

    if failed:

        print()

        print(
            "Failed Hosts"
        )

        print("-" * 75)

        for host in failed:

            print(
                f" • {host}"
            )

        print("-" * 75)