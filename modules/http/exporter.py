"""
HTTP Exporter

Export HTTP probe results and display summary.
"""

import json
from pathlib import Path

from core.logger import (
    success,
    section,
)


# ==========================================================
# Save Alive Hosts
# ==========================================================

def save_alive_hosts(
    results: dict,
    filename: str = "alive.txt",
) -> Path:
    """
    Save alive hosts.
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

            file.write(
                host + "\n"
            )

    success(
        f"Alive hosts saved to {output_file}"
    )

    return output_file


# ==========================================================
# Save HTTP Results
# ==========================================================

def save_http_results(
    results: dict,
    filename: str = "http_results.txt",
) -> Path:
    """
    Save HTTP probe results.
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

            file.write("=" * 70 + "\n")
            file.write(host + "\n")
            file.write("=" * 70 + "\n")

            for key, value in data.items():

                file.write(
                    f"{key:<18}: {value}\n"
                )

            file.write("\n")

    success(
        f"HTTP results saved to {output_file}"
    )

    return output_file


# ==========================================================
# Export JSON
# ==========================================================

def export_http_json(
    results: dict,
    filename: str = "http_results.json",
) -> Path:
    """
    Export HTTP results as JSON.
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
    Display HTTP summary.
    """

    section(
        "HTTP Probe Summary"
    )

    alive = len(results)

    dead = len(failed)

    http_hosts = 0

    https_hosts = 0

    status_codes = {}

    total_response = 0.0

    for data in results.values():

        if data["scheme"] == "http":

            http_hosts += 1

        else:

            https_hosts += 1

        status = data["status"]

        status_codes[status] = (
            status_codes.get(status, 0)
            + 1
        )

        total_response += data[
            "response_time"
        ]

    average = 0.0

    if alive:

        average = round(
            total_response / alive,
            3,
        )

    print(
        f"{'Alive Hosts':<25}{alive}"
    )

    print(
        f"{'Dead Hosts':<25}{dead}"
    )

    print("-" * 75)

    print(
        f"{'HTTP':<25}{http_hosts}"
    )

    print(
        f"{'HTTPS':<25}{https_hosts}"
    )

    print("-" * 75)

    for code in sorted(status_codes):

        print(
            f"{str(code):<25}"
            f"{status_codes[code]}"
        )

    print("-" * 75)

    print(
        f"{'Average Response':<25}"
        f"{average} sec"
    )

    print(
        f"{'Total Time':<25}"
        f"{elapsed:.2f} sec"
    )

    print("=" * 75)

    if failed:

        print()

        print("Dead Hosts")

        print("-" * 75)

        for host in failed:

            print(
                f" • {host}"
            )

        print("-" * 75)