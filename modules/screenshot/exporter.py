"""
Screenshot Exporter

Exports screenshot capture results.
"""

import json
from pathlib import Path

from core.logger import (
    success,
    section,
)


# ==========================================================
# Save Screenshot Results
# ==========================================================

def save_screenshot_results(
    results: dict,
    filename: str = "screenshots.txt",
) -> Path:
    """
    Save screenshot results in a human-readable format.

    Returns:
        Path
    """

    output_dir = Path("output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / filename

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        for host in sorted(results):

            data = results[host]

            file.write("=" * 75 + "\n")
            file.write(f"Host         : {host}\n")
            file.write(f"URL          : {data.get('url', '-')}\n")
            file.write(f"Screenshot   : {data.get('screenshot', '-')}\n")
            file.write(f"Captured     : {data.get('captured', False)}\n")
            file.write(f"Timestamp    : {data.get('timestamp', '-')}\n")
            file.write(
                f"Resolution   : "
                f"{data.get('width', '-')} x "
                f"{data.get('height', '-')}\n"
            )

            if "title" in data:

                file.write(
                    f"Title        : {data['title']}\n"
                )

            if "final_url" in data:

                file.write(
                    f"Final URL    : {data['final_url']}\n"
                )

            if "status" in data:

                file.write(
                    f"HTTP Status  : {data['status']}\n"
                )

            if "response_time" in data:

                file.write(
                    f"Response     : "
                    f"{data['response_time']:.3f} sec\n"
                )

            file.write("\n")

    success(
        f"Screenshot results saved to {output_file}"
    )

    return output_file


# ==========================================================
# Export JSON
# ==========================================================

def export_screenshot_json(
    results: dict,
    filename: str = "screenshots.json",
) -> Path:
    """
    Export screenshot results as JSON.

    Returns:
        Path
    """

    output_dir = Path("output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / filename

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            sort_keys=True,
        )

    success(
        f"JSON exported to {output_file}"
    )

    return output_file


# ==========================================================
# Summary
# ==========================================================

def show_summary(
    results: dict,
    failed: list,
    elapsed: float,
):
    """
    Display screenshot summary.
    """

    section(
        "Screenshot Capture Summary"
    )

    total = len(results) + len(failed)

    success_rate = (
        (len(results) / total) * 100
        if total
        else 0
    )

    print(
        f"{'Hosts Processed':<25}"
        f"{total}"
    )

    print(
        f"{'Screenshots':<25}"
        f"{len(results)}"
    )

    print(
        f"{'Failed':<25}"
        f"{len(failed)}"
    )

    print("-" * 75)

    print(
        f"{'Success Rate':<25}"
        f"{success_rate:.1f}%"
    )

    print(
        f"{'Total Time':<25}"
        f"{elapsed:.2f} sec"
    )

    print("=" * 75)

    if failed:

        print()

        print("Failed Hosts")

        print("-" * 75)

        for host in failed:

            print(
                f" • {host}"
            )

        print("-" * 75)