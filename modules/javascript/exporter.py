"""
JavaScript Exporter

Exports JavaScript analysis results.
"""

import json

from pathlib import Path

from config.config import (

    JAVASCRIPT_OUTPUT_DIR,

)

from core.logger import (

    success,

    warning,

)


# ==========================================================
# Ensure Output Directory
# ==========================================================

def ensure_output_directory() -> Path:
    """
    Create output directory.

    Returns:
        Path
    """

    JAVASCRIPT_OUTPUT_DIR.mkdir(

        parents=True,

        exist_ok=True,

    )

    return JAVASCRIPT_OUTPUT_DIR


# ==========================================================
# Write List
# ==========================================================

def write_list(
    filename: str,
    values,
) -> Path:
    """
    Write iterable values
    into a text file.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

    values = sorted(

        set(values)

    )

    try:

        with output_file.open(

            "w",

            encoding="utf-8",

        ) as file:

            for value in values:

                file.write(

                    f"{value}\n"

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
# Collect Analysis Items
# ==========================================================

def collect_analysis_items(
    results: dict,
    key: str,
):
    """
    Collect one analysis field
    from all JavaScript files.

    Returns:
        list
    """

    collected = set()

    for metadata in results.values():

        if not metadata:

            continue

        analysis = metadata.get(

            "analysis"

        ) or {}

        values = analysis.get(

            key,

            [],

        )

        if values:

            collected.update(

                values

            )

    return sorted(

        collected

    )


# ==========================================================
# Collect Secret Items
# ==========================================================

def collect_secret_items(
    results: dict,
):
    """
    Collect detected secrets.

    Returns:
        dict
    """

    secrets = {}

    for metadata in results.values():

        if not metadata:

            continue

        secret_data = metadata.get(

            "secrets"

        ) or {}

        findings = secret_data.get(

            "findings"

        ) or {}

        for secret_type, values in findings.items():

            secrets.setdefault(

                secret_type,

                set(),

            ).update(

                values

            )

    return {

        key: sorted(values)

        for key, values

        in secrets.items()

    }


# ==========================================================
# Generic Analysis Export
# ==========================================================

def export_analysis(
    results: dict,
    key: str,
    filename: str,
):
    """
    Export one analysis field.

    Returns:
        Path
    """

    values = collect_analysis_items(

        results,

        key,

    )

    return write_list(

        filename,

        values,

    )


# ==========================================================
# Export JSON
# ==========================================================

def export_json(
    results: dict,
    filename: str = "javascript.json",
):
    """
    Export JSON report.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

    try:

        with output_file.open(

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                results,

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

        f"JSON exported to {output_file}"

    )

    return output_file


# ==========================================================
# Save Human Readable Report
# ==========================================================

def save_results(
    results: dict,
    filename: str = "javascript.txt",
):
    """
    Save JavaScript report.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

    try:

        with output_file.open(

            "w",

            encoding="utf-8",

        ) as file:

            for url, metadata in sorted(

                results.items()

            ):

                if not metadata:

                    continue

                analysis = metadata.get(

                    "analysis"

                ) or {}

                statistics = analysis.get(

                    "statistics"

                ) or {}

                secrets = metadata.get(

                    "secrets"

                ) or {}

                findings = secrets.get(

                    "findings"

                ) or {}

                file.write(

                    "=" * 80 + "\n"

                )

                file.write(

                    f"JavaScript : {url}\n"

                )

                file.write(

                    f"Saved File : "

                    f"{metadata.get('path','-')}\n"

                )

                file.write(

                    f"Status     : "

                    f"{metadata.get('status','-')}\n\n"

                )

                file.write(

                    "Statistics\n"

                )

                file.write(

                    "-" * 80 + "\n"

                )

                for key, value in statistics.items():

                    file.write(

                        f"{key:<24}: {value}\n"

                    )

                if findings:

                    file.write(

                        "\nSecrets\n"

                    )

                    file.write(

                        "-" * 80 + "\n"

                    )

                    for secret_type, values in sorted(

                        findings.items()

                    ):

                        file.write(

                            f"[{secret_type}]\n"

                        )

                        for value in values:

                            file.write(

                                f"  - {value}\n"

                            )

                        file.write("\n")

                file.write("\n")

    except Exception as error:

        warning(

            f"{output_file}: {error}"

        )

        return output_file

    success(

        f"Results saved to {output_file}"

    )

    return output_file


# ==========================================================
# Export Analysis Files
# ==========================================================

def export_urls(
    results: dict,
):

    return export_analysis(

        results,

        "urls",

        "urls.txt",

    )


def export_comments(
    results: dict,
):

    return export_analysis(

        results,

        "comments",

        "comments.txt",

    )


def export_strings(
    results: dict,
):

    return export_analysis(

        results,

        "strings",

        "strings.txt",

    )


def export_source_maps(
    results: dict,
):

    return export_analysis(

        results,

        "source_maps",

        "source_maps.txt",

    )


def export_endpoints(
    results: dict,
):

    return export_analysis(

        results,

        "endpoints",

        "endpoints.txt",

    )


# ==========================================================
# Export Secrets
# ==========================================================

def export_secrets(
    results: dict,
    filename: str = "secrets.txt",
):
    """
    Export detected secrets.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

    secrets = collect_secret_items(

        results

    )

    try:

        with output_file.open(

            "w",

            encoding="utf-8",

        ) as file:

            if not secrets:

                file.write(

                    "No secrets detected.\n"

                )

            else:

                for secret_type, values in sorted(

                    secrets.items()

                ):

                    file.write(

                        "=" * 80 + "\n"

                    )

                    file.write(

                        f"{secret_type}\n"

                    )

                    file.write(

                        "-" * 80 + "\n"

                    )

                    for value in values:

                        file.write(

                            value + "\n"

                        )

                    file.write("\n")

    except Exception as error:

        warning(

            f"{output_file}: {error}"

        )

        return output_file

    success(

        f"Secrets exported to {output_file}"

    )

    return output_file


# ==========================================================
# Export All
# ==========================================================

def export_all(
    results: dict,
):
    """
    Export all JavaScript reports.

    Returns:
        None
    """

    exporters = (

        save_results,

        export_json,

        export_urls,

        export_comments,

        export_strings,

        export_source_maps,

        export_endpoints,

        export_secrets,

    )

    for exporter in exporters:

        try:

            exporter(

                results

            )

        except Exception as error:

            warning(

                f"{exporter.__name__}: {error}"

            )

    success(

        "JavaScript analysis export completed."

    )


# ==========================================================
# Summary
# ==========================================================

def show_summary(
    results: dict,
    failed: list,
    elapsed: float,
):
    """
    Display JavaScript analysis summary.

    Returns:
        None
    """

    total = len(

        results

    ) + len(

        failed

    )

    downloaded = len(

        results

    )

    success_rate = (

        (downloaded / total) * 100

        if total

        else 0.0

    )

    statistics = {

        "processed": total,

        "downloaded": downloaded,

        "failed": len(

            failed

        ),

        "success_rate": success_rate,

        "elapsed": elapsed,

    }

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

        f"{'Processed Files':<24}"

        f"{statistics['processed']}"

    )

    print(

        f"{'Downloaded Files':<24}"

        f"{statistics['downloaded']}"

    )

    print(

        f"{'Failed Files':<24}"

        f"{statistics['failed']}"

    )

    print(

        "-" * 80

    )

    print(

        f"{'Success Rate':<24}"

        f"{statistics['success_rate']:.1f}%"

    )

    print(

        f"{'Elapsed':<24}"

        f"{statistics['elapsed']:.2f} sec"

    )

    print(

        "=" * 80

    )

    if failed:

        print()

        print(

            "Failed Downloads"

        )

        print(

            "-" * 80

        )

        for item in sorted(

            failed

        ):

            print(

                f" • {item}"

            )

        print(

            "-" * 80

        )



