"""
Nuclei Exporter
"""

from __future__ import annotations

import csv
import json

from pathlib import Path
from typing import Any

from core.logger import success

from .constants import (
    CSV_FILE,
    CRITICAL_FILE,
    HIGH_FILE,
    JSON_FILE,
    OUTPUT_DIR,
    SUMMARY_FILE,
    TXT_FILE,
)

# ==========================================================
# Output Directory
# ==========================================================


def create_output_directory() -> Path:
    """
    Create output directory.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return OUTPUT_DIR


# ==========================================================
# Write Helpers
# ==========================================================


def write_text(
    path: Path,
    lines: list[str],
) -> Path:
    """
    Write text file.
    """

    create_output_directory()

    path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    success(f"Saved {path}")

    return path


def write_json(
    path: Path,
    data: dict[str, Any],
) -> Path:
    """
    Write JSON file.
    """

    create_output_directory()

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
        )

    success(f"Saved {path}")

    return path


def write_csv(
    path: Path,
    rows: list[list[Any]],
) -> Path:
    """
    Write CSV file.
    """

    create_output_directory()

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerows(rows)

    success(f"Saved {path}")

    return path


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

    statistics = analysis["statistics"]

    lines = []

    lines.append("=" * 80)
    lines.append("Nuclei Scan Report")
    lines.append("=" * 80)
    lines.append("")

    lines.append("Summary")
    lines.append("-" * 80)

    lines.append(f"Total Findings : {statistics['total_findings']}")

    lines.append(f"Critical       : {statistics['critical']}")

    lines.append(f"High           : {statistics['high']}")

    lines.append(f"Medium         : {statistics['medium']}")

    lines.append(f"Low            : {statistics['low']}")

    lines.append(f"Info           : {statistics['info']}")

    lines.append("")

    lines.append("=" * 80)
    lines.append("Findings")
    lines.append("=" * 80)

    for finding in results:

        lines.append(f"[{finding['severity'].upper()}]")

        lines.append(f"Target       : {finding.get('target', '')}")

        lines.append(f"URL          : {finding.get('url', '')}")

        lines.append(f"Template     : {finding.get('template_name', '')}")

        lines.append(f"Template ID  : {finding.get('template_id', '')}")

        lines.append(f"Protocol     : {finding.get('protocol', '')}")

        lines.append(f"Matcher      : {finding.get('matcher', '')}")

        if finding.get("description"):

            lines.append(f"Description  : {finding['description']}")

        if finding.get("tags"):

            lines.append(f"Tags         : {', '.join(finding['tags'])}")

        lines.append("-" * 80)

    return write_text(
        TXT_FILE,
        lines,
    )


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
# Export CSV
# ==========================================================


def export_csv(
    analysis: dict[str, Any],
) -> Path:
    """
    Export CSV report.
    """

    results = analysis["results"]

    rows: list[list[Any]] = [
        [
            "Severity",
            "Target",
            "URL",
            "Template ID",
            "Template Name",
            "Protocol",
            "Matcher",
            "Tags",
        ]
    ]

    for finding in results:

        rows.append(
            [
                finding.get("severity", ""),
                finding.get("target", ""),
                finding.get("url", ""),
                finding.get("template_id", ""),
                finding.get("template_name", ""),
                finding.get("protocol", ""),
                finding.get("matcher", ""),
                ", ".join(
                    finding.get(
                        "tags",
                        [],
                    )
                ),
            ]
        )

    return write_csv(
        CSV_FILE,
        rows,
    )


# ==========================================================
# Export High
# ==========================================================


def export_high(
    analysis: dict[str, Any],
) -> Path:
    """
    Export high findings.
    """

    results = analysis["results"]

    lines = []

    for finding in results:

        if finding.get("severity") != "high":
            continue

        lines.append(finding.get("url", ""))

    return write_text(
        HIGH_FILE,
        lines,
    )


# ==========================================================
# Export Critical
# ==========================================================


def export_critical(
    analysis: dict[str, Any],
) -> Path:
    """
    Export critical findings.
    """

    results = analysis["results"]

    lines = []

    for finding in results:

        if finding.get("severity") != "critical":
            continue

        lines.append(finding.get("url", ""))

    return write_text(
        CRITICAL_FILE,
        lines,
    )


# ==========================================================
# Export Summary
# ==========================================================


def export_summary(
    analysis: dict[str, Any],
) -> Path:
    """
    Export summary.
    """

    statistics = analysis["statistics"]

    lines = [
        "Nuclei Summary",
        "=" * 60,
        f"Targets         : {statistics.get('total_targets', 0)}",
        f"Findings        : {statistics.get('total_findings', 0)}",
        f"Critical        : {statistics.get('critical', 0)}",
        f"High            : {statistics.get('high', 0)}",
        f"Medium          : {statistics.get('medium', 0)}",
        f"Low             : {statistics.get('low', 0)}",
        f"Info            : {statistics.get('info', 0)}",
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

    print()

    print("=" * 60)
    print("Nuclei Scan Summary")
    print("=" * 60)

    print(f"{'Targets':<25}" f"{statistics.get('total_targets', 0)}")

    print(f"{'Findings':<25}" f"{statistics.get('total_findings', 0)}")

    print(f"{'Critical':<25}" f"{statistics.get('critical', 0)}")

    print(f"{'High':<25}" f"{statistics.get('high', 0)}")

    print(f"{'Medium':<25}" f"{statistics.get('medium', 0)}")

    print(f"{'Low':<25}" f"{statistics.get('low', 0)}")

    print(f"{'Info':<25}" f"{statistics.get('info', 0)}")

    print("=" * 60)


# ==========================================================
# Export All
# ==========================================================


def export_all(
    analysis: dict[str, Any],
) -> dict[str, Path]:
    """
    Export all reports.
    """

    files = {
        "txt": export_txt(analysis),
        "json": export_json(analysis),
        "csv": export_csv(analysis),
        "summary": export_summary(analysis),
        "high": export_high(analysis),
        "critical": export_critical(analysis),
    }

    show_summary(
        analysis,
    )

    return files


# ==========================================================
# Exports
# ==========================================================

__all__ = [
    "export_all",
]
