from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import info, progress_status, success, warning

from .analyzer import analyze
from .filters import apply_filters
from .parser import parse_nuclei
from .scanner import cleanup, scan_target


def process_target(
    target: str,
) -> tuple[
    str,
    list[dict[str, Any]] | None,
]:


    scan = scan_target(
        target,
    )

    if not scan["success"]:

        return (
            target,
            None,
        )

    output = scan["output"]

    try:

        parsed = parse_nuclei(
            output,
        )

        if parsed is None:

            return (
                target,
                None,
            )

        findings = apply_filters(
            parsed.get(
                "findings",
                [],
            )
        )

        return (
            target,
            findings,
        )

    finally:

        cleanup(
            output,
        )


def collect_findings(
    results: dict[
        str,
        list[dict[str, Any]],
    ],
) -> list[dict[str, Any]]:


    findings: list[dict[str, Any]] = []

    for target_findings in results.values():

        findings.extend(
            target_findings,
        )

    return findings


def run_nuclei(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:


    if not targets:

        warning("No targets supplied.")

        analysis = analyze(
            results=[],
            failed=[],
        )

        context.set_analysis(
            "nuclei",
            analysis,
        )

        return analysis

    info("Starting Nuclei Scan...")

    targets = sorted(
        set(
            targets,
        )
    )

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Shared thread pool is not initialized.")

    results: dict[
        str,
        list[dict[str, Any]],
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

        target = futures[future]

        completed += 1

        try:

            (
                hostname,
                findings,
            ) = future.result()

            if findings is not None:

                results[hostname] = findings

                progress_status(
                    completed,
                    total,
                    f"✓ {hostname}",
                )

            else:

                failed.append(
                    hostname,
                )

                progress_status(
                    completed,
                    total,
                    f"✗ {hostname}",
                )

        except KeyboardInterrupt:

            warning("Scan interrupted.")

            raise

        except Exception as error:

            warning(f"{target}: {error}")

            failed.append(
                target,
            )

            progress_status(
                completed,
                total,
                f"✗ {target}",
            )

    findings = collect_findings(
        results,
    )

    analysis = analyze(
        results=findings,
        failed=failed,
    )

    statistics = analysis["statistics"]

    statistics.update(
        {
            "total_targets": total,
            "successful": len(results),
            "failed": len(failed),
        }
    )

    context.set_analysis(
        "nuclei",
        analysis,
    )

    success(f"Targets      : {statistics['total_targets']}")

    success(f"Successful   : {statistics['successful']}")

    success(f"Failed       : {statistics['failed']}")

    success(f"Findings     : {statistics['total_findings']}")

    return analysis


def run(
    context: ExecutionContext,
    targets: list[str],
) -> dict[str, Any]:


    return run_nuclei(
        context,
        targets,
    )


def successful_targets(
    analysis: dict[str, Any],
) -> list[str]:


    target_statistics = analysis["statistics"].get(
        "target_statistics",
        {},
    )

    return sorted(
        target_statistics.keys(),
    )


def failed_targets(
    analysis: dict[str, Any],
) -> list[str]:


    return sorted(
        analysis.get(
            "failed",
            [],
        )
    )


__all__ = [
    "run",
    "run_nuclei",
    "successful_targets",
    "failed_targets",
]
