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

)

def ensure_output_directory() -> Path:

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
    Write iterable values into a file.

    Args:
        filename:
            Output filename.

        values:
            Iterable values.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

    with output_file.open(

        "w",

        encoding="utf-8",

    ) as file:

        for value in sorted(

            set(values)

        ):

            file.write(

                f"{value}\n"

            )

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
) -> list:
    """
    Collect one analysis field
    from every JavaScript file.

    Args:
        results:
            JavaScript results.

        key:
            Analysis field.

    Returns:
        list
    """

    collected = set()

    for metadata in results.values():

        analysis = metadata.get(

            "analysis",

            {},

        )

        collected.update(

            analysis.get(

                key,

                [],

            )

        )

    return sorted(

        collected

    )


# ==========================================================
# Collect Secrets
# ==========================================================

def collect_secret_items(
    results: dict,
) -> dict:
    """
    Collect detected secrets.

    Returns:
        dict
    """

    secrets = {}

    for metadata in results.values():

        secret_data = metadata.get(

            "secrets",

            {},

        )

        findings = secret_data.get(

            "findings",

            {},

        )

        for secret_type, values in findings.items():

            secrets.setdefault(

                secret_type,

                set(),

            ).update(

                values

            )

    return {

        key: sorted(value)

        for key, value

        in secrets.items()

    }


# ==========================================================
# Generic Analysis Export
# ==========================================================

def export_analysis(
    results: dict,
    key: str,
    filename: str,
) -> Path:
    """
    Generic exporter for
    analysis fields.

    Args:
        results:
            JavaScript results.

        key:
            Analysis key.

        filename:
            Output filename.

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
) -> Path:
    """
    Export JSON report.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

    with output_file.open(

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

        f"JSON exported to {output_file}"

    )

    return output_file


# ==========================================================
# Save Human Readable Report
# ==========================================================

def save_results(
    results: dict,
    filename: str = "javascript.txt",
) -> Path:
    """
    Save JavaScript analysis report.

    Returns:
        Path
    """

    output_file = (

        ensure_output_directory()

        / filename

    )

    with output_file.open(

        "w",

        encoding="utf-8",

    ) as file:

        for url, metadata in sorted(

            results.items()

        ):

            analysis = metadata.get(

                "analysis",

                {},

            )

            statistics = analysis.get(

                "statistics",

                {},

            )

            secrets = metadata.get(

                "secrets",

                {},

            )

            findings = secrets.get(

                "findings",

                {},

            )

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

                    f"{key:<20}: {value}\n"

                )

            if findings:

                file.write(

                    "\nSecrets\n"

                )

                file.write(

                    "-" * 80 + "\n"

                )

                for secret_type, values in findings.items():

                    file.write(

                        f"[{secret_type}]\n"

                    )

                    for value in values:

                        file.write(

                            f"  - {value}\n"

                        )

                    file.write("\n")

            file.write("\n")

    success(

        f"Results saved to {output_file}"

    )

    return output_file


# ==========================================================
# Export Analysis Files
# ==========================================================

def export_urls(
    results: dict,
) -> Path:

    return export_analysis(

        results,

        "urls",

        "urls.txt",

    )


def export_comments(
    results: dict,
) -> Path:

    return export_analysis(

        results,

        "comments",

        "comments.txt",

    )


def export_strings(
    results: dict,
) -> Path:

    return export_analysis(

        results,

        "strings",

        "strings.txt",

    )


def export_source_maps(
    results: dict,
) -> Path:

    return export_analysis(

        results,

        "source_maps",

        "source_maps.txt",

    )


def export_endpoints(
    results: dict,
) -> Path:

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
) -> Path:
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
    """

    save_results(
        results
    )

    export_json(
        results
    )

    export_urls(
        results
    )

    export_comments(
        results
    )

    export_strings(
        results
    )

    export_source_maps(
        results
    )

    export_endpoints(
        results
    )

    export_secrets(
        results
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
    Display summary.
    """

    total = len(results) + len(failed)

    success_rate = (

        (len(results) / total) * 100

        if total

        else 0

    )

    print("\n" + "=" * 80)
    print("JavaScript Analysis Summary")
    print("=" * 80)

    print(f"{'Processed':<20}{total}")
    print(f"{'Downloaded':<20}{len(results)}")
    print(f"{'Failed':<20}{len(failed)}")

    print("-" * 80)

    print(f"{'Success Rate':<20}{success_rate:.1f}%")
    print(f"{'Elapsed':<20}{elapsed:.2f} sec")

    print("=" * 80)

    if failed:

        print("\nFailed Downloads")
        print("-" * 80)

        for item in failed:

            print(f" • {item}")

        print("-" * 80)