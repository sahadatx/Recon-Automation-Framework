"""
Nuclei Manager

Coordinates Nuclei scanning,
parsing, filtering,
statistics and exporting.
"""

import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from config.config import (
    MAX_WORKERS,
)

from core.logger import (
    info,
    success,
    warning,
    progress_status,
)

from modules.nuclei.scanner import (
    scan_target,
    cleanup,
)

from modules.nuclei.parser import (
    parse_nuclei,
)

from modules.nuclei.filters import (
    apply_filters,
)

from modules.nuclei.statistics import (
    generate,
)

from modules.nuclei.exporter import (
    export_all,
)


# ==========================================================
# Process One Target
# ==========================================================

def process_target(
    target: str,
):
    """
    Scan one target.

    Returns:
        tuple(
            target,
            result | None,
        )
    """

    scan = scan_target(
        target
    )

    if not scan["success"]:

        return (
            target,
            None,
        )

    output = scan["output"]

    parsed = parse_nuclei(
        output
    )

    cleanup(
        output
    )

    if parsed is None:

        return (
            target,
            None,
        )

    findings = apply_filters(

        parsed.get(

            "findings",

            [],

        )

    )

    statistics = generate(
        findings
    )

    return (

        target,

        {

            "findings": findings,

            "statistics": statistics,

        },

    )


# ==========================================================
# Collect Findings
# ==========================================================

def collect_findings(
    results: dict,
):
    """
    Collect findings from all
    successful targets.

    Returns:
        list
    """

    findings = []

    for data in results.values():

        if not data:

            continue

        findings.extend(

            data.get(

                "findings",

                [],

            )

        )

    return findings


# ==========================================================
# Build Overall Statistics
# ==========================================================

def build_overall_statistics(
    results: dict,
    failed: list,
    elapsed: float,
):
    """
    Build overall scan
    statistics.

    Returns:
        dict
    """

    findings = collect_findings(
        results
    )

    statistics = generate(
        findings
    )

    statistics.update({

        "targets": len(results) + len(failed),

        "successful": len(
            results
        ),

        "failed": len(
            failed
        ),

        "elapsed": elapsed,

    })

    return statistics


# ==========================================================
# Run Nuclei
# ==========================================================

def run_nuclei(
    targets: list[str],
):
    """
    Run Nuclei against
    multiple targets.

    Returns:
        (
            results,
            overall,
            failed,
            elapsed,
        )
    """

    if not targets:

        warning(
            "No targets supplied."
        )

        return (

            {},

            {},

            [],

            0,

        )

    info(
        "Starting Nuclei Scan..."
    )

    targets = sorted(
        set(targets)
    )

    results: dict[str, dict] = {}

    failed: list[str] = []

    completed = 0

    total = len(
        targets
    )

    start_time = time.perf_counter()

    with ThreadPoolExecutor(

        max_workers=MAX_WORKERS,

    ) as executor:

        futures = {

            executor.submit(

                process_target,

                target,

            ): target

            for target in targets

        }

        for future in as_completed(
            futures
        ):

            target = futures[
                future
            ]

            completed += 1

            try:

                hostname, data = (

                    future.result()

                )

                if data:

                    results[
                        hostname
                    ] = data

                    progress_status(

                        completed,

                        total,

                        f"✓ {hostname}",

                    )

                else:

                    failed.append(
                        hostname
                    )

                    progress_status(

                        completed,

                        total,

                        f"✗ {hostname}",

                    )

            except KeyboardInterrupt:

                warning(
                    "Scan interrupted."
                )

                raise

            except Exception as error:

                warning(

                    f"{target}: {error}"

                )

                failed.append(
                    target
                )

                progress_status(

                    completed,

                    total,

                    f"✗ {target}",

                )

    elapsed = round(

        time.perf_counter()

        - start_time,

        2,

    )

    overall = build_overall_statistics(

        results,

        failed,

        elapsed,

    )

    success(

        f"Targets          : {overall['targets']}"

    )

    success(

        f"Successful       : {overall['successful']}"

    )

    success(

        f"Failed           : {overall['failed']}"

    )

    success(

        f"Findings         : {overall['total_findings']}"

    )

    success(

        f"Elapsed          : {overall['elapsed']:.2f} sec"

    )

    return (

        results,

        overall,

        failed,

        elapsed,

    )


# ==========================================================
# Export Results
# ==========================================================

def export_results(
    results: dict,
    overall: dict,
):
    """
    Export all findings.

    Args:
        results:
            Scan results.

        overall:
            Overall statistics.

    Returns:
        dict
    """

    findings = collect_findings(
        results
    )

    return export_all(

        findings,

        overall,

    )


# ==========================================================
# Run And Export
# ==========================================================

def run_and_export(
    targets: list[str],
):
    """
    Run Nuclei scan and
    export all reports.

    Args:
        targets:
            Target list.

    Returns:
        tuple
    """

    results, overall, failed, elapsed = (

        run_nuclei(
            targets
        )

    )

    files = export_results(

        results,

        overall,

    )

    return (

        results,

        overall,

        failed,

        elapsed,

        files,

    )


# ==========================================================
# Successful Targets
# ==========================================================

def successful_targets(
    results: dict,
):
    """
    Return successful
    targets.

    Returns:
        list
    """

    return sorted(

        results.keys()

    )


# ==========================================================
# Failed Targets
# ==========================================================

def failed_targets(
    failed: list,
):
    """
    Return failed
    targets.

    Returns:
        list
    """

    return sorted(

        failed

    )


# ==========================================================
# Print Summary
# ==========================================================

def print_summary(
    overall: dict,
):
    """
    Display final summary.

    Args:
        overall:
            Overall statistics.
    """

    success(
        "=" * 60
    )

    success(
        "Nuclei Scan Completed"
    )

    success(
        "=" * 60
    )

    success(
        f"Targets            : {overall.get('targets', 0)}"
    )

    success(
        f"Successful         : {overall.get('successful', 0)}"
    )

    success(
        f"Failed             : {overall.get('failed', 0)}"
    )

    success(
        f"Total Findings     : {overall.get('total_findings', 0)}"
    )

    success(
        f"Critical           : {overall.get('critical', 0)}"
    )

    success(
        f"High               : {overall.get('high', 0)}"
    )

    success(
        f"Medium             : {overall.get('medium', 0)}"
    )

    success(
        f"Low                : {overall.get('low', 0)}"
    )

    success(
        f"Info               : {overall.get('info', 0)}"
    )

    success(
        f"Elapsed            : {overall.get('elapsed', 0):.2f} sec"
    )

    success(
        "=" * 60
    )


# ==========================================================
# Self Test
# ==========================================================

if __name__ == "__main__":

    targets = [

        "https://scanme.sh",

    ]

    results, overall, failed, elapsed, files = (

        run_and_export(
            targets
        )

    )

    print_summary(
        overall
    )
