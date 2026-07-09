"""
Nuclei Exporter

Exports Nuclei findings into
multiple report formats.
"""

import json
import csv

from pathlib import Path

from core.logger import (
    success,
)


# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIRECTORY = (

    Path("output")

    / "nuclei"

)


# ==========================================================
# Create Output Directory
# ==========================================================

def ensure_output_directory():
    """
    Create output directory.

    Returns:
        Path
    """

    OUTPUT_DIRECTORY.mkdir(

        parents=True,

        exist_ok=True,

    )

    return OUTPUT_DIRECTORY


# ==========================================================
# Save Text
# ==========================================================

def write_text(
    filename: str,
    lines: list[str],
):
    """
    Save text report.

    Args:
        filename:
            Output filename.

        lines:
            Text lines.

    Returns:
        Path
    """

    output = (

        ensure_output_directory()

        / filename

    )

    with output.open(

        "w",

        encoding="utf-8",

    ) as file:

        file.write(

            "\n".join(
                lines
            )

        )

    success(

        f"Saved {output}"

    )

    return output


# ==========================================================
# Export TXT
# ==========================================================

def export_txt(
    findings: list,
    statistics: dict,
    filename: str = "results.txt",
):
    """
    Export TXT report.

    Args:
        findings:
            Filtered findings.

        statistics:
            Generated statistics.

        filename:
            Output filename.

    Returns:
        Path
    """

    lines = []

    lines.append(

        "=" * 80

    )

    lines.append(

        "Nuclei Scan Report"

    )

    lines.append(

        "=" * 80

    )

    lines.append("")

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    lines.append(

        "Summary"

    )

    lines.append(

        "-" * 80

    )

    lines.append(

        f"Total Findings : {statistics.get('total_findings', 0)}"

    )

    lines.append(

        f"Critical       : {statistics.get('critical', 0)}"

    )

    lines.append(

        f"High           : {statistics.get('high', 0)}"

    )

    lines.append(

        f"Medium         : {statistics.get('medium', 0)}"

    )

    lines.append(

        f"Low            : {statistics.get('low', 0)}"

    )

    lines.append(

        f"Info           : {statistics.get('info', 0)}"

    )

    lines.append("")

    lines.append(

        "=" * 80

    )

    lines.append(

        "Findings"

    )

    lines.append(

        "=" * 80

    )

    # ------------------------------------------------------
    # Findings
    # ------------------------------------------------------

    for finding in findings:

        lines.append(

            f"[{finding['severity'].upper()}]"

        )

        lines.append(

            f"URL          : {finding['url']}"

        )

        lines.append(

            f"Template     : {finding['template_name']}"

        )

        lines.append(

            f"Template ID  : {finding['template_id']}"

        )

        lines.append(

            f"Protocol     : {finding['protocol']}"

        )

        lines.append(

            f"Matcher      : {finding['matcher']}"

        )

        if finding.get(

            "description"

        ):

            lines.append(

                f"Description  : {finding['description']}"

            )

        if finding.get(

            "tags"

        ):

            lines.append(

                f"Tags         : {', '.join(finding['tags'])}"

            )

        lines.append(

            "-" * 80

        )

    return write_text(

        filename,

        lines,

    )


# ==========================================================
# Export JSON
# ==========================================================

def export_json(
    findings: list,
    statistics: dict,
    filename: str = "results.json",
):
    """
    Export JSON report.

    Args:
        findings:
            Filtered findings.

        statistics:
            Scan statistics.

        filename:
            Output filename.

    Returns:
        Path
    """

    output = (

        ensure_output_directory()

        / filename

    )

    data = {

        "findings": findings,

        "statistics": statistics,

    }

    with output.open(

        "w",

        encoding="utf-8",

    ) as file:

        json.dump(

            data,

            file,

            indent=4,

            sort_keys=True,

        )

    success(

        f"Saved {output}"

    )

    return output


# ==========================================================
# Export CSV
# ==========================================================

def export_csv(
    findings: list,
    filename: str = "results.csv",
):
    """
    Export CSV report.

    Args:
        findings:
            Filtered findings.

        filename:
            Output filename.

    Returns:
        Path
    """

    output = (

        ensure_output_directory()

        / filename

    )

    with output.open(

        "w",

        newline="",

        encoding="utf-8",

    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow([

            "Severity",

            "URL",

            "Template ID",

            "Template Name",

            "Protocol",

            "Matcher",

            "Tags",

        ])

        for finding in findings:

            writer.writerow([

                finding.get(
                    "severity",
                    "",
                ),

                finding.get(
                    "url",
                    "",
                ),

                finding.get(
                    "template_id",
                    "",
                ),

                finding.get(
                    "template_name",
                    "",
                ),

                finding.get(
                    "protocol",
                    "",
                ),

                finding.get(
                    "matcher",
                    "",
                ),

                ", ".join(

                    finding.get(

                        "tags",

                        [],

                    )

                ),

            ])

    success(

        f"Saved {output}"

    )

    return output


# ==========================================================
# Export Markdown
# ==========================================================

def export_markdown(
    findings: list,
    statistics: dict,
    filename: str = "results.md",
):
    """
    Export Markdown report.

    Args:
        findings:
            Filtered findings.

        statistics:
            Scan statistics.

        filename:
            Output filename.

    Returns:
        Path
    """

    lines = []

    lines.append(

        "# Nuclei Scan Report"

    )

    lines.append("")

    lines.append(

        "## Summary"

    )

    lines.append("")

    lines.append(

        f"- **Total Findings:** {statistics.get('total_findings', 0)}"

    )

    lines.append(

        f"- **Critical:** {statistics.get('critical', 0)}"

    )

    lines.append(

        f"- **High:** {statistics.get('high', 0)}"

    )

    lines.append(

        f"- **Medium:** {statistics.get('medium', 0)}"

    )

    lines.append(

        f"- **Low:** {statistics.get('low', 0)}"

    )

    lines.append(

        f"- **Info:** {statistics.get('info', 0)}"

    )

    lines.append("")

    lines.append(

        "## Findings"

    )

    lines.append("")

    for finding in findings:

        lines.append(

            f"### {finding['template_name']}"

        )

        lines.append("")

        lines.append(

            f"- **Severity:** {finding['severity']}"

        )

        lines.append(

            f"- **URL:** {finding['url']}"

        )

        lines.append(

            f"- **Template ID:** {finding['template_id']}"

        )

        lines.append(

            f"- **Protocol:** {finding['protocol']}"

        )

        lines.append(

            f"- **Matcher:** {finding['matcher']}"

        )

        if finding.get(

            "description"

        ):

            lines.append(

                f"- **Description:** {finding['description']}"

            )

        if finding.get(

            "tags"

        ):

            lines.append(

                f"- **Tags:** {', '.join(finding['tags'])}"

            )

        lines.append("")

    return write_text(

        filename,

        lines,

    )


# ==========================================================
# Show Summary
# ==========================================================

def show_summary(
    statistics: dict,
):
    """
    Display scan summary.

    Args:
        statistics:
            Generated statistics.
    """

    print()

    print("=" * 80)

    print(
        "Nuclei Scan Summary"
    )

    print("=" * 80)

    print(
        f"{'Total Findings':<30}"
        f"{statistics.get('total_findings', 0)}"
    )

    print(
        f"{'Critical':<30}"
        f"{statistics.get('critical', 0)}"
    )

    print(
        f"{'High':<30}"
        f"{statistics.get('high', 0)}"
    )

    print(
        f"{'Medium':<30}"
        f"{statistics.get('medium', 0)}"
    )

    print(
        f"{'Low':<30}"
        f"{statistics.get('low', 0)}"
    )

    print(
        f"{'Info':<30}"
        f"{statistics.get('info', 0)}"
    )

    print(
        f"{'Unique Templates':<30}"
        f"{statistics.get('unique_templates', 0)}"
    )

    print(
        f"{'Unique Targets':<30}"
        f"{statistics.get('unique_targets', 0)}"
    )

    print("=" * 80)


# ==========================================================
# Export All
# ==========================================================

def export_all(
    findings: list,
    statistics: dict,
):
    """
    Export all report formats.

    Args:
        findings:
            Filtered findings.

        statistics:
            Generated statistics.

    Returns:
        dict
    """

    files = {

        "text": export_txt(

            findings,

            statistics,

        ),

        "json": export_json(

            findings,

            statistics,

        ),

        "csv": export_csv(

            findings,

        ),

        "markdown": export_markdown(

            findings,

            statistics,

        ),

    }

    show_summary(
        statistics
    )

    return files


# ==========================================================
# Self Test
# ==========================================================

if __name__ == "__main__":

    sample = [

        {

            "severity": "high",

            "url": "https://example.com/.git/config",

            "template_id": "git-config",

            "template_name": "Git Config Disclosure",

            "protocol": "http",

            "matcher": "word",

            "description": "Exposed Git configuration.",

            "tags": [

                "git",

                "exposure",

            ],

        }

    ]

    statistics = {

        "total_findings": 1,

        "critical": 0,

        "high": 1,

        "medium": 0,

        "low": 0,

        "info": 0,

        "unique_templates": 1,

        "unique_targets": 1,

    }

    export_all(

        sample,

        statistics,

    )