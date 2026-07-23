"""
TLS Manager

Main entry point for
TLS Analysis.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import info

from modules.tls.certificate import collect_certificate
from modules.tls.protocols import collect_protocols
from modules.tls.ciphers import collect_cipher
from modules.tls.analyzer import analyze
from modules.tls.filters import filter_results
from modules.tls.statistics import (
    generate_statistics,
    print_summary,
)
from modules.tls.exporter import (
    export_results,
)


# ==========================================================
# Run TLS Analysis
# ==========================================================

def run_tls_analysis(
    targets: list[str],
) -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
]:
    """
    Run complete TLS Analysis pipeline.

    Pipeline:
        Certificate
        -> Protocols
        -> Cipher
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

        "TLS Analysis".center(

            80

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

            # ----------------------------------------------
            # Certificate
            # ----------------------------------------------

            certificate = collect_certificate(

                target

            )

            # ----------------------------------------------
            # Protocols
            # ----------------------------------------------

            protocols = collect_protocols(

                target

            )

            # ----------------------------------------------
            # Cipher
            # ----------------------------------------------

            cipher = collect_cipher(

                target

            )

            # ----------------------------------------------
            # Analysis
            # ----------------------------------------------

            result = analyze(

                certificate,

                protocols,

                cipher,

            )

            result["host"] = target

            results.append(

                result

            )

        # --------------------------------------------------
        # Filter Results
        # --------------------------------------------------

        info(

            "Filtering results..."

        )

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

            statistics

        )

        print()

        print("=" * 80)

        print(

            "[SUCCESS] TLS Analysis Completed"

        )

        print("=" * 80)

        print(

            f"Targets             : {statistics['targets']}"

        )

        print(

            f"Average Risk        : {statistics['average_risk']}"

        )

        print(

            f"Highest Risk        : {statistics['highest_risk']}"

        )

        print(

            f"Expired             : {statistics['expired']}"

        )

        print(

            f"Self Signed         : {statistics['self_signed']}"

        )

        print(

            f"Hostname Mismatch   : {statistics['hostname_mismatch']}"

        )

        print(

            f"Weak Protocol       : {statistics['weak_protocol']}"

        )

        print(

            f"Weak Cipher         : {statistics['weak_cipher']}"

        )

        print(

            f"Wildcard            : {statistics['wildcard']}"

        )

        print(

            f"Forward Secrecy     : {statistics['forward_secrecy']}"

        )

        print(

            f"Elapsed Time        : {statistics['elapsed']} sec"

        )

        print("=" * 80)

        return (

            results,

            statistics,

        )

    except KeyboardInterrupt:

        print()

        print(

            "[ERROR] TLS Analysis cancelled by user."

        )

        raise

    except Exception as error:

        print()

        print(

            "[ERROR] TLS Analysis failed."

        )

        print(

            f"[ERROR] {error}"

        )

        raise


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "run_tls_analysis",

]