"""
Dashboard Exporter

Export dashboard analysis results.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.logger import (
    success,
    warning,
)

from .constants import (
    OUTPUT_DIR,
    DASHBOARD_JSON,
    DASHBOARD_TXT,
    SUMMARY_FILE,
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
# Export JSON
# ==========================================================

def export_json(
    analysis: dict[str, Any],
) -> Path:
    """
    Export dashboard JSON.
    """

    return write_json(
        DASHBOARD_JSON,
        analysis,
    )


# ==========================================================
# Export TXT
# ==========================================================

def export_txt(
    analysis: dict[str, Any],
) -> Path:
    """
    Export dashboard text report.
    """

    results = analysis["results"]

    statistics = analysis["statistics"]

    lines = [

        "Dashboard",

        "=" * 80,

        "",

        f"Target              : {statistics['target']}",

        f"Elapsed Time        : {statistics['elapsed']} sec",

        f"Modules             : {statistics['modules']}",

        f"Completed Modules   : {statistics['completed_modules']}",

        f"Failed Modules      : {statistics['failed_modules']}",

        f"Findings            : {statistics['findings']}",

        "",

        "Modules",

        "-" * 80,

    ]

    for module in results.get(
        "module_names",
        [],
    ):

        lines.append(
            f"• {module}"
        )

    return write_text(
        DASHBOARD_TXT,
        lines,
    )


# ==========================================================
# Export Summary
# ==========================================================

def export_summary(
    analysis: dict[str, Any],
) -> Path:
    """
    Export dashboard summary.
    """

    statistics = analysis["statistics"]

    lines = [

        "Dashboard Summary",

        "=" * 40,

        f"Target             : {statistics['target']}",

        f"Modules            : {statistics['modules']}",

        f"Completed Modules  : {statistics['completed_modules']}",

        f"Failed Modules     : {statistics['failed_modules']}",

        f"Findings           : {statistics['findings']}",

        f"Elapsed Time       : {statistics['elapsed']} sec",

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
    Display dashboard summary.
    """

    statistics = analysis["statistics"]

    print()

    print("=" * 80)

    print(
        "Dashboard Summary".center(80)
    )

    print("=" * 80)

    print(
        f"Target             : {statistics['target']}"
    )

    print(
        f"Modules            : {statistics['modules']}"
    )

    print(
        f"Completed Modules  : {statistics['completed_modules']}"
    )

    print(
        f"Failed Modules     : {statistics['failed_modules']}"
    )

    print(
        f"Findings           : {statistics['findings']}"
    )

    print(
        f"Elapsed Time       : {statistics['elapsed']} sec"
    )

    print("=" * 80)


# ==========================================================
# Export All
# ==========================================================

def export_all(
    analysis: dict[str, Any],
) -> None:
    """
    Export all dashboard reports.
    """

    create_output_directory()

    export_json(
        analysis,
    )

    export_txt(
        analysis,
    )

    export_summary(
        analysis,
    )

    show_summary(
        analysis,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]