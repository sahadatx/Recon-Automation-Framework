"""
Takeover Manager

Main entry point for
Subdomain Takeover
Detection.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import info

from modules.takeover.helpers import (
    normalize_target,
    request_page,
    extract_status_code,
    extract_body,
    extract_title,
    resolve_cname,
    resolve_ipv4,
)

from modules.takeover.analyzer import (
    analyze,
)

from modules.takeover.filters import (
    filter_results,
)

from modules.takeover.statistics import (
    generate_statistics,
    print_summary,
)

from modules.takeover.exporter import (
    export_results,
)


# ==========================================================
# Run Takeover Detection
# ==========================================================

def run_takeover_detection(
    targets: list[str],
) -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
]:
    """
    Run complete
    Takeover Detection
    pipeline.

    Pipeline:
        HTTP
        -> DNS
        -> Analysis
        -> Filter
        -> Statistics
        -> Export

    Returns:
        tuple(
            results,
            statistics,
        )
    """

    print()

    print("=" * 80)

    print(

        "Subdomain Takeover Detection".center(

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

                    f"Skipping invalid target: "

                    f"{target}"

                )

                continue

            # ----------------------------------------------
            # HTTP
            # ----------------------------------------------

            response = request_page(

                target,

            )

            status_code = extract_status_code(

                response,

            )

            body = extract_body(

                response,

            )

            http_title = extract_title(

                response,

            )

            # ----------------------------------------------
            # DNS
            # ----------------------------------------------

            cname = resolve_cname(

                host,

            )

            ip = resolve_ipv4(

                host,

            )

            # ----------------------------------------------
            # Analysis
            # ----------------------------------------------

            result = analyze(

                host,

                body,

                status_code,

                cname,

                ip,

                http_title,

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

            "[SUCCESS] Subdomain Takeover Detection Completed"

        )

        print("=" * 80)

        print(

            f"Targets             : "

            f"{statistics['targets']}"

        )

        print(

            f"Vulnerable          : "

            f"{statistics['vulnerable']}"

        )

        print(

            f"Safe                : "

            f"{statistics['safe']}"

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

            "[ERROR] Subdomain Takeover Detection "

            "cancelled by user."

        )

        raise

    except Exception as error:

        print()

        print(

            "[ERROR] Subdomain Takeover Detection "

            "failed."

        )

        print(

            f"[ERROR] {error}"

        )

        raise


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "run_takeover_detection",

]

