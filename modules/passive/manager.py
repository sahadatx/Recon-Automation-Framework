"""
Passive Enumeration Manager

Coordinates all passive enumeration sources.
"""

import re
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from config.config import MAX_WORKERS

from core.logger import (
    info,
    warning,
    success,
)

from modules.passive.subfinder import run_subfinder
from modules.passive.assetfinder import run_assetfinder
from modules.passive.crtsh import run_crtsh
from modules.passive.chaos import run_chaos
from modules.passive.findomain import run_findomain
from modules.passive.securitytrails import run_securitytrails


# ==========================================================
# Tool Registry
# ==========================================================

PASSIVE_SOURCES = [
    ("Subfinder", run_subfinder),
    ("Assetfinder", run_assetfinder),
    ("crt.sh", run_crtsh),
    ("Chaos", run_chaos),
    ("Findomain", run_findomain),
    ("SecurityTrails", run_securitytrails),
]

RETRYABLE_TOOLS = {
    "crt.sh",
}


# ==========================================================
# Timed Runner
# ==========================================================

def timed_runner(function, domain):
    """
    Execute a passive source and measure execution time.
    """

    start = time.perf_counter()

    result = function(domain)

    elapsed = round(
        time.perf_counter() - start,
        2,
    )

    return result, elapsed


# ==========================================================
# Collect Passive Enumeration
# ==========================================================

def collect_subdomains(domain: str):
    """
    Execute every passive enumeration source in parallel.
    """

    info("Starting Passive Enumeration...")

    results = {}
    timings = {}
    failed = []
    retry_queue = []

    completed = 0
    total_sources = len(PASSIVE_SOURCES)

    start_time = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = {}

        # --------------------------------------------------
        # Submit Jobs
        # --------------------------------------------------

        for name, function in PASSIVE_SOURCES:

            future = executor.submit(
                timed_runner,
                function,
                domain,
            )

            futures[future] = (
                name,
                function,
            )

        # --------------------------------------------------
        # Collect Results
        # --------------------------------------------------

        for future in as_completed(futures):

            name, function = futures[future]

            completed += 1

            try:

                output, elapsed = future.result()

            except Exception as error:

                warning(
                    f"{name} crashed: {error}"
                )

                output = []
                elapsed = 0.0

                failed.append(name)

            info(
                f"[{completed}/{total_sources}] {name} completed."
            )

            results[name] = output
            timings[name] = elapsed

            if (
                not output
                and name in RETRYABLE_TOOLS
            ):

                retry_queue.append(
                    (
                        name,
                        function,
                    )
                )

    # --------------------------------------------------
    # Retry Queue
    # --------------------------------------------------

    if retry_queue:

        info("Retrying failed sources...")

        for name, function in retry_queue:

            try:

                retry_results = function(domain)

                if retry_results:

                    results[name] = retry_results

                    if name in failed:

                        failed.remove(name)

            except Exception as error:

                warning(
                    f"{name} retry failed: {error}"
                )

    total_time = round(
        time.perf_counter() - start_time,
        2,
    )

    return (
        results,
        timings,
        failed,
        total_time,
    )


# ==========================================================
# Merge Results
# ==========================================================

DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
)


def merge_results(
    results: dict,
    domain: str,
) -> list[str]:
    """
    Merge, validate and normalize subdomains.
    """

    unique = set()

    suffix = "." + domain.lower()

    for subdomains in results.values():

        for subdomain in subdomains:

            if not subdomain:
                continue

            subdomain = subdomain.strip().lower()

            # Remove trailing dot
            subdomain = subdomain.rstrip(".")

            # Keep only target domain
            if (
                subdomain != domain.lower()
                and not subdomain.endswith(suffix)
            ):
                continue

            # Validate hostname
            if not DOMAIN_RE.fullmatch(
                subdomain
            ):
                continue

            unique.add(
                subdomain
            )

    return sorted(
        unique
    )


# ==========================================================
# Save Results
# ==========================================================

def save_results(
    subdomains: list[str],
    filename: str = "subdomains.txt",
) -> Path:
    """
    Save subdomains to output directory.

    Args:
        subdomains: List of discovered subdomains.
        filename: Output filename.

    Returns:
        Output file path.
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

        for subdomain in subdomains:

            file.write(
                subdomain + "\n"
            )

    success(
        f"Saved {len(subdomains)} unique subdomains."
    )

    info(
        f"Output File : {output_file}"
    )

    return output_file


# ==========================================================
# Export Results (Future Use)
# ==========================================================

def export_results(
    results: dict,
    filename: str = "raw_results.txt",
) -> Path:
    """
    Export raw results grouped by source.

    Useful for debugging and future reporting.
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

        for source, subdomains in results.items():

            file.write("=" * 60 + "\n")
            file.write(f"{source}\n")
            file.write("=" * 60 + "\n")

            for subdomain in subdomains:

                file.write(
                    subdomain + "\n"
                )

            file.write("\n")

    success(
        f"Raw results exported to {output_file}"
    )

    return output_file


# ==========================================================
# Summary
# ==========================================================

def show_summary(
    results: dict,
    timings: dict,
    failed: list,
    unique: list[str],
    total_time: float,
) -> None:
    """
    Display passive enumeration summary.
    """

    print()

    print("=" * 78)
    print(" Passive Enumeration Summary ".center(78))
    print("=" * 78)

    print(
        f"{'Source':<20}"
        f"{'Subdomains':>12}"
        f"{'Time':>12}"
        f"{'Status':>15}"
    )

    print("-" * 78)

    success_count = 0

    for source, _ in PASSIVE_SOURCES:

        count = len(results.get(source, []))

        elapsed = timings.get(source, 0.0)

        if source in failed:

            status = "FAILED"

        elif count == 0:

            status = "EMPTY"

        else:

            status = "SUCCESS"

            success_count += 1

        print(
            f"{source:<20}"
            f"{count:>12}"
            f"{elapsed:>10.2f}s"
            f"{status:>15}"
        )

    print("-" * 78)

    print(
        f"{'Unique Subdomains':<20}"
        f"{len(unique):>12}"
    )

    success_ratio = f"{success_count}/{len(PASSIVE_SOURCES)}"

    print(
        f"{'Successful Tools':<20}"
        f"{success_ratio:>12}"
    )

    print(
        f"{'Failed Tools':<20}"
        f"{len(failed):>12}"
    )

    print(
        f"{'Total Scan Time':<20}"
        f"{total_time:>10.2f}s"
    )

    print("=" * 78)

    # ------------------------------------------------------
    # Failed Sources
    # ------------------------------------------------------

    if failed:

        print()
        print("Failed Sources")
        print("-" * 78)

        for source in failed:

            print(f" • {source}")

        print("-" * 78)