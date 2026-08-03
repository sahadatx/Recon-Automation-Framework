#!/usr/bin/env python3

"""
Email Security Manager

Coordinate Email Security analysis.
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.logger import info, success

from .analyzer import analyze
from .filters import filter_results
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
from .target_analyzer import analyze_target

# ==========================================================
# Run Email Security Analysis
# ==========================================================


def run_email_security(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Execute the complete Email Security workflow.

        Collect
            ↓
        Analyze
            ↓
        Store Context
            ↓
        Return Analysis
    """

    if not targets:

        analysis = analyze(
            results=[],
        )

        context.set_analysis(
            "email_security",
            analysis,
        )

        return analysis

    info("Starting Email Security Analysis...")

    results: list[dict[str, Any]] = []

    for target in targets:

        info(f"Analyzing {target}...")

        host = normalize_target(
            target,
        )

        if not host:
            continue

        mx = resolve_mx(host)

        spf, spf_record = resolve_spf(host)

        dkim, dkim_selector = resolve_dkim(host)

        dmarc, dmarc_record = resolve_dmarc(host)

        mta_sts = resolve_mta_sts(host)

        tls_rpt = resolve_tls_rpt(host)

        bimi = resolve_bimi(host)

        dnssec = resolve_dnskey(host)

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

        results.append(
            analyze_target(result),
        )

    analysis = analyze(
        results=filter_results(
            results,
        ),
    )

    context.set_analysis(
        "email_security",
        analysis,
    )

    statistics = analysis["statistics"]

    success(f"Targets             : {statistics['targets']}")

    success(f"Low Risk            : {statistics['low']}")

    success(f"Medium Risk         : {statistics['medium']}")

    success(f"High Risk           : {statistics['high']}")

    success(f"Critical Risk       : {statistics['critical']}")

    success(f"Average Score       : {statistics['average_score']}")

    success(f"Highest Score       : {statistics['highest_score']}")

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================


def run(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Public entry point for the
    Email Security module.
    """

    return run_email_security(
        context,
        targets,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_email_security",
]
