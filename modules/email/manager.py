"""
Email Security Manager

Main entry point for
Email Security
Analysis.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import info

from modules.email.helpers import (
    create_result,
    normalize_target,
    resolve_bimi,
    resolve_dkim,
    resolve_dmarc,
    resolve_dnskey,
    resolve_mta_sts,
    resolve_mx,
    resolve_spf,
    resolve_tls_rpt,
)

from modules.email.analyzer import (
    analyze,
)

from modules.email.filters import (
    filter_results,
)

from modules.email.statistics import (
    generate_statistics,
    print_summary,
)

from modules.email.exporter import (
    export_results,
)


# ==========================================================
# Run Email Security Analysis
# ==========================================================

def run_email_security(
    targets: list[str],
) -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
]:
    """
    Run complete
    Email Security
    pipeline.

    Pipeline:
        DNS
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

        "Email Security Analysis".center(

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
            # DNS
            # ----------------------------------------------

            mx = resolve_mx(

                host,

            )

            spf, spf_record = resolve_spf(

                host,

            )

            dkim, dkim_selector = resolve_dkim(

                host,

            )

            dmarc, dmarc_record = resolve_dmarc(

                host,

            )

            mta_sts = resolve_mta_sts(

                host,

            )

            tls_rpt = resolve_tls_rpt(

                host,

            )

            bimi = resolve_bimi(

                host,

            )

            dnssec = resolve_dnskey(

                host,

            )

            # ----------------------------------------------
            # Create Result
            # ----------------------------------------------

            result = create_result(

                host,

                mx,

                spf,

                spf_record,

                dkim,

                dkim_selector,

                dmarc,

                dmarc_record,

                mta_sts,

                tls_rpt,

                bimi,

                dnssec,

            )

            # ----------------------------------------------
            # Analysis
            # ----------------------------------------------

            result = analyze(

                result,

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

            "[SUCCESS] Email Security Analysis Completed"

        )

        print("=" * 80)

        print(

            f"Targets             : "

            f"{statistics['targets']}"

        )

        print(

            f"Low Risk            : "

            f"{statistics['low']}"

        )

        print(

            f"Medium Risk         : "

            f"{statistics['medium']}"

        )

        print(

            f"High Risk           : "

            f"{statistics['high']}"

        )

        print(

            f"Critical Risk       : "

            f"{statistics['critical']}"

        )

        print(

            f"Average Score       : "

            f"{statistics['average_score']}"

        )

        print(

            f"Highest Score       : "

            f"{statistics['highest_score']}"

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

            "[ERROR] Email Security Analysis "

            "cancelled by user."

        )

        raise

    except Exception as error:

        print()

        print(

            "[ERROR] Email Security Analysis "

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

    "run_email_security",

]