"""
Directory Fuzzing Exporter

Export Directory
Fuzzing analysis
results.
"""

from __future__ import annotations

import csv
import json

from pathlib import Path
from typing import Any

from core.logger import (
    success,
    warning,
)

from .constants import (
    OUTPUT_DIR,
    TXT_FILE,
    JSON_FILE,
    CSV_FILE,
    SUMMARY_FILE,
    INTERESTING_FILE,
)


# ==========================================================
# Output Directory
# ==========================================================

def create_output_directory() -> None:
    """
    Create output directory.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# Write Text
# ==========================================================

def write_text(
    output_file: Path,
    lines: list[str],
) -> Path:
    """
    Write text file.

    Args:
        output_file:
            Destination file.

        lines:
            File content.

    Returns:
        Output file path.
    """

    try:

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        success(
            f"Saved {output_file}"
        )

    except OSError as error:

        warning(
            f"{output_file}: {error}"
        )

    return output_file


# ==========================================================
# Write JSON
# ==========================================================

def write_json(
    output_file: Path,
    data: Any,
) -> Path:
    """
    Write JSON file.

    Args:
        output_file:
            Destination file.

        data:
            JSON data.

    Returns:
        Output file path.
    """

    try:

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
                default=str,
            )

        success(
            f"Saved {output_file}"
        )

    except OSError as error:

        warning(
            f"{output_file}: {error}"
        )

    return output_file


# ==========================================================
# Write CSV
# ==========================================================

def write_csv(
    output_file: Path,
    results: dict[str, Any],
) -> Path:
    """
    Write CSV report.

    Args:
        output_file:
            Destination file.

        results:
            Directory Fuzzing results.

    Returns:
        Output file path.
    """

    try:

        with output_file.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

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

            for target, analysis in results.items():

                for result in analysis.get(
                    "results",
                    [],
                ):

                    writer.writerow(
                        [
                            target,
                            result.get("url", ""),
                            result.get("status", ""),
                            result.get("length", ""),
                            result.get("words", ""),
                            result.get("lines", ""),
                            result.get("content_type", ""),
                            result.get("redirect", ""),
                        ]
                    )

        success(
            f"Saved {output_file}"
        )

    except OSError as error:

        warning(
            f"{output_file}: {error}"
        )

    return output_file


# ==========================================================
# Export JSON
# ==========================================================

def export_json(
    analysis: dict[str, Any],
) -> Path:
    """
    Export JSON report.
    """

    return write_json(
        JSON_FILE,
        analysis,
    )


# ==========================================================
# Export TXT
# ==========================================================

def export_txt(
    analysis: dict[str, Any],
) -> Path:
    """
    Export TXT report.
    """

    results = analysis["results"]

    lines: list[str] = []

    lines.append("=" * 80)
    lines.append("Directory Fuzzing Results")
    lines.append("=" * 80)
    lines.append("")

    for target, target_analysis in results.items():

        statistics = target_analysis["statistics"]

        lines.append(
            f"Target : {target}"
        )

        lines.append("-" * 80)

        lines.append(
            f"Results                 : {statistics['total_results']}"
        )

        lines.append(
            f"Interesting Files       : {statistics['interesting_files']}"
        )

        lines.append(
            f"Interesting Directories : {statistics['interesting_directories']}"
        )

        lines.append("")

        for result in target_analysis["results"]:

            lines.append(
                f"[{result.get('status', '')}] {result.get('url', '')}"
            )

        lines.append("")
        lines.append("")

    return write_text(
        TXT_FILE,
        lines,
    )


# ==========================================================
# Export CSV
# ==========================================================

def export_csv(
    analysis: dict[str, Any],
) -> Path:
    """
    Export CSV report.
    """

    return write_csv(
        CSV_FILE,
        analysis["results"],
    )


# ==========================================================
# Export Interesting
# ==========================================================

def export_interesting(
    analysis: dict[str, Any],
) -> Path:
    """
    Export interesting findings.
    """

    results = analysis["results"]

    lines: list[str] = []

    lines.append("=" * 80)
    lines.append("Interesting Findings")
    lines.append("=" * 80)
    lines.append("")

    for target, target_analysis in results.items():

        interesting = target_analysis.get(
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
                    f"  [FILE] {item.get('url', '')}"
                )

        if directories:

            lines.append("")
            lines.append(
                "Interesting Directories"
            )

            for item in directories:

                lines.append(
                    f"  [DIR ] {item.get('url', '')}"
                )

        lines.append("")

    return write_text(
        INTERESTING_FILE,
        lines,
    )


# ==========================================================
# Export Summary
# ==========================================================

def export_summary(
    analysis: dict[str, Any],
) -> Path:
    """
    Export summary report.
    """

    statistics = analysis["statistics"]

    lines = [

        "Directory Fuzzing Summary",

        "=" * 40,

        f"Targets                  : {statistics['targets']}",

        f"Successful               : {statistics['successful']}",

        f"Failed                   : {statistics['failed']}",

        f"Discovered Paths         : {statistics['total_results']}",

        f"Interesting Files        : {statistics['interesting_files']}",

        f"Interesting Directories  : {statistics['interesting_directories']}",

    ]

    return write_text(
        SUMMARY_FILE,
        lines,
    )


# ==========================================================
# Show Summary
# ==========================================================

def show_summary(
    analysis: dict[str, Any],
) -> None:
    """
    Display summary.
    """

    statistics = analysis["statistics"]

    failed = analysis.get(
        "failed",
        [],
    )

    print()

    print("=" * 80)
    print(
        "Directory Fuzzing Summary".center(80)
    )
    print("=" * 80)

    print(f"Targets                  : {statistics['targets']}")
    print(f"Successful               : {statistics['successful']}")
    print(f"Failed                   : {statistics['failed']}")
    print(f"Discovered Paths         : {statistics['total_results']}")
    print(f"Interesting Files        : {statistics['interesting_files']}")
    print(f"Interesting Directories  : {statistics['interesting_directories']}")

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
    analysis: dict[str, Any],
) -> None:
    """
    Export all reports.
    """

    create_output_directory()

    export_json(analysis)

    export_txt(analysis)

    export_csv(analysis)

    export_interesting(analysis)

    export_summary(analysis)

    show_summary(analysis)


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]