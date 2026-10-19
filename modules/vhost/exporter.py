from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config.config import VHOST_OUTPUT_DIR
from core.logger import success, warning


def create_output_directory() -> Path:


    VHOST_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return VHOST_OUTPUT_DIR


def write_text(
    output_file: Path,
    lines: list[str],
) -> Path:


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


def write_json(
    output_file: Path,
    data: Any,
) -> Path:


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


def export_json(
    analysis: dict[str, Any],
) -> Path:


    return write_json(
        VHOST_OUTPUT_DIR / "results.json",
        analysis,
    )


def export_txt(
    analysis: dict[str, Any],
) -> Path:


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


def export_interesting(
    analysis: dict[str, Any],
) -> Path:


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


def export_summary(
    analysis: dict[str, Any],
) -> Path:


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


def export_all(
    analysis: dict[str, Any],
) -> None:


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


def show_summary(
    analysis: dict[str, Any],
) -> None:


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


__all__ = [
    "export_all",
]
