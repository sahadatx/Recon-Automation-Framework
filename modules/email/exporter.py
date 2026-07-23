"""
Email Security Exporter

Export Email
Security analysis
results.
"""

from __future__ import annotations

import csv
import json

from .constants import (
    CSV_FILE,
    HIGH_RISK_FILE,
    JSON_FILE,
    SUMMARY_FILE,
    TXT_FILE,
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

            f"Provider            : {result['provider']}"

        )

        lines.append(

            f"Risk                : {result['risk']}"

        )

        lines.append(

            f"Score               : {result['score']}"

        )

        lines.append(

            f"MX Records          : "

            f"{', '.join(result['mx'])}"

        )

        lines.append(

            f"SPF                 : {result['spf']}"

        )

        lines.append(

            f"DKIM                : {result['dkim']}"

        )

        lines.append(

            f"DMARC               : {result['dmarc']}"

        )

        lines.append(

            f"MTA-STS             : {result['mta_sts']}"

        )

        lines.append(

            f"TLS-RPT             : {result['tls_rpt']}"

        )

        lines.append(

            f"BIMI                : {result['bimi']}"

        )

        lines.append(

            f"DNSSEC              : {result['dnssec']}"

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

                    result["target"],

                    result["provider"],

                    result["risk"],

                    result["score"],

                    result["spf"],

                    result["dkim"],

                    result["dmarc"],

                    result["mta_sts"],

                    result["tls_rpt"],

                    result["bimi"],

                    result["dnssec"],

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

        f"Elapsed Time       : {statistics['elapsed']} sec",

        "",

        "Risk Levels",

        "-" * 40,

    ]

    for level, count in statistics[

        "risk_statistics"

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
# High Risk Export
# ==========================================================

def export_high_risk(
    results,
) -> None:
    """
    Export high risk
    targets.
    """

    targets = [

        result

        for result

        in results

        if result.get(

            "risk",

        )

        in

        (

            "High",

            "Critical",

        )

    ]

    lines = []

    for result in targets:

        lines.append(

            f"{result['target']} -> "

            f"{result['risk']} "

            f"(Score: "

            f"{result['score']})"

        )

    write_text(

        HIGH_RISK_FILE,

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

    export_high_risk(

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

