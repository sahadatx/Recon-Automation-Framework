"""
Takeover Manager

Coordinates the complete
Subdomain Takeover
Detection pipeline.
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
    request_page,
    extract_status_code,
    extract_body,
    extract_title,
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
# Run Takeover Detection
# ==========================================================

def run_takeover_detection(
    targets: list[str],
) -> dict[str, Any]:
    """
    Run complete
    Subdomain Takeover
    Detection pipeline.
    """

    if not targets:

        return analyze(
            results=[],
            elapsed=0,
        )

    info(
        "Starting Subdomain Takeover Detection..."
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
        # HTTP
        # --------------------------------------------------

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

        # --------------------------------------------------
        # DNS
        # --------------------------------------------------

        cname = resolve_cname(
            host,
        )

        ip = resolve_ipv4(
            host,
        )

        # --------------------------------------------------
        # Analyze Target
        # --------------------------------------------------

        result = analyze_target(
            target=host,
            body=body,
            status_code=status_code,
            cname=cname,
            ip=ip,
            http_title=http_title,
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
        f"Vulnerable          : {statistics['vulnerable']}"
    )

    success(
        f"Safe                : {statistics['safe']}"
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
# Public Exports
# ==========================================================

__all__ = [
    "run_takeover_detection",
]