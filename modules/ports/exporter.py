"""
Port Scanner Exporter

Exports scan results and displays summaries.
"""

import csv
import json
from pathlib import Path

from core.logger import (
    success,
    section,
)


# ==========================================================
# Save Open Hosts
# ==========================================================

def save_open_ports(
    results: dict,
    filename: str = "open_ports.txt",
):
    """
    Save only hosts that have open ports.
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

            file.write(f"{host}\n")

    success(
        f"Open hosts saved to {output_file}"
    )

    return output_file


# ==========================================================
# Save Port Results
# ==========================================================

def save_port_results(
    results: dict,
    filename: str = "port_results.txt",
):
    """
    Save detailed scan results.
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

            file.write("=" * 70 + "\n")
            file.write(f"{host}\n")
            file.write("=" * 70 + "\n")

            for port in results[host]:

                file.write(
                    f"{port['port']:>5}/tcp   "
                    f"{port['state']:<6}   "
                    f"{port['service']}\n"
                )

            file.write("\n")

    success(
        f"Port results saved to {output_file}"
    )

    return output_file


# ==========================================================
# Export JSON
# ==========================================================

def export_port_json(
    results: dict,
    filename: str = "port_results.json",
):
    """
    Export JSON results.
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
# Export CSV
# ==========================================================

def export_open_ports_csv(
    results: dict,
    filename: str = "open_ports.csv",
):
    """
    Export open ports to CSV.
    """

    output_dir = Path("output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / filename

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(

            [
                "Host",
                "Port",
                "Service",
                "State",
            ]

        )

        for host in sorted(results):

            for port in results[host]:

                writer.writerow(

                    [
                        host,
                        port["port"],
                        port["service"],
                        port["state"],
                    ]

                )

    success(
        f"CSV exported to {output_file}"
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
    Display scan summary.
    """

    section(
        "Port Scan Summary"
    )

    open_ports = 0

    services = {}

    for ports in results.values():

        open_ports += len(
            ports
        )

        for port in ports:

            service = port[
                "service"
            ]

            services[
                service
            ] = services.get(
                service,
                0,
            ) + 1

    print(
        f"{'Hosts Scanned':<25}"
        f"{len(results)+len(failed)}"
    )

    print(
        f"{'Hosts With Open':<25}"
        f"{len(results)}"
    )

    print(
        f"{'Hosts Without Open':<25}"
        f"{len(failed)}"
    )

    print("-" * 75)

    print(
        f"{'Open Ports':<25}"
        f"{open_ports}"
    )

    print("-" * 75)

    print(
        "Service Breakdown"
    )

    print("-" * 75)

    for service in sorted(
        services
    ):

        print(
            f"{service:<25}"
            f"{services[service]}"
        )

    print("-" * 75)

    average = (
        open_ports /
        len(results)
        if results
        else 0
    )

    print(
        f"{'Average Open':<25}"
        f"{average:.2f}"
    )

    print(
        f"{'Total Time':<25}"
        f"{elapsed:.2f} sec"
    )

    print("=" * 75)

    if failed:

        print()

        print(
            "Hosts Without Open Ports"
        )

        print("-" * 75)

        for host in failed:

            print(
                f" • {host}"
            )

        print("-" * 75)