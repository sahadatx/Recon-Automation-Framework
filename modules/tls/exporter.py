"""
TLS Exporter

Export TLS analysis results.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIR = Path(

    "output/tls"

)

OUTPUT_DIR.mkdir(

    parents=True,

    exist_ok=True,

)

TXT_FILE = OUTPUT_DIR / "results.txt"

JSON_FILE = OUTPUT_DIR / "results.json"

CSV_FILE = OUTPUT_DIR / "results.csv"

SUMMARY_FILE = OUTPUT_DIR / "summary.txt"

HIGH_RISK_FILE = OUTPUT_DIR / "high_risk.txt"


# ==========================================================
# Write Text
# ==========================================================

def write_text(
    path: Path,
    content: str,
):
    """
    Write text file.
    """

    path.write_text(

        content,

        encoding="utf-8",

    )


# ==========================================================
# TXT Export
# ==========================================================

def export_txt(
    results,
):
    """
    Export TXT report.
    """

    lines = []

    for result in results:

        lines.append("=" * 80)

        lines.append(

            f"Target              : {result['host']}"

        )

        lines.append(

            f"Risk Level          : {result['risk_level']}"

        )

        lines.append(

            f"Risk Score          : {result['risk_score']}"

        )

        lines.append(

            f"Days Remaining      : {result['days_remaining']}"

        )

        lines.append(

            f"Expired             : {result['expired']}"

        )

        lines.append(

            f"Self Signed         : {result['self_signed']}"

        )

        lines.append(

            f"Hostname Match      : {result['hostname_match']}"

        )

        lines.append(

            f"Weak Protocol       : {result['weak_protocol']}"

        )

        lines.append(

            f"Weak Cipher         : {result['weak_cipher']}"

        )

        lines.append(

            f"Forward Secrecy     : {result['forward_secrecy']}"

        )

        lines.append(

            f"Wildcard            : {result['wildcard']}"

        )

        lines.append(

            "Recommendations"

        )

        recommendations = result.get(

            "recommendations",

            [],

        )

        if recommendations:

            for item in recommendations:

                lines.append(

                    f"  - {item}"

                )

        else:

            lines.append(

                "  None"

            )

        lines.append("")

    write_text(

        TXT_FILE,

        "\n".join(lines),

    )

# ==========================================================
# JSON Export
# ==========================================================

def export_json(
    results,
):
    """
    Export JSON report.
    """

    with JSON_FILE.open(

        "w",

        encoding="utf-8",

    ) as fp:

        json.dump(

            results,

            fp,

            indent=4,

            ensure_ascii=False,

        )


# ==========================================================
# CSV Export
# ==========================================================

def export_csv(
    results,
):
    """
    Export CSV report.
    """

    with CSV_FILE.open(

        "w",

        newline="",

        encoding="utf-8",

    ) as fp:

        writer = csv.writer(

            fp

        )

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

                    result["host"],

                    result["risk_level"],

                    result["risk_score"],

                    result["days_remaining"],

                    result["expired"],

                    result["self_signed"],

                    result["hostname_match"],

                    result["weak_protocol"],

                    result["weak_cipher"],

                    result["forward_secrecy"],

                    result["wildcard"],

                ]

            )


# ==========================================================
# Summary Export
# ==========================================================

def export_summary(
    statistics,
):
    """
    Export summary report.
    """

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

        f"Elapsed Time        : {statistics['elapsed']} sec",

        "",

        "Risk Levels",

        "-" * 40,

    ]

    for level, count in statistics[

        "risk_levels"

    ].items():

        lines.append(

            f"{level:<20}{count}"

        )

    write_text(

        SUMMARY_FILE,

        "\n".join(lines),

    )


# ==========================================================
# High Risk Export
# ==========================================================

def export_high_risk(
    results,
):
    """
    Export High/Critical targets.
    """

    targets = [

        result

        for result

        in results

        if result.get(

            "risk_level"

        )

        in (

            "High",

            "Critical",

        )

    ]

    lines = []

    for result in targets:

        lines.append(

            f"{result['host']} -> "

            f"{result['risk_level']} "

            f"(Score: {result['risk_score']})"

        )

    write_text(

        HIGH_RISK_FILE,

        "\n".join(lines),

    )


# ==========================================================
# Export All
# ==========================================================

def export_results(
    results,
    statistics,
):
    """
    Export all reports.
    """

    export_txt(

        results

    )

    export_json(

        results

    )

    export_csv(

        results

    )

    export_summary(

        statistics

    )

    export_high_risk(

        results

    )

    print(

        f"[SUCCESS] Saved {TXT_FILE}"

    )

    print(

        f"[SUCCESS] Saved {JSON_FILE}"

    )

    print(

        f"[SUCCESS] Saved {CSV_FILE}"

    )

    print(

        f"[SUCCESS] Saved {SUMMARY_FILE}"

    )

    print(

        f"[SUCCESS] Saved {HIGH_RISK_FILE}"

    )


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "export_txt",

    "export_json",

    "export_csv",

    "export_summary",

    "export_high_risk",

    "export_results",

]
