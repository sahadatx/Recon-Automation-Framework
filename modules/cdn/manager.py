"""
CDN Manager

Main entry point for
CDN Detection.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import info

from modules.cdn.helpers import (
    normalize_target,
    request_headers,
    extract_headers,
    get_server_header,
    resolve_cname,
    resolve_ipv4,
)

from modules.cdn.analyzer import analyze
from modules.cdn.filters import filter_results
from modules.cdn.statistics import (
    generate_statistics,
    print_summary,
)
from modules.cdn.exporter import (
    export_results,
)


# ==========================================================
# Run CDN Detection
# ==========================================================

def run_cdn_detection(
    targets: list[str],
) -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
]:
    """
    Run complete CDN Detection pipeline.

    Pipeline:
        Headers
        -> CNAME
        -> IP
        -> Analyzer
        -> Filter
        -> Statistics
        -> Export

    Returns:
        tuple(results, statistics)
    """

    print()

    print("=" * 80)

    print(

        "CDN Detection".center(

            80,

        )

    )

    print("=" * 80)

    start = perf_counter()

    results = []

    try:

        # --------------------------------------------------
        # Analyze Targets
        # --------------------------------------------------

        for target in targets:

            info(

                f"Analyzing {target}..."

            )

            host = normalize_target(

                target,

            )

            if not host:

                info(

                    f"Skipping invalid target: {target}"

                )

                continue

            # ----------------------------------------------
            # Headers
            # ----------------------------------------------

            response = request_headers(
                target,
            )

            headers = extract_headers(
                response,
            )

            server = get_server_header(

                headers,

            )           

            # ----------------------------------------------
            # CNAME
            # ----------------------------------------------

            cname = resolve_cname(

                host,

            )

            # ----------------------------------------------
            # IP
            # ----------------------------------------------

            ip = resolve_ipv4(

                host,

            )

            # ----------------------------------------------
            # Analysis
            # ----------------------------------------------

            result = analyze(

                host,

                headers,

                server,

                cname,

                ip,

            )

            results.append(

                result,

            )


        # --------------------------------------------------
        # Filter Results
        # --------------------------------------------------

        info(

            "Filtering results..."

        )

        results = filter_results(

            results,

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

        info(

            "Exporting results..."

        )

        export_results(

            results,

            statistics,

        )

        # --------------------------------------------------
        # Print Summary
        # --------------------------------------------------

        print_summary(

            statistics,

        )

        print()

        print("=" * 80)

        print(

            "[SUCCESS] CDN Detection Completed"

        )

        print("=" * 80)

        print(

            f"Targets             : {statistics['targets']}"

        )

        print(

            f"CDN Detected        : {statistics['detected']}"

        )

        print(

            f"CDN Not Detected    : {statistics['undetected']}"

        )

        print(

            f"Average Confidence  : "
            f"{statistics['average_confidence']}"

        )

        print(

            f"Highest Confidence  : "
            f"{statistics['highest_confidence']}"

        )

        print(

            f"Elapsed Time        : "
            f"{statistics['elapsed']} sec"

        )

        print("=" * 80)

        return (

            results,

            statistics,

        )

    except KeyboardInterrupt:

        print()

        print(

            "[ERROR] CDN Detection cancelled by user."

        )

        raise

    except Exception as error:

        print()

        print(

            "[ERROR] CDN Detection failed."

        )

        print(

            f"[ERROR] {error}"

        )

        raise


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "run_cdn_detection",

]