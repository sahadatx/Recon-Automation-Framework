"""
Crawler Exporter

Export crawler results.
"""

from __future__ import annotations

import csv
import json

from modules.crawler.constants import (
    CRAWLER_OUTPUT_DIR,
    RESULTS_CSV,
    RESULTS_JSON,
    RESULTS_TXT,
    SUMMARY_TXT,
)


# ==========================================================
# Create Output Directory
# ==========================================================

def create_output_directory() -> None:
    """
    Create the crawler output directory.
    """

    CRAWLER_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# Export Results (TXT)
# ==========================================================

def export_results_txt(
    analysis: dict,
) -> None:
    """
    Export crawler results as text.
    """

    with RESULTS_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        for (
            host,
            result,
        ) in sorted(
            analysis["results"].items()
        ):

            file.write(
                "=" * 70 + "\n"
            )

            file.write(
                f"{host}\n"
            )

            file.write(
                "=" * 70 + "\n"
            )

            for url in sorted(
                result["pages"]
            ):

                file.write(
                    f"{url}\n"
                )

            file.write("\n")


# ==========================================================
# Export Results (JSON)
# ==========================================================

def export_results_json(
    analysis: dict,
) -> None:
    """
    Export crawler results as JSON.
    """

    data = json.loads(
        json.dumps(
            analysis,
            default=list,
        )
    )

    with RESULTS_JSON.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            sort_keys=True,
        )


# ==========================================================
# Export Results (CSV)
# ==========================================================

def export_results_csv(
    analysis: dict,
) -> None:
    """
    Export crawler results as CSV.
    """

    with RESULTS_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(
            file,
        )

        writer.writerow(
            [
                "Host",
                "URL",
                "Status",
                "Content Type",
                "Content Length",
            ]
        )

        for (
            host,
            result,
        ) in sorted(
            analysis["results"].items()
        ):

            for (
                url,
                page,
            ) in sorted(
                result["pages"].items()
            ):

                writer.writerow(
                    [
                        host,
                        url,
                        page["status"],
                        page["content_type"],
                        page["content_length"],
                    ]
                )


# ==========================================================
# Export Summary
# ==========================================================

def export_summary(
    analysis: dict,
) -> None:
    """
    Export crawler summary.
    """

    statistics = analysis[
        "statistics"
    ]

    with SUMMARY_TXT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "Crawler Summary\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )

        file.write(
            f"Hosts             : {statistics['hosts']}\n"
        )

        file.write(
            f"Total URLs        : {statistics['total_urls']}\n"
        )

        file.write(
            f"Average URLs/Host : {statistics['average_urls_per_host']}\n"
        )

        file.write(
            f"Failed Pages      : {statistics['failed']}\n"
        )

        file.write(
            f"Internal URLs     : {statistics['internal_urls']}\n"
        )

        file.write(
            f"External URLs     : {statistics['external_urls']}\n"
        )

        file.write(
            f"JavaScript Files  : {statistics['javascript']}\n"
        )

        file.write(
            f"CSS Files         : {statistics['css']}\n"
        )

        file.write(
            f"Forms             : {statistics['forms']}\n"
        )

        file.write(
            f"Emails            : {statistics['emails']}\n"
        )

        file.write(
            f"Scan Time         : {analysis['scan_time']} sec\n\n"
        )

        file.write(
            "URLs Per Host\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for (
            host,
            count,
        ) in statistics[
            "urls_per_host"
        ].items():

            file.write(
                f"{host:<40}{count}\n"
            )


# ==========================================================
# Export All
# ==========================================================

def export_all(
    analysis: dict,
) -> None:
    """
    Export all crawler output files.
    """

    create_output_directory()

    export_results_txt(
        analysis,
    )

    export_results_json(
        analysis,
    )

    export_results_csv(
        analysis,
    )

    export_summary(
        analysis,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "create_output_directory",
    "export_results_txt",
    "export_results_json",
    "export_results_csv",
    "export_summary",
    "export_all",
]