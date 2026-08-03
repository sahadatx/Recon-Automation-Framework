#!/usr/bin/env python3

"""
CDN Manager

Coordinates the complete
CDN Detection pipeline.
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.logger import info, success

from .analyzer import analyze
from .filters import filter_results
from .helpers import (
    extract_headers,
    get_server_header,
    normalize_target,
    request_headers,
    resolve_cname,
    resolve_ipv4,
)
from .target_analyzer import analyze_target

# ==========================================================
# Run CDN Detection
# ==========================================================


def run_cdn_detection(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Run the complete CDN detection workflow.
    """

    if not targets:

        analysis = analyze(
            results=[],
        )

        context.set_analysis(
            "cdn",
            analysis,
        )

        return analysis

    info("Starting CDN Detection...")

    results: list[dict[str, Any]] = []

    for target in targets:

        info(f"Analyzing {target}...")

        host = normalize_target(
            target,
        )

        if not host:
            continue

        response = request_headers(
            context,
            target,
        )

        headers = extract_headers(
            response,
        )

        result = analyze_target(
            target=host,
            headers=headers,
            server=get_server_header(
                headers,
            ),
            cname=resolve_cname(
                host,
            ),
            ip=resolve_ipv4(
                host,
            ),
        )

        results.append(
            result,
        )

    analysis = analyze(
        results=filter_results(
            results,
        ),
    )

    context.set_analysis(
        "cdn",
        analysis,
    )

    statistics = analysis["statistics"]

    success(f"Targets             : {statistics['targets']}")

    success(f"CDN Detected        : {statistics['detected']}")

    success(f"CDN Not Detected    : {statistics['undetected']}")

    success(f"Average Confidence  : " f"{statistics['average_confidence']}")

    success(f"Highest Confidence  : " f"{statistics['highest_confidence']}")

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================


def run(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Public entry point for the CDN module.
    """

    return run_cdn_detection(
        context,
        targets,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_cdn_detection",
]
