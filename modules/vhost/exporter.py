"""
Virtual Host Discovery Exporter

Export Virtual Host Discovery
results into multiple formats.
"""

import json

from pathlib import Path

from config.config import (

    VHOST_OUTPUT_DIR,

)

from core.logger import (

    success,

)


# ==========================================================
# Create Output Directory
# ==========================================================

def create_output_directory() -> Path:
    """
    Create output directory.

    Returns:
        Path
    """

    VHOST_OUTPUT_DIR.mkdir(

        parents=True,

        exist_ok=True,

    )

    return VHOST_OUTPUT_DIR


# ==========================================================
# Export JSON
# ==========================================================

def export_json(
    results: list,
) -> Path:
    """
    Export JSON results.

    Returns:
        Path
    """

    output = create_output_directory()

    file = output / "results.json"

    with file.open(

        "w",

        encoding="utf-8",

    ) as handle:

        json.dump(

            results,

            handle,

            indent=4,

        )

    return file


# ==========================================================
# Export TXT
# ==========================================================

def export_txt(
    results: list,
) -> Path:
    """
    Export TXT results.

    Returns:
        Path
    """

    output = create_output_directory()

    file = output / "results.txt"

    with file.open(

        "w",

        encoding="utf-8",

    ) as handle:

        for result in results:

            handle.write(

                f"{result['host']}"

                f"\t"

                f"{result['status']}"

                f"\t"

                f"{result['url']}"

                "\n"

            )

    return file


# ==========================================================
# Export Interesting Hosts
# ==========================================================

def export_interesting(
    interesting: list,
) -> Path:
    """
    Export interesting hosts.

    Returns:
        Path
    """

    output = create_output_directory()

    file = output / "interesting.txt"

    with file.open(

        "w",

        encoding="utf-8",

    ) as handle:

        for result in interesting:

            handle.write(

                f"{result['host']}"

                f"\t"

                f"{result['status']}"

                f"\t"

                f"{result['url']}"

                "\n"

            )

    return file


# ==========================================================
# Export Summary
# ==========================================================

def export_summary(
    statistics: dict,
) -> Path:
    """
    Export summary.

    Returns:
        Path
    """

    output = create_output_directory()

    file = output / "summary.txt"

    with file.open(

        "w",

        encoding="utf-8",

    ) as handle:

        handle.write(

            "Virtual Host Discovery Summary\n"

        )

        handle.write(

            "=" * 40

            + "\n\n"

        )

        handle.write(

            f"Discovered Hosts       : "

            f"{statistics['total_results']}\n"

        )

        handle.write(

            f"Interesting Hosts      : "

            f"{statistics['interesting_hosts']}\n\n"

        )

        handle.write(

            f"HTTP 200               : "

            f"{statistics['status_200']}\n"

        )

        handle.write(

            f"HTTP 204               : "

            f"{statistics['status_204']}\n"

        )

        handle.write(

            f"HTTP 301               : "

            f"{statistics['status_301']}\n"

        )

        handle.write(

            f"HTTP 302               : "

            f"{statistics['status_302']}\n"

        )

        handle.write(

            f"HTTP 307               : "

            f"{statistics['status_307']}\n"

        )

        handle.write(

            f"HTTP 401               : "

            f"{statistics['status_401']}\n"

        )

        handle.write(

            f"HTTP 403               : "

            f"{statistics['status_403']}\n"

        )

    return file


# ==========================================================
# Export All
# ==========================================================

def export(
    results: list,
    interesting: list,
    statistics: dict,
) -> dict:
    """
    Export all reports.

    Returns:
        dict
    """

    files = {

        "json": export_json(

            results

        ),

        "txt": export_txt(

            results

        ),

        "interesting": export_interesting(

            interesting

        ),

        "summary": export_summary(

            statistics

        ),

    }

    success(

        "Virtual Host Discovery "

        "results exported."

    )

    return files