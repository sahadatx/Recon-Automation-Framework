"""
Email Security Exporter

Export Email Security
analysis results.
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

from .constants import (
    OUTPUT_DIR,
    TXT_FILE,
    JSON_FILE,
    CSV_FILE,
    SUMMARY_FILE,
    HIGH_RISK_FILE,
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

    Args:
        output_file:
            Destination file.

        lines:
            File content.

    Returns:
        Output file path.
    """

    try:

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        success(f"Saved {output_file}")

    except OSError as error:

        warning(f"{output_file}: {error}")

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

    Args:
        output_file:
            Destination file.

        data:
            JSON data.

    Returns:
        Output file path.
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

        success(f"Saved {output_file}")

    except OSError as error:

        warning(f"{output_file}: {error}")

    return output_file


# ==========================================================
# Write CSV
# ==========================================================


def write_csv(
    output_file: Path,
    results: list[dict[str, Any]],
) -> Path:
    """
    Write CSV report.

    Args:
        output_file:
            Destination file.

        results:
            Email Security results.

    Returns:
        Output file path.
    """

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
                    "Provider",
                    "Risk",
                    "Score",
                    "SPF",
                    "DKIM",
                    "DMARC",
                    "MTA-STS",
                    "TLS-RPT",
                    "BIMI",
                    "DNSSEC",
                ]
            )

            for result in results:

                writer.writerow(
                    [
                        result.get("target", ""),
                        result.get("provider", ""),
                        result.get("risk", ""),
                        result.get("score", 0),
                        result.get("spf", False),
                        result.get("dkim", False),
                        result.get("dmarc", False),
                        result.get("mta_sts", False),
                        result.get("tls_rpt", False),
                        result.get("bimi", False),
                        result.get("dnssec", False),
                    ]
                )

        success(f"Saved {output_file}")

    except OSError as error:

        warning(f"{output_file}: {error}")

    return output_file


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
# Export TXT
# ==========================================================


def export_txt(
    analysis: dict[str, Any],
) -> Path:
    """
    Export TXT report.
    """

    results = analysis["results"]

    lines: list[str] = []

    for result in results:

        lines.append("=" * 80)

        lines.append(f"Target              : {result.get('target', '-')}")

        lines.append(f"Provider            : {result.get('provider', '-')}")

        lines.append(f"Risk                : {result.get('risk', '-')}")

        lines.append(f"Score               : {result.get('score', 0)}")

        lines.append("MX Records          : " + ", ".join(result.get("mx", [])))

        lines.append(f"SPF                 : {result.get('spf', False)}")

        lines.append(f"DKIM                : {result.get('dkim', False)}")

        lines.append(f"DMARC               : {result.get('dmarc', False)}")

        lines.append(f"MTA-STS             : {result.get('mta_sts', False)}")

        lines.append(f"TLS-RPT             : {result.get('tls_rpt', False)}")

        lines.append(f"BIMI                : {result.get('bimi', False)}")

        lines.append(f"DNSSEC              : {result.get('dnssec', False)}")

        lines.append("Recommendations")

        recommendations = result.get(
            "recommendations",
            [],
        )

        if recommendations:

            for recommendation in recommendations:

                lines.append(f"  - {recommendation}")

        else:

            lines.append("  None")

        lines.append("")

    return write_text(
        TXT_FILE,
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
    """

    return write_csv(
        CSV_FILE,
        analysis["results"],
    )


# ==========================================================
# Export High Risk
# ==========================================================


def export_high_risk(
    analysis: dict[str, Any],
) -> Path:
    """
    Export High/Critical risk targets.
    """

    results = analysis["results"]

    lines: list[str] = []

    for result in results:

        if result.get(
            "risk",
            "",
        ) not in (
            "High",
            "Critical",
        ):
            continue

        lines.append(
            f"{result.get('target', '-')}"
            f" -> "
            f"{result.get('risk', '-')}"
            f" (Score: {result.get('score', 0)})"
        )

    return write_text(
        HIGH_RISK_FILE,
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
    """

    statistics = analysis["statistics"]

    lines = [
        "Email Security Summary",
        "=" * 40,
        f"Targets            : {statistics['targets']}",
        f"Low Risk           : {statistics['low']}",
        f"Medium Risk        : {statistics['medium']}",
        f"High Risk          : {statistics['high']}",
        f"Critical Risk      : {statistics['critical']}",
        f"SPF Enabled        : {statistics['spf_enabled']}",
        f"DKIM Enabled       : {statistics['dkim_enabled']}",
        f"DMARC Enabled      : {statistics['dmarc_enabled']}",
        f"Average Score      : {statistics['average_score']}",
        f"Highest Score      : {statistics['highest_score']}",
        "",
        "Risk Levels",
        "-" * 40,
    ]

    for level, count in statistics["risk_statistics"].items():

        lines.append(f"{level:<20}{count}")

    lines.extend(
        [
            "",
            "Providers",
            "-" * 40,
        ]
    )

    for provider, count in statistics["provider_statistics"].items():

        lines.append(f"{provider:<20}{count}")

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
    Display Email Security summary.
    """

    statistics = analysis["statistics"]

    print()

    print("=" * 80)

    print("Email Security Summary".center(80))

    print("=" * 80)

    print(f"Targets            : {statistics['targets']}")
    print(f"Low Risk           : {statistics['low']}")
    print(f"Medium Risk        : {statistics['medium']}")
    print(f"High Risk          : {statistics['high']}")
    print(f"Critical Risk      : {statistics['critical']}")
    print(f"SPF Enabled        : {statistics['spf_enabled']}")
    print(f"DKIM Enabled       : {statistics['dkim_enabled']}")
    print(f"DMARC Enabled      : {statistics['dmarc_enabled']}")
    print(f"Average Score      : {statistics['average_score']}")
    print(f"Highest Score      : {statistics['highest_score']}")

    print("-" * 80)

    print("Risk Levels")

    print("-" * 80)

    for level, count in statistics["risk_statistics"].items():

        print(f"{level:<30}{count}")

    print("-" * 80)

    print("Providers")

    print("-" * 80)

    for provider, count in statistics["provider_statistics"].items():

        print(f"{provider:<30}{count}")

    print("=" * 80)


# ==========================================================
# Export All
# ==========================================================


def export_all(
    analysis: dict[str, Any],
) -> None:
    """
    Export all reports.
    """

    create_output_directory()

    export_json(analysis)

    export_txt(analysis)

    export_csv(analysis)

    export_high_risk(analysis)

    export_summary(analysis)

    show_summary(analysis)


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "export_all",
]
