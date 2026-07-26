"""
CDN Manager

Coordinates the complete
CDN Detection pipeline.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from core.logger import (
    info,
    success,
)

from .helpers import (
    normalize_target,
    request_headers,
    extract_headers,
    get_server_header,
    resolve_cname,
    resolve_ipv4,
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
# Run CDN Detection
# ==========================================================

def run_cdn_detection(
    targets: list[str],
) -> dict[str, Any]:
    """
    Run complete CDN Detection.
    """

    if not targets:

        return analyze(
            results=[],
            elapsed=0,
        )

    info(
        "Starting CDN Detection..."
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

        response = request_headers(
            target,
        )

        headers = extract_headers(
            response,
        )

        server = get_server_header(
            headers,
        )

        cname = resolve_cname(
            host,
        )

        ip = resolve_ipv4(
            host,
        )

        result = analyze_target(
            target=host,
            headers=headers,
            server=server,
            cname=cname,
            ip=ip,
        )

        results.append(
            result,
        )

    results = filter_results(
        results,
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
        f"CDN Detected        : {statistics['detected']}"
    )

    success(
        f"CDN Not Detected    : {statistics['undetected']}"
    )

    success(
        f"Average Confidence  : {statistics['average_confidence']}"
    )

    success(
        f"Highest Confidence  : {statistics['highest_confidence']}"
    )

    success(
        f"Elapsed             : {statistics['elapsed']:.2f} sec"
    )

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================

def run(
    targets: list[str],
) -> dict[str, Any]:
    """
    Public entry point for the CDN module.
    """

    return run_cdn_detection(
        targets,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_cdn_detection",
]