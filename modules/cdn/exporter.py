from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from core.logger import success, warning

from .constants import (
    CSV_FILE,
    DETECTED_FILE,
    JSON_FILE,
    OUTPUT_DIR,
    SUMMARY_FILE,
    TXT_FILE,
)


def create_output_directory() -> None:


    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def write_text(
    output_file: Path,
    lines: list[str],
) -> Path:


    try:

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        success(f"Saved {output_file}")

    except OSError as error:

        warning(f"{output_file}: {error}")

    return output_file


def write_json(
    output_file: Path,
    data: Any,
) -> Path:


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


def write_csv(
    output_file: Path,
    results: list[dict[str, Any]],
) -> Path:


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
                    "CDN",
                    "Provider",
                    "Confidence",
                    "Methods",
                    "CNAME",
                    "IP",
                ]
            )

            for result in results:

                writer.writerow(
                    [
                        result.get("target", ""),
                        result.get("cdn", False),
                        result.get("provider", ""),
                        result.get("confidence", ""),
                        ", ".join(
                            result.get(
                                "method",
                                [],
                            )
                        ),
                        result.get("cname", ""),
                        result.get("ip", ""),
                    ]
                )

        success(f"Saved {output_file}")

    except OSError as error:

        warning(f"{output_file}: {error}")

    return output_file


def export_json(
    analysis: dict[str, Any],
) -> Path:


    return write_json(
        JSON_FILE,
        analysis,
    )


def export_txt(
    analysis: dict[str, Any],
) -> Path:


    results = analysis["results"]

    lines: list[str] = []

    for result in results:

        lines.append("=" * 80)

        lines.append(f"Target              : {result.get('target', '-')}")

        lines.append(f"CDN Detected        : {result.get('cdn', False)}")

        lines.append(f"Provider            : {result.get('provider', '-')}")

        lines.append(f"Confidence          : {result.get('confidence', '-')}")

        lines.append("Methods             : " + ", ".join(result.get("method", [])))

        lines.append(f"CNAME               : {result.get('cname', '-')}")

        lines.append(f"IP Address          : {result.get('ip', '-')}")

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


def export_csv(
    analysis: dict[str, Any],
) -> Path:


    return write_csv(
        CSV_FILE,
        analysis["results"],
    )


def export_detected(
    analysis: dict[str, Any],
) -> Path:


    results = analysis["results"]

    lines: list[str] = []

    for result in results:

        if not result.get(
            "cdn",
            False,
        ):
            continue

        lines.append(
            f"{result.get('target', '-')}"
            f" -> "
            f"{result.get('provider', '-')}"
            f" (Confidence: {result.get('confidence', '-')})"
        )

    return write_text(
        DETECTED_FILE,
        lines,
    )


def export_summary(
    analysis: dict[str, Any],
) -> Path:


    statistics = analysis["statistics"]

    lines = [
        "CDN Detection Summary",
        "=" * 40,
        f"Targets             : {statistics['targets']}",
        f"CDN Detected        : {statistics['detected']}",
        f"CDN Not Detected    : {statistics['undetected']}",
        f"Average Confidence  : {statistics['average_confidence']}",
        f"Highest Confidence  : {statistics['highest_confidence']}",
        "",
        "Confidence Levels",
        "-" * 40,
    ]

    for level, count in statistics["confidence_statistics"].items():

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


def show_summary(
    analysis: dict[str, Any],
) -> None:


    statistics = analysis["statistics"]

    print()

    print("=" * 80)

    print("CDN Detection Summary".center(80))

    print("=" * 80)

    print(f"Targets             : {statistics['targets']}")
    print(f"CDN Detected        : {statistics['detected']}")
    print(f"CDN Not Detected    : {statistics['undetected']}")
    print(f"Average Confidence  : {statistics['average_confidence']}")
    print(f"Highest Confidence  : {statistics['highest_confidence']}")

    print("-" * 80)

    print("Confidence Levels")

    print("-" * 80)

    for level, count in statistics["confidence_statistics"].items():

        print(f"{level:<30}{count}")

    print("-" * 80)

    print("Providers")

    print("-" * 80)

    for provider, count in statistics["provider_statistics"].items():

        print(f"{provider:<30}{count}")

    print("=" * 80)


def export_all(
    analysis: dict[str, Any],
) -> None:


    create_output_directory()

    export_json(analysis)

    export_txt(analysis)

    export_csv(analysis)

    export_detected(analysis)

    export_summary(analysis)

    show_summary(analysis)


__all__ = [
    "export_all",
]
