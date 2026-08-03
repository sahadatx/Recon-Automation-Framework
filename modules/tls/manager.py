#!/usr/bin/env python3

"""
TLS Manager

Coordinate TLS analysis.
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.logger import (
    info,
    success,
)

from .analyzer import (
    analyze,
    analyze_host,
)
from .certificate import collect_certificate
from .ciphers import collect_cipher
from .filters import filter_results
from .protocols import collect_protocols

# ==========================================================
# Run TLS Analysis
# ==========================================================


def run_tls_analysis(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Execute the complete
    TLS analysis workflow.

        Collect
            ↓
        Filter
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
            "tls",
            analysis,
        )

        return analysis

    info("Starting TLS Analysis...")

    results: list[dict[str, Any]] = []

    for target in targets:

        info(f"Analyzing {target}...")

        certificate = collect_certificate(
            target,
        )

        protocols = collect_protocols(
            target,
        )

        cipher = collect_cipher(
            target,
        )

        result = analyze_host(
            certificate=certificate,
            protocols=protocols,
            cipher=cipher,
        )

        results.append(
            result,
        )

    results = filter_results(
        results,
    )

    analysis = analyze(
        results=results,
    )

    context.set_analysis(
        "tls",
        analysis,
    )

    statistics = analysis["statistics"]

    success(f"Targets             : {statistics['targets']}")

    success(f"Average Risk        : {statistics['average_risk']}")

    success(f"Highest Risk        : {statistics['highest_risk']}")

    success(f"Expired             : {statistics['expired']}")

    success(f"Self Signed         : {statistics['self_signed']}")

    success(f"Hostname Mismatch   : {statistics['hostname_mismatch']}")

    success(f"Weak Protocol       : {statistics['weak_protocol']}")

    success(f"Weak Cipher         : {statistics['weak_cipher']}")

    success(f"Wildcard            : {statistics['wildcard']}")

    success(f"Forward Secrecy     : {statistics['forward_secrecy']}")

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
    TLS module.
    """

    return run_tls_analysis(
        context,
        targets,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_tls_analysis",
]
