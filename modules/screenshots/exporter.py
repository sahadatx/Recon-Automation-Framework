from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from core.logger import success, warning
from modules.screenshots.constants import (
    RESULTS_JSON,
    RESULTS_TXT,
    SCREENSHOT_OUTPUT_DIR,
    SUMMARY_TXT,
)


def ensure_output_directory() -> Path:


    SCREENSHOT_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return SCREENSHOT_OUTPUT_DIR


def write_text(
    path: Path,
    lines: list[str],
) -> Path:


    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("\n".join(lines))

    success(f"Saved {path}")

    return path


def write_json(
    path: Path,
    data: Any,
) -> Path:


    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            sort_keys=True,
        )

    success(f"Saved {path}")

    return path


def write_csv(
    path: Path,
    results: list[dict],
) -> Path:


    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "URL",
                "Title",
                "Status",
                "Captured",
                "Screenshot",
                "Filesize",
                "Elapsed",
            ]
        )

        for item in results:

            writer.writerow(
                [
                    item.get("url"),
                    item.get("title"),
                    item.get("status"),
                    item.get("captured"),
                    item.get("path"),
                    item.get("filesize"),
                    item.get("elapsed"),
                ]
            )

    success(f"Saved {path}")

    return path


def export_results(
    analysis: dict[str, Any],
) -> Path:


    lines = []

    for result in analysis.get("results", []):

        lines.append("=" * 80)

        lines.append(f"URL        : {result.get('url', '-')}")

        lines.append(f"Title      : {result.get('title', '-')}")

        lines.append(f"Captured   : {result.get('captured', False)}")

        lines.append(f"Status     : {result.get('status', '-')}")

        lines.append(f"Screenshot : {result.get('path', '-')}")

        lines.append(f"Size       : {result.get('filesize', 0)} bytes")

        lines.append(f"Time       : {result.get('elapsed', 0)} sec")

        lines.append("")

    return write_text(
        RESULTS_TXT,
        lines,
    )


def export_json(
    analysis: dict[str, Any],
) -> Path:


    return write_json(
        RESULTS_JSON,
        analysis,
    )


def export_summary(
    analysis: dict[str, Any],
) -> Path:


    statistics = analysis.get(
        "statistics",
        {},
    )

    lines = [
        "=" * 70,
        "Screenshot Analysis Summary",
        "=" * 70,
        "",
        f"Total Targets       : {statistics.get('total_targets', 0)}",
        f"Captured            : {statistics.get('captured', 0)}",
        f"Failed              : {statistics.get('failed', 0)}",
        f"Success Rate        : {statistics.get('success_rate', 0)}%",
        f"Average Time        : {statistics.get('average_time', 0)} sec",
        f"Average Size        : {statistics.get('average_size', 0)} bytes",
        "",
    ]

    return write_text(
        SUMMARY_TXT,
        lines,
    )


def export_all(
    analysis: dict[str, Any],
) -> None:


    exporters = (
        export_results,
        export_json,
        export_summary,
    )

    for exporter in exporters:

        try:

            exporter(analysis)

        except Exception as error:

            warning(f"{exporter.__name__}: {error}")

    success("Screenshot reports exported successfully.")


def show_summary(
    analysis: dict[str, Any],
) -> None:


    statistics = analysis.get(
        "statistics",
        {},
    )

    print()

    print("=" * 80)

    print("Screenshot Capture Summary")

    print("=" * 80)

    print(f"{'Total Targets':<30}" f"{statistics.get('total_targets', 0)}")

    print(f"{'Captured':<30}" f"{statistics.get('captured', 0)}")

    print(f"{'Failed':<30}" f"{statistics.get('failed', 0)}")

    print(f"{'Success Rate':<30}" f"{statistics.get('success_rate', 0)}%")

    print("=" * 80)


__all__ = [
    "export_results",
    "export_json",
    "export_summary",
    "export_all",
    "show_summary",
]
