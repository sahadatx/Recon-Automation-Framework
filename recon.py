#!/usr/bin/env python3

"""
Recon Automation Framework

Main Entry Point
"""

from __future__ import annotations

import sys

from concurrent.futures import ThreadPoolExecutor

from typing import (
    Any,
    Callable,
)

from cli.config import (
    build_config,
)

from cli.parser import (
    parse_arguments,
)

from cli.pipeline import (
    build_pipeline,
)

from core.banner import (
    show_banner,
)

from core.context import (
    ExecutionContext,
)

from core.executor import (
    execute_module,
)

from core.http import (
    create_http_session,
)

from core.logger import (
    divider,
    error,
    info,
    success,
)

from modules.fuzzing.exporter import (
    export_all as export_fuzzing_results,
)

from modules.nuclei.exporter import (
    export_all as export_nuclei_results,
)

from modules.takeover.exporter import (
    export_all as export_takeover_results,
)


# ==========================================================
# Types
# ==========================================================

Exporter = Callable[
    [
        dict[str, Any],
    ],
    None,
]


# ==========================================================
# Exporters
# ==========================================================

EXPORTERS: dict[
    str,
    Exporter,
] = {
    "fuzzing": export_fuzzing_results,
    "nuclei": export_nuclei_results,
    "takeover": export_takeover_results,
}


# ==========================================================
# Export Analysis
# ==========================================================


def export_analysis(
    module: str,
    analysis: dict[str, Any] | None,
) -> None:
    """
    Export module analysis.

    Only modules registered in
    EXPORTERS are exported.
    """

    if analysis is None:

        return

    exporter = EXPORTERS.get(
        module,
    )

    if exporter is None:

        return

    exporter(
        analysis,
    )


# ==========================================================
# Execute Module
# ==========================================================


def execute_module_pipeline(
    context: ExecutionContext,
    module: str,
    index: int,
    total: int,
    config: dict[str, Any],
) -> None:
    """
    Execute one framework module.

    Workflow

        Start Timer
              ↓
        Execute Module
              ↓
        Stop Timer
              ↓
        Export
              ↓
        Success Message
    """

    if not config["quiet"]:

        info(
            f"[{index}/{total}] "
            f"Running {module} module..."
        )

    arguments: tuple[
        Any,
        ...,
    ] = ()

    if module == "passive":

        arguments = (
            config["target"],
        )

    analysis: dict[
        str,
        Any,
    ] | None = None

    context.performance.start_module(
        module,
    )

    try:

        analysis = execute_module(
            context,
            module,
            *arguments,
        )

    finally:

        elapsed = (
            context.performance.stop_module(
                module,
            )
        )

    export_analysis(
        module,
        analysis,
    )

    if not config["quiet"]:

        success(
            f"Completed {module} module "
            f"({elapsed:.2f} sec)"
        )


# ==========================================================
# Framework Summary
# ==========================================================


def print_summary(
    total_modules: int,
    elapsed: float,
    quiet: bool,
) -> None:
    """
    Display framework summary.
    """

    if quiet:

        return

    divider()

    success(
        "Recon Completed",
    )

    info(
        f"Modules Executed : "
        f"{total_modules}",
    )

    info(
        f"Elapsed Time     : "
        f"{elapsed:.2f} sec",
    )

    info(
        "Output Directory : output/",
    )

    divider()


# ==========================================================
# Performance Summary
# ==========================================================


def print_performance_summary(
    context: ExecutionContext,
    quiet: bool,
) -> None:
    """
    Display framework performance
    summary.
    """

    if quiet:

        return

    report = (
        context.performance.markdown()
    )

    if not report:

        return

    divider()

    success(
        "Performance Summary",
    )

    print(
        report,
    )

    divider()


# ==========================================================
# Main
# ==========================================================


def main() -> None:
    """
    Framework entry point.
    """

    arguments = parse_arguments()

    config = build_config(
        arguments,
    )

    pipeline = build_pipeline(
        config,
    )

    if not config["quiet"]:

        show_banner()

    context = ExecutionContext()

    context.performance.start()

    session = create_http_session()

    thread_pool = ThreadPoolExecutor(
        max_workers=config["threads"],
    )

    context.set_http_session(
        session,
    )

    context.set_thread_pool(
        thread_pool,
    )

    try:

        total_modules = len(
            pipeline,
        )

        context.performance.set_target_count(
            config.get(
                "target_count",
                1,
            )
        )

        for (
            index,
            module,
        ) in enumerate(
            pipeline,
            start=1,
        ):

            execute_module_pipeline(
                context=context,
                module=module,
                index=index,
                total=total_modules,
                config=config,
            )

        framework_elapsed = (
            context.performance.stop()
        )

        context.set_statistic(
            "framework_time",
            framework_elapsed,
        )

        context.set_statistic(
            "modules",
            total_modules,
        )

        context.set_statistic(
            "pipeline",
            pipeline,
        )

        context.set_statistic(
            "performance",
            context.performance.summary(),
        )

        context.performance.generate_report()

        print_summary(
            total_modules=total_modules,
            elapsed=framework_elapsed,
            quiet=config["quiet"],
        )

        print_performance_summary(
            context=context,
            quiet=config["quiet"],
        )

        if not config["quiet"]:

            success(
                "Framework completed in "
                f"{framework_elapsed:.2f} sec."
            )

    finally:

        thread_pool.shutdown(
            wait=True,
        )

        session.close()

        context.clear()


# ==========================================================
# Entry Point
# ==========================================================


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()

        error(
            "Execution interrupted by user.",
        )

        sys.exit(
            130,
        )

    except ValueError as exception:

        error(
            str(
                exception,
            ),
        )

        sys.exit(
            1,
        )

    except Exception as exception:

        error(
            f"Unexpected error: {exception}",
        )

        sys.exit(
            1,
        )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "main",
    "execute_module_pipeline",
    "export_analysis",
    "print_summary",
    "print_performance_summary",
]