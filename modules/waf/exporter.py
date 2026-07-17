"""
WAF Exporter

Export WAF detection results.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIR = Path("output/waf")

OUTPUT_DIR.mkdir(

    parents=True,

    exist_ok=True,

)

TXT_FILE = OUTPUT_DIR / "results.txt"
JSON_FILE = OUTPUT_DIR / "results.json"
CSV_FILE = OUTPUT_DIR / "results.csv"
SUMMARY_FILE = OUTPUT_DIR / "summary.txt"
DETECTED_FILE = OUTPUT_DIR / "detected.txt"


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

        lines.append(f"Target      : {result['url']}")
        lines.append(f"Detected    : {result['detected']}")
        lines.append(f"Vendor      : {result['vendor']}")
        lines.append(f"Confidence  : {result['confidence']}")
        lines.append(f"Score       : {result['score']}")
        lines.append("Evidence")

        for item in result.get(

            "evidence",

            [],

        ):

            lines.append(

                f"  - {item}"

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

                "Detected",

                "Vendor",

                "Confidence",

                "Score",

            ]

        )

        for result in results:

            writer.writerow(

                [

                    result["url"],

                    result["detected"],

                    result["vendor"],

                    result["confidence"],

                    result["score"],

                ]

            )


# ==========================================================
# Summary Export
# ==========================================================

def export_summary(
    results,
):
    """
    Export summary report.
    """

    total = len(

        results

    )

    detected = sum(

        result.get(

            "detected",

            False,

        )

        for result

        in results

    )

    content = [

        "WAF Detection Summary",

        "=" * 40,

        f"Targets      : {total}",

        f"Detected     : {detected}",

        f"Undetected   : {total - detected}",

    ]

    write_text(

        SUMMARY_FILE,

        "\n".join(content),

    )


# ==========================================================
# Detected Export
# ==========================================================

def export_detected(
    results,
):
    """
    Export detected targets only.
    """

    detected = [

        result

        for result

        in results

        if result.get(

            "detected",

            False,

        )

    ]

    lines = []

    for result in detected:

        lines.append(

            f"{result['url']} -> {result['vendor']} ({result['confidence']})"

        )

    write_text(

        DETECTED_FILE,

        "\n".join(lines),

    )


# ==========================================================
# Export All
# ==========================================================

def export_results(
    results,
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

        results

    )

    export_detected(

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

        f"[SUCCESS] Saved {DETECTED_FILE}"

    )