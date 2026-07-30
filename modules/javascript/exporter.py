"""
JavaScript Exporter

Export JavaScript analysis results.
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

from modules.javascript.constants import (
    JAVASCRIPT_OUTPUT_DIR,
    RESULTS_TXT,
    RESULTS_JSON,
    RESULTS_CSV,
    SUMMARY_TXT,
    JAVASCRIPT_TXT,
    URLS_TXT,
    ENDPOINTS_TXT,
    SOURCE_MAPS_TXT,
    INTERESTING_FILES_TXT,
    INTERESTING_DIRECTORIES_TXT,
    SECRETS_TXT,
    FILES_DIR,
)


# ==========================================================
# Ensure Output Directory
# ==========================================================

def ensure_output_directory() -> Path:
    """
    Create JavaScript output directory.

    Returns:
        Output directory path.
    """

    JAVASCRIPT_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    FILES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return JAVASCRIPT_OUTPUT_DIR


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

    ensure_output_directory()

    try:

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            for line in lines:

                file.write(
                    f"{line}\n"
                )

    except Exception as error:

        warning(
            f"{output_file}: {error}"
        )

        return output_file

    success(
        f"Saved {output_file}"
    )

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

    ensure_output_directory()

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

        warning(
            f"{output_file}: {error}"
        )

        return output_file

    success(
        f"Saved {output_file}"
    )

    return output_file


# ==========================================================
# Write CSV File
# ==========================================================

def write_csv(
    output_file: Path,
    headers: list[str],
    rows: list[list[Any]],
) -> Path:
    """
    Write CSV file.

    Args:
        output_file:
            Destination file.

        headers:
            CSV headers.

        rows:
            CSV rows.

    Returns:
        Output file path.
    """

    ensure_output_directory()

    try:

        with output_file.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow(
                headers
            )

            writer.writerows(
                rows
            )

    except Exception as error:

        warning(
            f"{output_file}: {error}"
        )

        return output_file

    success(
        f"Saved {output_file}"
    )

    return output_file


# ==========================================================
# Helper Functions
# ==========================================================

def unique_sorted(
    values: list[str],
) -> list[str]:
    """
    Return unique sorted values.
    """

    return sorted(
        {
            value
            for value in values
            if value
        }
    )


def flatten(
    values: list[list[str]],
) -> list[str]:
    """
    Flatten nested lists.
    """

    flattened: list[str] = []

    for value in values:

        flattened.extend(
            value
        )

    return flattened


def collect_analysis(
    results: dict,
    field: str,
) -> list[str]:
    """
    Collect one analysis field
    from every JavaScript file.
    """

    collected: list[str] = []

    for metadata in results.values():

        analysis = metadata.get(
            "analysis",
            {},
        )

        collected.extend(
            analysis.get(
                field,
                [],
            )
        )

    return unique_sorted(
        collected
    )


def collect_interesting(
    results: dict,
    field: str,
) -> list[str]:
    """
    Collect interesting findings.
    """

    collected: list[str] = []

    for metadata in results.values():

        interesting = metadata.get(
            "interesting",
            {},
        )

        collected.extend(
            interesting.get(
                field,
                [],
            )
        )

    return unique_sorted(
        collected
    )


def collect_secrets(
    results: dict,
) -> dict[str, list[str]]:
    """
    Collect detected secrets.
    """

    secrets: dict[
        str,
        set[str],
    ] = {}

    for metadata in results.values():

        findings = (
            metadata.get(
                "secrets",
                {},
            )
            .get(
                "findings",
                {},
            )
        )

        for (
            secret_type,
            values,
        ) in findings.items():

            secrets.setdefault(
                secret_type,
                set(),
            ).update(
                values
            )

    return {

        key: sorted(values)

        for (
            key,
            values,
        ) in secrets.items()

    }

# ==========================================================
# Export Results (TXT)
# ==========================================================

def export_results(
    analysis: dict,
) -> Path:
    """
    Export human-readable results.
    """

    lines: list[str] = []

    statistics = analysis[
        "statistics"
    ]

    for (
        javascript,
        metadata,
    ) in sorted(
        analysis[
            "results"
        ].items()
    ):

        file_statistics = (
            metadata.get(
                "analysis",
                {},
            ).get(
                "statistics",
                {},
            )
        )

        lines.append(
            "=" * 80
        )

        lines.append(
            f"JavaScript : {javascript}"
        )

        lines.append(
            f"Saved File : {metadata.get('path','-')}"
        )

        lines.append(
            f"Status     : {metadata.get('status','-')}"
        )

        lines.append("")

        lines.append(
            "Statistics"
        )

        lines.append(
            "-" * 80
        )

        for (
            key,
            value,
        ) in sorted(
            file_statistics.items()
        ):

            lines.append(
                f"{key:<28}: {value}"
            )

        lines.append("")

    lines.append(
        "=" * 80
    )

    lines.append(
        "Overall Statistics"
    )

    lines.append(
        "-" * 80
    )

    for (
        key,
        value,
    ) in sorted(
        statistics.items()
    ):

        if isinstance(
            value,
            dict,
        ):

            continue

        lines.append(
            f"{key:<28}: {value}"
        )

    return write_text(
        RESULTS_TXT,
        lines,
    )


# ==========================================================
# Export JSON
# ==========================================================

def export_json(
    analysis: dict,
) -> Path:
    """
    Export JSON report.
    """

    return write_json(
        RESULTS_JSON,
        analysis,
    )


# ==========================================================
# Export CSV
# ==========================================================

def export_csv(
    analysis: dict,
) -> Path:
    """
    Export CSV report.
    """

    headers = [

        "javascript",

        "status",

        "saved_file",

        "urls",

        "comments",

        "strings",

        "source_maps",

        "endpoints",

        "interesting_files",

        "interesting_directories",

        "secret_types",

        "total_secrets",

    ]

    rows: list[
        list
    ] = []

    for (
        javascript,
        metadata,
    ) in sorted(
        analysis[
            "results"
        ].items()
    ):

        js_statistics = (
            metadata.get(
                "analysis",
                {},
            ).get(
                "statistics",
                {},
            )
        )

        interesting_statistics = (
            metadata.get(
                "interesting",
                {},
            ).get(
                "statistics",
                {},
            )
        )

        secret_statistics = (
            metadata.get(
                "secrets",
                {},
            ).get(
                "statistics",
                {},
            )
        )

        rows.append(

            [

                javascript,

                metadata.get(
                    "status",
                    "",
                ),

                metadata.get(
                    "path",
                    "",
                ),

                js_statistics.get(
                    "urls",
                    0,
                ),

                js_statistics.get(
                    "comments",
                    0,
                ),

                js_statistics.get(
                    "strings",
                    0,
                ),

                js_statistics.get(
                    "source_maps",
                    0,
                ),

                js_statistics.get(
                    "endpoints",
                    0,
                ),

                interesting_statistics.get(
                    "interesting_files",
                    0,
                ),

                interesting_statistics.get(
                    "interesting_directories",
                    0,
                ),

                secret_statistics.get(
                    "secret_types",
                    0,
                ),

                secret_statistics.get(
                    "total_secrets",
                    0,
                ),

            ]

        )

    return write_csv(

        RESULTS_CSV,

        headers,

        rows,

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

    statistics = analysis[
        "statistics"
    ]

    lines = [

        "JavaScript Analysis Summary",

        "=" * 80,

        f"Processed Files           : {statistics['processed_files']}",

        f"URLs                      : {statistics['urls']}",

        f"Comments                  : {statistics['comments']}",

        f"Strings                   : {statistics['strings']}",

        f"Source Maps               : {statistics['source_maps']}",

        f"Endpoints                 : {statistics['endpoints']}",

        f"Interesting Files         : {statistics['interesting_files']}",

        f"Interesting Directories   : {statistics['interesting_directories']}",

        f"Secret Types              : {statistics['secret_types']}",

        f"Total Secrets             : {statistics['total_secrets']}",

        f"Average URLs / File       : {statistics['average_urls_per_file']}",

    ]

    return write_text(

        SUMMARY_TXT,

        lines,

    )

# ==========================================================
# Export JavaScript Files
# ==========================================================

def export_javascript(
    analysis: dict,
) -> Path:
    """
    Export downloaded JavaScript URLs.
    """

    javascript = sorted(
        analysis[
            "results"
        ].keys()
    )

    return write_text(
        JAVASCRIPT_TXT,
        javascript,
    )


# ==========================================================
# Export URLs
# ==========================================================

def export_urls(
    analysis: dict,
) -> Path:
    """
    Export discovered URLs.
    """

    urls = collect_analysis(
        analysis[
            "results"
        ],
        "urls",
    )

    return write_text(
        URLS_TXT,
        urls,
    )


# ==========================================================
# Export Endpoints
# ==========================================================

def export_endpoints(
    analysis: dict,
) -> Path:
    """
    Export discovered endpoints.
    """

    endpoints = collect_analysis(
        analysis[
            "results"
        ],
        "endpoints",
    )

    return write_text(
        ENDPOINTS_TXT,
        endpoints,
    )


# ==========================================================
# Export Source Maps
# ==========================================================

def export_source_maps(
    analysis: dict,
) -> Path:
    """
    Export discovered source maps.
    """

    source_maps = collect_analysis(
        analysis[
            "results"
        ],
        "source_maps",
    )

    return write_text(
        SOURCE_MAPS_TXT,
        source_maps,
    )


# ==========================================================
# Export Interesting Files
# ==========================================================

def export_interesting_files(
    analysis: dict,
) -> Path:
    """
    Export interesting files.
    """

    interesting = collect_interesting(
        analysis[
            "results"
        ],
        "interesting_files",
    )

    return write_text(
        INTERESTING_FILES_TXT,
        interesting,
    )


# ==========================================================
# Export Interesting Directories
# ==========================================================

def export_interesting_directories(
    analysis: dict,
) -> Path:
    """
    Export interesting directories.
    """

    directories = collect_interesting(
        analysis[
            "results"
        ],
        "interesting_directories",
    )

    return write_text(
        INTERESTING_DIRECTORIES_TXT,
        directories,
    )


# ==========================================================
# Export Secrets
# ==========================================================

def export_secrets(
    analysis: dict,
) -> Path:
    """
    Export detected secrets.
    """

    findings = collect_secrets(
        analysis[
            "results"
        ]
    )

    lines: list[str] = []

    if not findings:

        lines.append(
            "No secrets detected."
        )

    else:

        for (
            secret_type,
            values,
        ) in sorted(
            findings.items()
        ):

            lines.append(
                "=" * 80
            )

            lines.append(
                secret_type
            )

            lines.append(
                "-" * 80
            )

            lines.extend(
                values
            )

            lines.append("")

    return write_text(
        SECRETS_TXT,
        lines,
    )

# ==========================================================
# Export All
# ==========================================================

def export_all(
    analysis: dict,
) -> None:
    """
    Export all JavaScript reports.
    """

    exporters = (

        export_results,

        export_json,

        export_csv,

        export_summary,

        export_javascript,

        export_urls,

        export_endpoints,

        export_source_maps,

        export_interesting_files,

        export_interesting_directories,

        export_secrets,

    )

    for exporter in exporters:

        try:

            exporter(
                analysis
            )

        except Exception as error:

            warning(
                f"{exporter.__name__}: {error}"
            )

    success(
        "JavaScript reports exported successfully."
    )


# ==========================================================
# Show Summary
# ==========================================================

def show_summary(
    analysis: dict[str, Any],
) -> None:
    """
    Display JavaScript analysis summary.
    """

    statistics = analysis[
        "statistics"
    ]

    print()

    print(
        "=" * 80
    )

    print(
        "JavaScript Analysis Summary"
    )

    print(
        "=" * 80
    )

    print(
        f"{'Processed Files':<30}"
        f"{statistics['processed_files']}"
    )

    print(
        f"{'URLs':<30}"
        f"{statistics['urls']}"
    )

    print(
        f"{'Comments':<30}"
        f"{statistics['comments']}"
    )

    print(
        f"{'Strings':<30}"
        f"{statistics['strings']}"
    )

    print(
        f"{'Source Maps':<30}"
        f"{statistics['source_maps']}"
    )

    print(
        f"{'Endpoints':<30}"
        f"{statistics['endpoints']}"
    )

    print(
        f"{'Interesting Files':<30}"
        f"{statistics['interesting_files']}"
    )

    print(
        f"{'Interesting Directories':<30}"
        f"{statistics['interesting_directories']}"
    )

    print(
        f"{'Secret Types':<30}"
        f"{statistics['secret_types']}"
    )

    print(
        f"{'Total Secrets':<30}"
        f"{statistics['total_secrets']}"
    )

    print(
        f"{'Average URLs / File':<30}"
        f"{statistics['average_urls_per_file']}"
    )

    print(
        "=" * 80
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "export_results",

    "export_json",

    "export_csv",

    "export_summary",

    "export_javascript",

    "export_urls",

    "export_endpoints",

    "export_source_maps",

    "export_interesting_files",

    "export_interesting_directories",

    "export_secrets",

    "export_all",

    "show_summary",

]