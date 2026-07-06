"""
DNS Resolution Manager

Coordinates parallel DNS resolution for all discovered
subdomains.
"""

import json
import time
from pathlib import Path
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from config.config import MAX_WORKERS

from core.logger import (
    info,
    warning,
    success,
    progress,
    section,
)

from modules.dns.records import (
    resolve_all_records,
)


# ==========================================================
# Resolve One Subdomain
# ==========================================================

def resolve_subdomain(
    subdomain: str,
):
    """
    Resolve every supported DNS record for one subdomain.

    Returns:
        tuple[str, dict]
    """

    records = resolve_all_records(
        subdomain
    )

    return (
        subdomain,
        records,
    )


# ==========================================================
# Resolve All Subdomains
# ==========================================================

def resolve_subdomains(
    subdomains: list[str],
):
    """
    Resolve DNS records for every subdomain
    using ThreadPoolExecutor.

    Returns:
        tuple
        (
            results,
            failed,
            elapsed
        )
    """

    info(
        "Starting DNS Resolution..."
    )

    results = {}

    failed = []

    total = len(subdomains)

    completed = 0

    start_time = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {

            executor.submit(
                resolve_subdomain,
                subdomain,
            ): subdomain

            for subdomain in subdomains

        }

        for future in as_completed(
            futures
        ):

            subdomain = futures[
                future
            ]

            completed += 1

            try:

                hostname, records = (
                    future.result()
                )

                results[
                    hostname
                ] = records

            except Exception as error:

                warning(
                    f"{subdomain}: {error}"
                )

                failed.append(
                    subdomain
                )

            progress(
                completed,
                total,
                f"✓ {subdomain} resolved"
            )

    elapsed = round(
        time.perf_counter()
        - start_time,
        2,
    )

    success(
        f"Resolved "
        f"{len(results)} hosts."
    )

    return (
        results,
        failed,
        elapsed,
    )


# ==========================================================
# Save DNS Results
# ==========================================================

def save_dns_results(
    results: dict,
    filename: str = "dns_results.txt",
) -> Path:
    """
    Save DNS results in a human-readable format.
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

            records = results[host]

            for record_type, values in records.items():

                file.write(f"\n{record_type}\n")

                if values:

                    for value in values:

                        file.write(
                            f"  - {value}\n"
                        )

                else:

                    file.write(
                        "  No Record\n"
                    )

            file.write("\n")

    success(
        f"DNS results saved to {output_file}"
    )

    return output_file
    

# ==========================================================
# Export JSON
# ==========================================================

def export_dns_json(
    results: dict,
    filename: str = "dns_results.json",
) -> Path:
    """
    Export DNS results as JSON.
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
    Display DNS resolution summary.
    """

    section(
        "DNS Resolution Summary"
    )

    total_hosts = len(results)

    record_counts = {
        "A": 0,
        "AAAA": 0,
        "MX": 0,
        "NS": 0,
        "TXT": 0,
        "SOA": 0,
        "CNAME": 0,
    }

    enabled_hosts = {
        "A": 0,
        "AAAA": 0,
        "MX": 0,
        "NS": 0,
        "TXT": 0,
        "SOA": 0,
        "CNAME": 0,
    }   

    # -----------------------------------------
    # Count DNS Records
    # -----------------------------------------

    for records in results.values():

        for record_type, values in records.items():

            if record_type not in record_counts:
                continue

            record_counts[record_type] += len(values)

            if values:
                enabled_hosts[record_type] += 1

    total_records = sum(
        record_counts.values()
    )


    # -----------------------------------------
    # General Statistics
    # -----------------------------------------

    print(
        f"{'Resolved Hosts':<25}"
        f"{total_hosts}"
    )

    print(
        f"{'Failed Hosts':<25}"
        f"{len(failed)}"
    )

    print("-" * 75)

    # -----------------------------------------
    # DNS Record Counts
    # -----------------------------------------

    print("DNS Record Counts")
    print("-" * 75)

    print(f"{'A Records':<25}{record_counts['A']}")
    print(f"{'AAAA Records':<25}{record_counts['AAAA']}")
    print(f"{'MX Records':<25}{record_counts['MX']}")
    print(f"{'NS Records':<25}{record_counts['NS']}")
    print(f"{'TXT Records':<25}{record_counts['TXT']}")
    print(f"{'SOA Records':<25}{record_counts['SOA']}")
    print(f"{'CNAME Records':<25}{record_counts['CNAME']}")

    print("-" * 75)

    # -----------------------------------------
    # Hosts Containing Records
    # -----------------------------------------

    print("Hosts Containing Records")
    print("-" * 75)

    print(f"{'A Hosts':<25}{enabled_hosts['A']}")
    print(f"{'AAAA Hosts':<25}{enabled_hosts['AAAA']}")
    print(f"{'MX Hosts':<25}{enabled_hosts['MX']}")
    print(f"{'NS Hosts':<25}{enabled_hosts['NS']}")
    print(f"{'TXT Hosts':<25}{enabled_hosts['TXT']}")
    print(f"{'SOA Hosts':<25}{enabled_hosts['SOA']}")
    print(f"{'CNAME Hosts':<25}{enabled_hosts['CNAME']}")

    print("-" * 75)

    # -----------------------------------------
    # Totals
    # -----------------------------------------

    print(
        f"{'Total DNS Records':<25}"
        f"{total_records}"
    )

    print(
        f"{'Total Time':<25}"
        f"{elapsed:.2f} sec"
    )

    print("=" * 75)

    # -----------------------------------------
    # Failed Hosts
    # -----------------------------------------

    if failed:

        print()

        print("Failed Hosts")

        print("-" * 75)

        for host in failed:

            print(f" • {host}")

        print("-" * 75)
