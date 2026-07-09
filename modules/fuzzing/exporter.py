"""
Directory Fuzzing Exporter

Exports directory fuzzing results.
"""

import csv
import json

from pathlib import Path

from core.logger import (
    success,
)


# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIRECTORY = (

    Path("output")

    / "fuzzing"

)


# ==========================================================
# Create Output Directory
# ==========================================================

def ensure_output_directory():
    """
    Create output directory.

    Returns:
        Path
    """

    OUTPUT_DIRECTORY.mkdir(

        parents=True,

        exist_ok=True,

    )

    return OUTPUT_DIRECTORY


# ==========================================================
# Write Text File
# ==========================================================

def write_text(
    filename: str,
    lines: list[str],
):
    """
    Write text file.
    """

    output = (

        ensure_output_directory()

        / filename

    )

    with output.open(

        "w",

        encoding="utf-8",

    ) as file:

        file.write(

            "\n".join(lines)

        )

    success(
        f"Saved {output}"
    )

    return output


# ==========================================================
# Export TXT
# ==========================================================

def export_txt(
    results: dict,
    filename: str = "results.txt",
):
    """
    Export TXT report.
    """

    lines = []

    lines.append("=" * 80)
    lines.append("Directory Fuzzing Results")
    lines.append("=" * 80)
    lines.append("")

    for target, data in results.items():

        lines.append(
            f"Target : {target}"
        )

        lines.append(
            "-" * 80
        )

        statistics = data.get(
            "statistics",
            {},
        )

        lines.append(
            f"Results                 : {statistics.get('total_results',0)}"
        )

        lines.append(
            f"Interesting Files       : {statistics.get('interesting_files',0)}"
        )

        lines.append(
            f"Interesting Directories : {statistics.get('interesting_directories',0)}"
        )

        lines.append("")

        for result in data.get(
            "results",
            [],
        ):

            lines.append(

                f"[{result['status']}] {result['url']}"

            )

        lines.append("")
        lines.append("")

    return write_text(

        filename,

        lines,

    )


# ==========================================================
# Export JSON
# ==========================================================

def export_json(
    results: dict,
    filename: str = "results.json",
):
    """
    Export JSON report.
    """

    output = (

        ensure_output_directory()

        / filename

    )

    with output.open(

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
        f"Saved {output}"
    )

    return output


# ==========================================================
# Export CSV
# ==========================================================

def export_csv(
    results: dict,
    filename: str = "results.csv",
):
    """
    Export CSV report.
    """

    output = (

        ensure_output_directory()

        / filename

    )

    with output.open(

        "w",

        newline="",

        encoding="utf-8",

    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(

            [

                "Target",

                "URL",

                "Status",

                "Length",

                "Words",

                "Lines",

                "Content-Type",

                "Redirect",

            ]

        )

        for target, data in results.items():

            for result in data.get(
                "results",
                [],
            ):

                writer.writerow(

                    [

                        target,

                        result.get(
                            "url",
                            "",
                        ),

                        result.get(
                            "status",
                            "",
                        ),

                        result.get(
                            "length",
                            "",
                        ),

                        result.get(
                            "words",
                            "",
                        ),

                        result.get(
                            "lines",
                            "",
                        ),

                        result.get(
                            "content_type",
                            "",
                        ),

                        result.get(
                            "redirect",
                            "",
                        ),

                    ]

                )

    success(
        f"Saved {output}"
    )

    return output


# ==========================================================
# Export Interesting Results
# ==========================================================

def export_interesting(
    results: dict,
    filename: str = "interesting.txt",
):
    """
    Export interesting findings.
    """

    lines = []

    lines.append("=" * 80)
    lines.append("Interesting Findings")
    lines.append("=" * 80)
    lines.append("")

    for target, data in results.items():

        interesting = data.get(
            "interesting",
            {},
        )

        files = interesting.get(
            "files",
            [],
        )

        directories = interesting.get(
            "directories",
            [],
        )

        lines.append(
            f"Target : {target}"
        )

        lines.append("-" * 80)

        if files:

            lines.append("Interesting Files")

            for item in files:

                lines.append(
                    f"  [FILE] {item['url']}"
                )

        if directories:

            lines.append("")
            lines.append(
                "Interesting Directories"
            )

            for item in directories:

                lines.append(
                    f"  [DIR ] {item['url']}"
                )

        lines.append("")

    return write_text(
        filename,
        lines,
    )


# ==========================================================
# Export Summary
# ==========================================================

def export_summary(
    results: dict,
    filename: str = "summary.txt",
):
    """
    Export summary report.
    """

    total_targets = len(results)

    total_results = 0

    interesting_files = 0

    interesting_directories = 0

    lines = []

    lines.append("=" * 80)
    lines.append("Directory Fuzzing Summary")
    lines.append("=" * 80)
    lines.append("")

    for data in results.values():

        statistics = data.get(
            "statistics",
            {},
        )

        total_results += statistics.get(
            "total_results",
            0,
        )

        interesting_files += statistics.get(
            "interesting_files",
            0,
        )

        interesting_directories += statistics.get(
            "interesting_directories",
            0,
        )

    lines.append(
        f"Targets                  : {total_targets}"
    )

    lines.append(
        f"Discovered Paths         : {total_results}"
    )

    lines.append(
        f"Interesting Files        : {interesting_files}"
    )

    lines.append(
        f"Interesting Directories  : {interesting_directories}"
    )

    return write_text(
        filename,
        lines,
    )


# ==========================================================
# Show Summary
# ==========================================================

def show_summary(
    results: dict,
    overall: dict,
    failed: list,
    elapsed: float,
):
    """
    Display summary.
    """

    print()

    print("=" * 80)
    print("Directory Fuzzing Summary")
    print("=" * 80)

    print(
        f"{'Targets':<25}"
        f"{overall.get('targets',0)}"
    )

    print(
        f"{'Successful':<25}"
        f"{overall.get('successful',0)}"
    )

    print(
        f"{'Failed':<25}"
        f"{overall.get('failed',0)}"
    )

    print(
        f"{'Discovered Paths':<25}"
        f"{overall.get('total_results',0)}"
    )

    print(
        f"{'Interesting Files':<25}"
        f"{overall.get('interesting_files',0)}"
    )

    print(
        f"{'Interesting Directories':<25}"
        f"{overall.get('interesting_directories',0)}"
    )

    print(
        f"{'Elapsed':<25}"
        f"{elapsed:.2f} sec"
    )

    if failed:

        print()
        print("Failed Targets")
        print("-" * 80)

        for target in failed:

            print(
                f" • {target}"
            )

    print("=" * 80)


# ==========================================================
# Export All
# ==========================================================

def export_all(
    results: dict,
):
    """
    Export all reports.
    """

    files = {

        "text": export_txt(
            results
        ),

        "json": export_json(
            results
        ),

        "csv": export_csv(
            results
        ),

        "interesting": export_interesting(
            results
        ),

        "summary": export_summary(
            results
        ),

    }

    return files