"""
TLS Exporter

Export TLS analysis results.
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


# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIR = Path("output/tls")


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

        success(
            f"Saved {output_file}"
        )

    except OSError as error:

        warning(
            f"{output_file}: {error}"
        )

    return output_file


# ==========================================================
# Write CSV
# ==========================================================

def write_csv(
    output_file: Path,
    results: list[dict[str, Any]],
) -> Path:
    """
    Write CSV file.

    Args:
        output_file:
            Destination file.

        results:
            TLS results.

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
                    "Risk Level",
                    "Risk Score",
                    "Days Remaining",
                    "Expired",
                    "Self Signed",
                    "Hostname Match",
                    "Weak Protocol",
                    "Weak Cipher",
                    "Forward Secrecy",
                    "Wildcard",
                ]
            )

            for result in results:

                writer.writerow(
                    [
                        result.get("host", ""),
                        result.get("risk_level", ""),
                        result.get("risk_score", 0),
                        result.get("days_remaining", 0),
                        result.get("expired", False),
                        result.get("self_signed", False),
                        result.get("hostname_match", False),
                        result.get("weak_protocol", False),
                        result.get("weak_cipher", False),
                        result.get("forward_secrecy", False),
                        result.get("wildcard", False),
                    ]
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
    Export JSON report.
    """

    return write_json(
        OUTPUT_DIR / "results.json",
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

        lines.append(
            f"Target              : {result.get('host', '-')}"
        )

        lines.append(
            f"Risk Level          : {result.get('risk_level', '-')}"
        )

        lines.append(
            f"Risk Score          : {result.get('risk_score', 0)}"
        )

        lines.append(
            f"Days Remaining      : {result.get('days_remaining', 0)}"
        )

        lines.append(
            f"Expired             : {result.get('expired', False)}"
        )

        lines.append(
            f"Self Signed         : {result.get('self_signed', False)}"
        )

        lines.append(
            f"Hostname Match      : {result.get('hostname_match', False)}"
        )

        lines.append(
            f"Weak Protocol       : {result.get('weak_protocol', False)}"
        )

        lines.append(
            f"Weak Cipher         : {result.get('weak_cipher', False)}"
        )

        lines.append(
            f"Forward Secrecy     : {result.get('forward_secrecy', False)}"
        )

        lines.append(
            f"Wildcard            : {result.get('wildcard', False)}"
        )

        lines.append("Recommendations")

        recommendations = result.get(
            "recommendations",
            [],
        )

        if recommendations:

            for recommendation in recommendations:

                lines.append(
                    f"  - {recommendation}"
                )

        else:

            lines.append(
                "  None"
            )

        lines.append("")

    return write_text(
        OUTPUT_DIR / "results.txt",
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
        OUTPUT_DIR / "results.csv",
        analysis["results"],
    )


# ==========================================================
# Export High Risk
# ==========================================================

def export_high_risk(
    analysis: dict[str, Any],
) -> Path:
    """
    Export High/Critical targets.
    """

    results = analysis["results"]

    lines: list[str] = []

    for result in results:

        if result.get(
            "risk_level",
            "",
        ) not in (
            "High",
            "Critical",
        ):
            continue

        lines.append(

            f"{result.get('host', '-')}"
            f" -> "
            f"{result.get('risk_level', '-')}"
            f" "
            f"(Score: {result.get('risk_score', 0)})"

        )

    return write_text(
        OUTPUT_DIR / "high_risk.txt",
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

        "TLS Analysis Summary",

        "=" * 40,

        f"Targets             : {statistics['targets']}",

        f"Average Risk        : {statistics['average_risk']}",

        f"Highest Risk        : {statistics['highest_risk']}",

        f"Expired             : {statistics['expired']}",

        f"Self Signed         : {statistics['self_signed']}",

        f"Hostname Mismatch   : {statistics['hostname_mismatch']}",

        f"Weak Protocol       : {statistics['weak_protocol']}",

        f"Weak Cipher         : {statistics['weak_cipher']}",

        f"Wildcard            : {statistics['wildcard']}",

        f"Forward Secrecy     : {statistics['forward_secrecy']}",

        "",

        "Risk Levels",

        "-" * 40,

    ]

    for level, count in statistics["risk_levels"].items():

        lines.append(
            f"{level:<20}{count}"
        )

    return write_text(
        OUTPUT_DIR / "summary.txt",
        lines,
    )


# ==========================================================
# Show Summary
# ==========================================================

def show_summary(
    analysis: dict[str, Any],
) -> None:
    """
    Display TLS summary.
    """

    statistics = analysis["statistics"]

    print()

    print("=" * 80)

    print(
        "TLS Analysis Summary".center(80)
    )

    print("=" * 80)

    print(f"Targets             : {statistics['targets']}")
    print(f"Average Risk        : {statistics['average_risk']}")
    print(f"Highest Risk        : {statistics['highest_risk']}")
    print(f"Expired             : {statistics['expired']}")
    print(f"Self Signed         : {statistics['self_signed']}")
    print(f"Hostname Mismatch   : {statistics['hostname_mismatch']}")
    print(f"Weak Protocol       : {statistics['weak_protocol']}")
    print(f"Weak Cipher         : {statistics['weak_cipher']}")
    print(f"Wildcard            : {statistics['wildcard']}")
    print(f"Forward Secrecy     : {statistics['forward_secrecy']}")

    print("-" * 80)

    print("Risk Levels")

    print("-" * 80)

    for level, count in statistics["risk_levels"].items():

        print(
            f"{level:<30}{count}"
        )

    print("=" * 80)


# ==========================================================
# Export All
# ==========================================================

def export_all(
    analysis: dict[str, Any],
) -> None:
    """
    Export all TLS reports.
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