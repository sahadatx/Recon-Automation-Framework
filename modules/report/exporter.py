from __future__ import annotations

import json
from typing import Any

from core.logger import success

from .constants import REPORT_JSON, REPORT_MD, REPORT_TXT, SUMMARY_TXT
from .helpers import ensure_output_directory
from .statistics import generate_summary


def export_json(
    report: dict[str, Any],
) -> None:


    with REPORT_JSON.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
        )

    success(f"Saved {REPORT_JSON}")


def export_text(
    report: dict[str, Any],
) -> None:


    with REPORT_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            json.dumps(
                report,
                indent=4,
                ensure_ascii=False,
            )
        )

    success(f"Saved {REPORT_TXT}")


def export_markdown(
    report: dict[str, Any],
) -> None:


    lines = [
        "# Recon Automation Framework Report",
        "",
    ]

    for section, data in report.items():

        lines.append(f"## {section.title()}")

        lines.append("")

        lines.append("```json")

        lines.append(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            )
        )

        lines.append("```")

        lines.append("")

    REPORT_MD.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    success(f"Saved {REPORT_MD}")


def export_summary(
    statistics: dict[str, Any],
) -> None:


    SUMMARY_TXT.write_text(
        generate_summary(statistics),
        encoding="utf-8",
    )

    success(f"Saved {SUMMARY_TXT}")


def export_all(
    report: dict[str, Any],
    statistics: dict[str, Any],
) -> None:


    ensure_output_directory()

    export_json(
        report,
    )

    export_text(
        report,
    )

    export_markdown(
        report,
    )

    export_summary(
        statistics,
    )


def show_summary(
    statistics: dict[str, Any],
) -> None:


    print()

    print("=" * 80)

    print("Report Summary")

    print("=" * 80)

    for key, value in statistics.items():

        print(f"{key.replace('_', ' ').title():<30} {value}")

    print("=" * 80)


__all__ = [
    "export_json",
    "export_text",
    "export_markdown",
    "export_summary",
    "export_all",
    "show_summary",
]
