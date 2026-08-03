#!/usr/bin/env python3

"""
Takeover Manager

Coordinate subdomain takeover
detection and analysis.
"""

from __future__ import annotations

from concurrent.futures import (
    as_completed,
)

from typing import Any

from core.context import (
    ExecutionContext,
)

from core.logger import (
    info,
    progress_status,
    success,
    warning,
)

from .analyzer import (
    analyze,
)

from .filters import (
    filter_results,
)

from .helpers import (
    extract_body,
    extract_status_code,
    extract_title,
    normalize_target,
    request_page,
    resolve_cname,
    resolve_ipv4,
)

from .target_analyzer import (
    analyze_target,
)

# ==========================================================
# Process Target
# ==========================================================


def process_target(
    target: str,
) -> tuple[
    str,
    dict[str, Any] | None,
]:
    """
    Analyze one target.
    """

    host = normalize_target(
        target,
    )

    if not host:

        return (
            target,
            None,
        )

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

    cname = resolve_cname(
        host,
    )

    ip = resolve_ipv4(
        host,
    )

    result = analyze_target(
        target=host,
        body=body,
        status_code=status_code,
        cname=cname,
        ip=ip,
        http_title=http_title,
    )

    return (
        host,
        result,
    )


# ==========================================================
# Run Takeover Detection
# ==========================================================


def run_takeover_detection(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Execute the complete
    takeover detection workflow.

        Scan
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
            "takeover",
            analysis,
        )

        return analysis

    info("Starting Subdomain Takeover Detection...")

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Shared thread pool is not initialized.")

    targets = sorted(
        set(
            targets,
        )
    )

    completed = 0

    total = len(
        targets,
    )

    results: list[dict[str, Any]] = []

    futures = {
        executor.submit(
            process_target,
            target,
        ): target
        for target in targets
    }

    for future in as_completed(
        futures,
    ):

        target = futures[future]

        completed += 1

        try:

            (
                _,
                result,
            ) = future.result()

            if result is None:

                progress_status(
                    completed,
                    total,
                    f"✗ {target}",
                )

                continue

            results.append(
                result,
            )

            progress_status(
                completed,
                total,
                f"✓ {target}",
            )

        except Exception as error:

            warning(f"{target}: {error}")

            progress_status(
                completed,
                total,
                f"✗ {target}",
            )

    results = filter_results(
        results,
    )

    analysis = analyze(
        results=results,
    )

    context.set_analysis(
        "takeover",
        analysis,
    )

    statistics = analysis["statistics"]

    success(f"Targets             : {statistics['targets']}")

    success(f"Vulnerable          : {statistics['vulnerable']}")

    success(f"Safe                : {statistics['safe']}")

    success(f"Average Confidence  : {statistics['average_confidence']}")

    success(f"Highest Confidence  : {statistics['highest_confidence']}")

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
    Takeover module.
    """

    return run_takeover_detection(
        context,
        targets,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_takeover_detection",
]
