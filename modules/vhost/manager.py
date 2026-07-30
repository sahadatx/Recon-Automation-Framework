#!/usr/bin/env python3

"""
Virtual Host Discovery Manager

Coordinate virtual host
discovery and analysis.
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
    apply_filters,
)

from .interesting import (
    scan as detect_interesting,
)

from .parser import (
    parse_ffuf,
)

from .scanner import (
    scan_target,
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
    Scan one target.
    """

    scan = scan_target(
        target,
    )

    if not scan["success"]:

        return (
            target,
            None,
        )

    output = scan[
        "output"
    ]

    try:

        parsed = parse_ffuf(
            output,
        )

        if parsed is None:

            return (
                target,
                None,
            )

        results = apply_filters(
            parsed.get(
                "results",
                [],
            ),
        )

        interesting = detect_interesting(
            results,
        )

        return (
            target,
            {
                "results": results,
                "interesting": interesting,
            },
        )

    finally:

        # cleanup(output)
        pass


# ==========================================================
# Collect Results
# ==========================================================


def collect_results(
    results: dict[
        str,
        dict[str, Any],
    ],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """
    Merge scan results.
    """

    findings: list[
        dict[str, Any]
    ] = []

    interesting: list[
        dict[str, Any]
    ] = []

    for data in results.values():

        findings.extend(
            data.get(
                "results",
                [],
            ),
        )

        interesting.extend(
            data.get(
                "interesting",
                [],
            ),
        )

    return (
        findings,
        interesting,
    )


# ==========================================================
# Run Virtual Host Discovery
# ==========================================================


def run_vhosts(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:
    """
    Execute the complete
    virtual host discovery
    workflow.

        Scan
            ↓
        Collect
            ↓
        Analyze
            ↓
        Store Context
            ↓
        Return Analysis
    """

    if not targets:

        warning(
            "No targets supplied.",
        )

        analysis = analyze(
            results=[],
            interesting=[],
        )

        context.set_analysis(
            "vhost",
            analysis,
        )

        return analysis

    info(
        "Starting Virtual Host Discovery...",
    )

    targets = sorted(
        set(
            targets,
        ),
    )

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError(
            "Shared thread pool is not initialized.",
        )

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed: list[str] = []

    completed = 0

    total = len(
        targets,
    )

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

        target = futures[
            future
        ]

        completed += 1

        try:

            (
                hostname,
                data,
            ) = future.result()

            if data is None:

                failed.append(
                    hostname,
                )

                progress_status(
                    completed,
                    total,
                    f"✗ {hostname}",
                )

                continue

            results[
                hostname
            ] = data

            progress_status(
                completed,
                total,
                f"✓ {hostname}",
            )

        except Exception as error:

            failed.append(
                target,
            )

            warning(
                f"{target}: {error}",
            )

            progress_status(
                completed,
                total,
                f"✗ {target}",
            )

    (
        findings,
        interesting,
    ) = collect_results(
        results,
    )

    analysis = analyze(
        results=findings,
        interesting=interesting,
    )

    statistics = analysis[
        "statistics"
    ]

    statistics.update(
        {
            "total_targets": total,
            "successful": len(
                results,
            ),
            "failed": len(
                failed,
            ),
        },
    )

    analysis[
        "failed"
    ] = sorted(
        failed,
    )

    context.set_analysis(
        "vhost",
        analysis,
    )

    success(
        f"Targets             : {total}",
    )

    success(
        f"Successful          : {len(results)}",
    )

    success(
        f"Failed              : {len(failed)}",
    )

    success(
        f"Discovered Hosts    : "
        f"{statistics['total_results']}",
    )

    success(
        f"Interesting Hosts   : "
        f"{statistics['interesting_hosts']}",
    )

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
    Virtual Host Discovery module.
    """

    return run_vhosts(
        context,
        targets,
    )


# ==========================================================
# Successful Targets
# ==========================================================


def successful_targets(
    analysis: dict[str, Any],
) -> list[str]:
    """
    Return successful targets.
    """

    return sorted(
        {
            result.get(
                "target",
                "",
            )

            for result in analysis.get(
                "results",
                [],
            )

            if result.get(
                "target",
            )
        },
    )


# ==========================================================
# Failed Targets
# ==========================================================


def failed_targets(
    analysis: dict[str, Any],
) -> list[str]:
    """
    Return failed targets.
    """

    return sorted(
        analysis.get(
            "failed",
            [],
        ),
    )


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "run",
    "run_vhosts",
    "successful_targets",
    "failed_targets",
]