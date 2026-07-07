"""
Crawler Exporter

Export URL discovery results.
"""

import csv
import json
from pathlib import Path

from core.logger import (
    info,
    success,
)


# ==========================================================
# Create Output Directory
# ==========================================================

def create_output_dir(
    output_dir: str,
):
    """
    Create output directory.

    Returns:
        Path
    """

    path = Path(
        output_dir
    )

    path.mkdir(

        parents=True,

        exist_ok=True,

    )

    return path


# ==========================================================
# Export TXT
# ==========================================================

def export_txt(
    results: dict,
    output_dir: str = "output",
):
    """
    Export discovered URLs
    into TXT file.

    Returns:
        str
    """

    output = create_output_dir(
        output_dir
    )

    file_path = output / "urls.txt"

    with open(

        file_path,

        "w",

        encoding="utf-8",

    ) as file:

        for host in results.values():

            for url in host.get(
                "pages",
                {},
            ):

                file.write(
                    f"{url}\n"
                )

    success(
        f"TXT Export: {file_path}"
    )

    return str(
        file_path
    )


# ==========================================================
# Export JSON
# ==========================================================

def export_json(
    results: dict,
    output_dir: str = "output",
):
    """
    Export full crawl
    results into JSON.

    Returns:
        str
    """

    output = create_output_dir(
        output_dir
    )

    file_path = output / "results.json"

    with open(

        file_path,

        "w",

        encoding="utf-8",

    ) as file:

        json.dump(

            results,

            file,

            indent=4,

            ensure_ascii=False,

        )

    success(
        f"JSON Export: {file_path}"
    )

    return str(
        file_path
    )


# ==========================================================
# Export CSV
# ==========================================================

def export_csv(
    results: dict,
    output_dir: str = "output",
):
    """
    Export discovered URLs
    into CSV.

    Returns:
        str
    """

    output = create_output_dir(
        output_dir
    )

    file_path = output / "urls.csv"

    with open(

        file_path,

        "w",

        newline="",

        encoding="utf-8",

    ) as csvfile:

        writer = csv.writer(
            csvfile
        )

        writer.writerow(

            [

                "Host",

                "URL",

                "Status",

                "Content-Type",

                "Content-Length",

            ]

        )

        for host, data in results.items():

            for url, page in data.get(
                "pages",
                {},
            ).items():

                writer.writerow(

                    [

                        host,

                        url,

                        page.get(
                            "status",
                            "",
                        ),

                        page.get(
                            "content_type",
                            "",
                        ),

                        page.get(
                            "content_length",
                            "",
                        ),

                    ]

                )

    success(
        f"CSV Export: {file_path}"
    )

    return str(
        file_path
    )


# ==========================================================
# Show Summary
# ==========================================================

def show_summary(
    summary: dict,
):
    """
    Print crawl summary.
    """

    info(
        "-" * 60
    )

    info(
        "URL Discovery Summary"
    )

    info(
        "-" * 60
    )

    info(
        f"Hosts          : {summary.get('hosts', 0)}"
    )

    info(
        f"Success        : {summary.get('success', 0)}"
    )

    info(
        f"Failed         : {summary.get('failed', 0)}"
    )

    info(
        f"Pages          : {summary.get('pages', 0)}"
    )

    info(
        f"Elapsed        : {summary.get('elapsed', 0)} sec"
    )

    info(
        "-" * 60
    )


# ==========================================================
# Export All
# ==========================================================

def export_all(
    crawl_result: dict,
    output_dir: str = "output",
):
    """
    Export all results.

    Returns:
        dict
    """

    results = crawl_result.get(
        "results",
        {},
    )

    summary = crawl_result.get(
        "summary",
        {},
    )

    txt_file = export_txt(

        results,

        output_dir,

    )

    json_file = export_json(

        results,

        output_dir,

    )

    csv_file = export_csv(

        results,

        output_dir,

    )

    show_summary(
        summary
    )

    return {

        "txt": txt_file,

        "json": json_file,

        "csv": csv_file,

    }
