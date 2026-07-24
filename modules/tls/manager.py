"""
TLS Manager

Coordinates the complete
TLS Analysis pipeline.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import (
    info,
    success,
)

from .certificate import collect_certificate
from .protocols import collect_protocols
from .ciphers import collect_cipher

from .analyzer import analyze
from .filters import filter_results


# ==========================================================
# Run TLS Analysis
# ==========================================================

def run_tls_analysis(
    targets: list[str],
) -> dict[str, Any]:
    """
    Run complete TLS Analysis.
    """

    if not targets:

        return analyze(
            results=[],
            elapsed=0,
        )

    info(
        "Starting TLS Analysis..."
    )

    start = perf_counter()

    results: list[dict[str, Any]] = []

    for target in targets:

        info(
            f"Analyzing {target}..."
        )

        certificate = collect_certificate(
            target
        )

        protocols = collect_protocols(
            target
        )

        cipher = collect_cipher(
            target
        )

        result = analyze(
            certificate,
            protocols,
            cipher,
        )

        result["host"] = target

        results.append(
            result
        )

    results = filter_results(
        results
    )

    elapsed = (
        perf_counter()
        - start
    )

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
        f"Average Risk        : {statistics['average_risk']}"
    )

    success(
        f"Highest Risk        : {statistics['highest_risk']}"
    )

    success(
        f"Expired             : {statistics['expired']}"
    )

    success(
        f"Self Signed         : {statistics['self_signed']}"
    )

    success(
        f"Hostname Mismatch   : {statistics['hostname_mismatch']}"
    )

    success(
        f"Weak Protocol       : {statistics['weak_protocol']}"
    )

    success(
        f"Weak Cipher         : {statistics['weak_cipher']}"
    )

    success(
        f"Wildcard            : {statistics['wildcard']}"
    )

    success(
        f"Forward Secrecy     : {statistics['forward_secrecy']}"
    )

    success(
        f"Elapsed             : {statistics['elapsed']:.2f} sec"
    )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run_tls_analysis",
]