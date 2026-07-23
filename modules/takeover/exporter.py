"""
Takeover Exporter

Export Subdomain
Takeover analysis
results.
"""

from __future__ import annotations

import csv
import json

from .constants import (
    TXT_FILE,
    JSON_FILE,
    CSV_FILE,
    SUMMARY_FILE,
    VULNERABLE_FILE,
)


# ==========================================================
# Write Text
# ==========================================================

def write_text(
    path,
    content: str,
) -> None:
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
) -> None:
    """
    Export TXT report.
    """

    lines = []

    for result in results:

        lines.append("=" * 80)

        lines.append(

            f"Target              : {result['target']}"

        )

        lines.append(

            f"Vulnerable          : {result['vulnerable']}"

        )

        lines.append(

            f"Provider            : {result['provider']}"

        )

        lines.append(

            f"Confidence          : {result['confidence']}"

        )

        lines.append(

            f"Methods             : "

            f"{', '.join(result['methods'])}"

        )

        lines.append(

            f"Status Code         : {result['status_code']}"

        )

        lines.append(

            f"Fingerprint         : {result['fingerprint']}"

        )

        lines.append(

            f"CNAME               : {result['cname']}"

        )

        lines.append(

            f"IP Address          : {result['ip']}"

        )

        lines.append(

            f"HTTP Title          : {result['http_title']}"

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

        "\n".join(

            lines,

        ),

    )


# ==========================================================
# JSON Export
# ==========================================================

def export_json(
    results,
) -> None:
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
) -> None:
    """
    Export CSV report.
    """

    with CSV_FILE.open(

        "w",

        newline="",

        encoding="utf-8",

    ) as fp:

        writer = csv.writer(

            fp,

        )

        writer.writerow(

            [

                "Target",

                "Vulnerable",

                "Provider",

                "Confidence",

                "Methods",

                "Status Code",

                "Fingerprint",

                "CNAME",

                "IP",

                "HTTP Title",

            ]

        )

        for result in results:

            writer.writerow(

                [

                    result["target"],

                    result["vulnerable"],

                    result["provider"],

                    result["confidence"],

                    ", ".join(

                        result["methods"],

                    ),

                    result["status_code"],

                    result["fingerprint"],

                    result["cname"],

                    result["ip"],

                    result["http_title"],

                ]

            )


# ==========================================================
# Summary Export
# ==========================================================

def export_summary(
    statistics,
) -> None:
    """
    Export summary report.
    """

    lines = [

        "Subdomain Takeover Summary",

        "=" * 40,

        f"Targets             : {statistics['targets']}",

        f"Vulnerable          : {statistics['vulnerable']}",

        f"Safe                : {statistics['safe']}",

        f"Average Confidence  : {statistics['average_confidence']}",

        f"Highest Confidence  : {statistics['highest_confidence']}",

        f"Elapsed Time        : {statistics['elapsed']} sec",

        "",

        "Confidence Levels",

        "-" * 40,

    ]

    for level, count in statistics[

        "confidence_statistics"

    ].items():

        lines.append(

            f"{level:<20}{count}"

        )

    lines.extend(

        [

            "",

            "Providers",

            "-" * 40,

        ]

    )

    for provider, count in statistics[

        "provider_statistics"

    ].items():

        lines.append(

            f"{provider:<20}{count}"

        )

    write_text(

        SUMMARY_FILE,

        "\n".join(

            lines,

        ),

    )


# ==========================================================
# Vulnerable Export
# ==========================================================

def export_vulnerable(
    results,
) -> None:
    """
    Export vulnerable
    targets.
    """

    targets = [

        result

        for result

        in results

        if result.get(

            "vulnerable",

            False,

        )

    ]

    lines = []

    for result in targets:

        lines.append(

            f"{result['target']} -> "

            f"{result['provider']} "

            f"(Confidence: "

            f"{result['confidence']})"

        )

    write_text(

        VULNERABLE_FILE,

        "\n".join(

            lines,

        ),

    )


# ==========================================================
# Export All
# ==========================================================

def export_results(
    results,
    statistics,
) -> None:
    """
    Export all reports.
    """

    export_txt(

        results,

    )

    export_json(

        results,

    )

    export_csv(

        results,

    )

    export_summary(

        statistics,

    )

    export_vulnerable(

        results,

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

        f"[SUCCESS] Saved {VULNERABLE_FILE}"

    )


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "export_txt",

    "export_json",

    "export_csv",

    "export_summary",

    "export_vulnerable",

    "export_results",

]


