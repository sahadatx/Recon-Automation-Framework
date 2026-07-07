"""
Screenshot Exporter

Exports screenshot capture results.
"""

import json
from pathlib import Path

from core.logger import (
    success,
    section,
)


# ==========================================================
# Output Directory
# ==========================================================

def ensure_output_directory() -> Path:
    """
    Create output directory.

    Returns:
        Path
    """

    output = Path("output")

    output.mkdir(

        parents=True,

        exist_ok=True,

    )

    return output


# ==========================================================
# Save Screenshot Results
# ==========================================================

def save_screenshot_results(
    results: dict,
    filename: str = "screenshots.txt",
) -> Path:
    """
    Save screenshot results.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

    with output_file.open(

        "w",

        encoding="utf-8",

    ) as file:

        for host in sorted(results):

            data = results[host]

            file.write("=" * 80 + "\n")

            file.write(
                f"Host         : {host}\n"
            )

            file.write(
                f"URL          : {data.get('url', '-')}\n"
            )

            file.write(
                f"Title        : {data.get('title', '-')}\n"
            )

            file.write(
                f"Captured     : {data.get('captured', False)}\n"
            )

            file.write(
                f"Status       : {data.get('status', '-')}\n"
            )

            file.write(
                f"Screenshot   : {data.get('path', '-')}\n"
            )

            file.write(
                f"Width        : {data.get('width', '-')}\n"
            )

            file.write(
                f"Height       : {data.get('height', '-')}\n"
            )

            file.write(
                f"Filesize     : {data.get('filesize', 0)} bytes\n"
            )

            file.write(
                f"Capture Time : {data.get('elapsed', 0):.2f} sec\n"
            )

            file.write("\n")

    success(
        f"Screenshot results saved to {output_file}"
    )

    return output_file


# ==========================================================
# Export JSON
# ==========================================================

def export_screenshot_json(
    results: dict,
    filename: str = "screenshots.json",
) -> Path:
    """
    Export screenshot results to JSON.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

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

def export_screenshot_csv(
    results: dict,
    filename: str = "screenshots.csv",
) -> Path:
    """
    Export screenshot results to CSV.

    Returns:
        Path
    """

    import csv

    output_file = (

        ensure_output_directory()

        / filename

    )

    with output_file.open(

        "w",

        newline="",

        encoding="utf-8",

    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            "Host",

            "URL",

            "Title",

            "Status",

            "Captured",

            "Width",

            "Height",

            "Filesize",

            "Elapsed",

            "Screenshot",

        ])

        for host in sorted(results):

            data = results[host]

            writer.writerow([

                host,

                data.get("url"),

                data.get("title"),

                data.get("status"),

                data.get("captured"),

                data.get("width"),

                data.get("height"),

                data.get("filesize"),

                data.get("elapsed"),

                data.get("path"),

            ])

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
    Display screenshot summary.
    """

    section(
        "Screenshot Capture Summary"
    )

    total = len(results) + len(failed)

    success_rate = (

        (len(results) / total) * 100

        if total

        else 0

    )

    print(

        f"{'Hosts Processed':<25}"

        f"{total}"

    )

    print(

        f"{'Captured':<25}"

        f"{len(results)}"

    )

    print(

        f"{'Failed':<25}"

        f"{len(failed)}"

    )

    print(

        f"{'Success Rate':<25}"

        f"{success_rate:.2f}%"

    )

    print(

        f"{'Elapsed':<25}"

        f"{elapsed:.2f} sec"

    )

    print("=" * 80)

    if failed:

        print()

        print("Failed Hosts")

        print("-" * 80)

        for host in failed:

            print(

                f"• {host}"

            )

        print("-" * 80)