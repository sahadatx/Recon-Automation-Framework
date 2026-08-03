"""
Virtual Host Discovery Exporter

Export Virtual Host Discovery
results into multiple formats.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config.config import VHOST_OUTPUT_DIR
from core.logger import success, warning

# ==========================================================
# Create Output Directory
# ==========================================================


def create_output_directory() -> Path:
    """
    Create Virtual Host Discovery output directory.

    Returns:
        Output directory path.
    """

    VHOST_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return VHOST_OUTPUT_DIR


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
                sort_keys=True,
                default=str,
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
            Virtual Host Discovery analysis.

    Returns:
        Output file path.
    """

    return write_json(
        VHOST_OUTPUT_DIR / "results.json",
        analysis,
    )


# ==========================================================
# Export TXT
# ==========================================================


def export_txt(
    analysis: dict[str, Any],
) -> Path:
    """
    Export discovered virtual hosts.

    Args:
        analysis:
            Virtual Host Discovery analysis.

    Returns:
        Output file path.
    """

    results = analysis["results"]

    lines: list[str] = []

    for result in results:

        lines.append(
            f"{result.get('host', '-')}"
            f"\t"
            f"{result.get('status', '-')}"
            f"\t"
            f"{result.get('url', '-')}"
        )

    return write_text(
        VHOST_OUTPUT_DIR / "results.txt",
        lines,
    )


# ==========================================================
# Export Interesting Hosts
# ==========================================================


def export_interesting(
    analysis: dict[str, Any],
) -> Path:
    """
    Export interesting virtual hosts.

    Args:
        analysis:
            Virtual Host Discovery analysis.

    Returns:
        Output file path.
    """

    statistics = analysis["statistics"]

    interesting = statistics.get(
        "interesting",
        [],
    )

    lines: list[str] = []

    for result in interesting:

        lines.append(
            f"{result.get('host', '-')}"
            f"\t"
            f"{result.get('status', '-')}"
            f"\t"
            f"{result.get('url', '-')}"
        )

    return write_text(
        VHOST_OUTPUT_DIR / "interesting.txt",
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
            Virtual Host Discovery analysis.

    Returns:
        Output file path.
    """

    statistics = analysis["statistics"]

    lines = [
        "Virtual Host Discovery Summary",
        "=" * 80,
        f"Discovered Hosts        : {statistics['total_results']}",
        f"Interesting Hosts       : {statistics['interesting_hosts']}",
        "",
        f"HTTP 200                : {statistics['status_200']}",
        f"HTTP 204                : {statistics['status_204']}",
        f"HTTP 301                : {statistics['status_301']}",
        f"HTTP 302                : {statistics['status_302']}",
        f"HTTP 307                : {statistics['status_307']}",
        f"HTTP 401                : {statistics['status_401']}",
        f"HTTP 403                : {statistics['status_403']}",
        "",
    ]

    return write_text(
        VHOST_OUTPUT_DIR / "summary.txt",
        lines,
    )


# ==========================================================
# Export All
# ==========================================================


def export_all(
    analysis: dict[str, Any],
) -> None:
    """
    Export all Virtual Host Discovery reports.

    Args:
        analysis:
            Virtual Host Discovery analysis.
    """

    exporters = (
        export_json,
        export_txt,
        export_interesting,
        export_summary,
    )

    for exporter in exporters:

        try:

            exporter(analysis)

        except Exception as error:

            warning(f"{exporter.__name__}: {error}")

    success("Virtual Host Discovery reports exported successfully.")


# ==========================================================
# Show Summary
# ==========================================================


def show_summary(
    analysis: dict[str, Any],
) -> None:
    """
    Display Virtual Host Discovery summary.
    """

    statistics = analysis["statistics"]

    print()

    print("=" * 80)

    print("Virtual Host Discovery Summary")

    print("=" * 80)

    print(f"{'Discovered Hosts':<30}" f"{statistics['total_results']}")

    print(f"{'Interesting Hosts':<30}" f"{statistics['interesting_hosts']}")

    print(f"{'HTTP 200':<30}" f"{statistics['status_200']}")

    print(f"{'HTTP 204':<30}" f"{statistics['status_204']}")

    print(f"{'HTTP 301':<30}" f"{statistics['status_301']}")

    print(f"{'HTTP 302':<30}" f"{statistics['status_302']}")

    print(f"{'HTTP 307':<30}" f"{statistics['status_307']}")

    print(f"{'HTTP 401':<30}" f"{statistics['status_401']}")

    print(f"{'HTTP 403':<30}" f"{statistics['status_403']}")

    print("=" * 80)


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]
