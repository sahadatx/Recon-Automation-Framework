"""
WAF Manager

Main entry point for
WAF Detection.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import info

from modules.waf.scanner import scan_targets
from modules.waf.detector import detect_all
from modules.waf.filters import filter_results
from modules.waf.statistics import (
    generate_statistics,
    print_summary,
)
from modules.waf.exporter import export_results


# ==========================================================
# Run WAF Detection
# ==========================================================

def run_waf_detection(
    targets: list[str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Run complete WAF Detection pipeline.

    Pipeline:
        Scan
        -> Detect
        -> Filter
        -> Statistics
        -> Export

    Returns:
        tuple(results, statistics)
    """

    print()
    print("=" * 80)
    print("WAF Detection".center(80))
    print("=" * 80)

    start = perf_counter()

    try:

        # --------------------------------------------------
        # Scan Targets
        # --------------------------------------------------

        info("Scanning targets...")

        scans = scan_targets(
            targets
        )

        # --------------------------------------------------
        # Detect WAF
        # --------------------------------------------------

        info("Matching fingerprints...")

        results = detect_all(
            scans
        )

        # --------------------------------------------------
        # Filter Results
        # --------------------------------------------------

        info("Filtering results...")

        results = filter_results(
            results
        )

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        elapsed = perf_counter() - start

        statistics = generate_statistics(
            results,
            elapsed,
        )

        # --------------------------------------------------
        # Export Results
        # --------------------------------------------------

        info("Exporting results...")

        export_results(
            results
        )

        # --------------------------------------------------
        # Print Summary
        # --------------------------------------------------

        print_summary(
            statistics
        )

        print()
        print("=" * 80)
        print("[SUCCESS] WAF Detection Completed")
        print("=" * 80)
        print(f"Targets          : {statistics['targets']}")
        print(f"WAF Detected     : {statistics['detected']}")
        print(f"Not Detected     : {statistics['not_detected']}")
        print(f"Success Rate     : {statistics['success_rate']}%")
        print(f"Average Score    : {statistics['average_score']}")
        print(f"Highest Score    : {statistics['highest_score']}")
        print(f"Elapsed Time     : {statistics['elapsed']} sec")
        print("=" * 80)

        return (
            results,
            statistics,
        )

    except KeyboardInterrupt:

        print()
        print("[ERROR] WAF Detection cancelled by user.")
        raise

    except Exception as error:

        print()
        print("[ERROR] WAF Detection failed.")
        print(f"[ERROR] {error}")
        raise