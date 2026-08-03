"""
WAF Detection Exporter

Export WAF Detection
results into multiple formats.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from config.config import WAF_OUTPUT_DIR
from core.logger import success, warning

# ==========================================================
# Create Output Directory
# ==========================================================


def create_output_directory() -> Path:
    """
    Create WAF Detection output directory.

    Returns:
        Output directory path.
    """

    WAF_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return WAF_OUTPUT_DIR


# ==========================================================
# Write Text File
# ==========================================================


def write_text(
    output_file: Path,
    lines: list[str],
) -> Path:
    """
    Write text lines to a file.

    Args:
        output_file:
            Destination file.

        lines:
            Text lines.

    Returns:
        Output file path.
    """

    create_output_directory()

    try:

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            for line in lines:

                file.write(f"{line}\n")

    except Exception as error:

        warning(f"{output_file}: {error}")

        return output_file

    success(f"Saved {output_file}")

    return output_file


# ==========================================================
# Write JSON File
# ==========================================================


def write_json(
    output_file: Path,
    data: Any,
) -> Path:
    """
    Write JSON data.

    Args:
        output_file:
            Destination file.

        data:
            JSON serializable object.

    Returns:
        Output file path.
    """

    create_output_directory()

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

    except Exception as error:

        warning(f"{output_file}: {error}")

        return output_file

    success(f"Saved {output_file}")

    return output_file


# ==========================================================
# Write CSV File
# ==========================================================


def write_csv(
    output_file: Path,
    rows: list[dict[str, Any]],
) -> Path:
    """
    Write CSV data.

    Args:
        output_file:
            Destination file.

        rows:
            CSV rows.

    Returns:
        Output file path.
    """

    create_output_directory()

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
                    "Detected",
                    "Vendor",
                    "Confidence",
                    "Score",
                ]
            )

            for row in rows:

                writer.writerow(
                    [
                        row.get("url", ""),
                        row.get("detected", False),
                        row.get("vendor", ""),
                        row.get("confidence", ""),
                        row.get("score", 0),
                    ]
                )

    except Exception as error:

        warning(f"{output_file}: {error}")

        return output_file

    success(f"Saved {output_file}")

    return output_file


# ==========================================================
# Export JSON
# ==========================================================


def export_json(
    analysis: dict[str, Any],
) -> Path:
    """
    Export JSON report.

    Args:
        analysis:
            WAF Detection analysis.

    Returns:
        Output file path.
    """

    return write_json(
        WAF_OUTPUT_DIR / "results.json",
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

    Args:
        analysis:
            WAF Detection analysis.

    Returns:
        Output file path.
    """

    results = analysis["results"]

    lines: list[str] = []

    for result in results:

        lines.append("=" * 80)

        lines.append(f"Target      : {result.get('url', '-')}")

        lines.append(f"Detected    : {result.get('detected', False)}")

        lines.append(f"Vendor      : {result.get('vendor', '-')}")

        lines.append(f"Confidence  : {result.get('confidence', '-')}")

        lines.append(f"Score       : {result.get('score', 0)}")

        lines.append("Evidence")

        for item in result.get(
            "evidence",
            [],
        ):

            lines.append(f"  - {item}")

        lines.append("")

    return write_text(
        WAF_OUTPUT_DIR / "results.txt",
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

    Args:
        analysis:
            WAF Detection analysis.

    Returns:
        Output file path.
    """

    return write_csv(
        WAF_OUTPUT_DIR / "results.csv",
        analysis["results"],
    )


# ==========================================================
# Export Detected Targets
# ==========================================================


def export_detected(
    analysis: dict[str, Any],
) -> Path:
    """
    Export detected WAF targets only.

    Args:
        analysis:
            WAF Detection analysis.

    Returns:
        Output file path.
    """

    results = analysis["results"]

    lines: list[str] = []

    for result in results:

        if not result.get(
            "detected",
            False,
        ):

            continue

        lines.append(
            f"{result.get('url', '-')}"
            f" -> "
            f"{result.get('vendor', '-')}"
            f" ({result.get('confidence', '-')})"
        )

    return write_text(
        WAF_OUTPUT_DIR / "detected.txt",
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

    Args:
        analysis:
            WAF Detection analysis.

    Returns:
        Output file path.
    """

    statistics = analysis["statistics"]

    lines = [
        "WAF Detection Summary",
        "=" * 80,
        f"Targets                : {statistics['targets']}",
        f"WAF Detected           : {statistics['detected']}",
        f"Not Detected           : {statistics['not_detected']}",
        f"Success Rate           : {statistics['success_rate']}%",
        f"Average Score          : {statistics['average_score']}",
        f"Highest Score          : {statistics['highest_score']}",
        "",
        "Detected Vendors",
        "-" * 80,
    ]

    vendors = statistics.get(
        "vendors",
        {},
    )

    if vendors:

        for vendor, count in vendors.items():

            lines.append(f"{vendor:<30}{count}")

    else:

        lines.append("None")

    lines.extend(
        [
            "",
            "Confidence Levels",
            "-" * 80,
        ]
    )

    confidence = statistics.get(
        "confidence",
        {},
    )

    if confidence:

        for level, count in confidence.items():

            lines.append(f"{level:<30}{count}")

    else:

        lines.append("None")

    return write_text(
        WAF_OUTPUT_DIR / "summary.txt",
        lines,
    )


# ==========================================================
# Show Summary
# ==========================================================


def show_summary(
    analysis: dict[str, Any],
) -> None:
    """
    Display WAF Detection summary.
    """

    statistics = analysis["statistics"]

    print()

    print("=" * 80)

    print("WAF Detection Summary")

    print("=" * 80)

    print(f"{'Targets':<30}" f"{statistics['targets']}")

    print(f"{'WAF Detected':<30}" f"{statistics['detected']}")

    print(f"{'Not Detected':<30}" f"{statistics['not_detected']}")

    print(f"{'Success Rate':<30}" f"{statistics['success_rate']}%")

    print(f"{'Average Score':<30}" f"{statistics['average_score']}")

    print(f"{'Highest Score':<30}" f"{statistics['highest_score']}")

    print("-" * 80)

    print("Detected Vendors")

    print("-" * 80)

    vendors = statistics.get(
        "vendors",
        {},
    )

    if vendors:

        for vendor, count in vendors.items():

            print(f"{vendor:<30}{count}")

    else:

        print("None")

    print("-" * 80)

    print("Confidence Levels")

    print("-" * 80)

    confidence = statistics.get(
        "confidence",
        {},
    )

    if confidence:

        for level, count in confidence.items():

            print(f"{level:<30}{count}")

    else:

        print("None")

    print("=" * 80)


# ==========================================================
# Export All
# ==========================================================


def export_all(
    analysis: dict[str, Any],
) -> None:
    """
    Export all WAF Detection reports.

    Args:
        analysis:
            WAF Detection analysis.
    """

    exporters = (
        export_json,
        export_txt,
        export_csv,
        export_detected,
        export_summary,
    )

    for exporter in exporters:

        try:

            exporter(analysis)

        except Exception as error:

            warning(f"{exporter.__name__}: {error}")

    success("WAF Detection reports exported successfully.")


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]
