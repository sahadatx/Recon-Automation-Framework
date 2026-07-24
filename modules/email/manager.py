"""
Email Security Manager

Coordinates the complete
Email Security
pipeline.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import (
    info,
    success,
)

from .helpers import (
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

from .target_analyzer import (
    analyze_target,
)

from .analyzer import (
    analyze,
)

from .filters import (
    filter_results,
)


# ==========================================================
# Run Email Security Analysis
# ==========================================================

def run_email_security(
    targets: list[str],
) -> dict[str, Any]:
    """
    Run complete
    Email Security pipeline.
    """

    if not targets:

        return analyze(
            results=[],
            elapsed=0,
        )

    info(
        "Starting Email Security Analysis..."
    )

    start = perf_counter()

    results: list[dict[str, Any]] = []

    for target in targets:

        info(
            f"Analyzing {target}..."
        )

        host = normalize_target(
            target,
        )

        if not host:
            continue

        # --------------------------------------------------
        # DNS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Create Result
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Analyze Target
        # --------------------------------------------------

        result = analyze_target(
            result,
        )

        results.append(
            result,
        )

    # ------------------------------------------------------
    # Filter Results
    # ------------------------------------------------------

    results = filter_results(
        results,
    )

    elapsed = (
        perf_counter()
        - start
    )

    # ------------------------------------------------------
    # Module Analysis
    # ------------------------------------------------------

    analysis = analyze(
        results=results,
        elapsed=elapsed,
    )

    statistics = analysis[
        "statistics"
    ]

    success(
        f"Targets             : {statistics['targets']}"
    )

    success(
        f"Low Risk            : {statistics['low']}"
    )

    success(
        f"Medium Risk         : {statistics['medium']}"
    )

    success(
        f"High Risk           : {statistics['high']}"
    )

    success(
        f"Critical Risk       : {statistics['critical']}"
    )

    success(
        f"Average Score       : {statistics['average_score']}"
    )

    success(
        f"Highest Score       : {statistics['highest_score']}"
    )

    success(
        f"Elapsed             : {statistics['elapsed']:.2f} sec"
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run_email_security",
]