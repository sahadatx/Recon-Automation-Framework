#!/usr/bin/env python3

"""
Recon Automation Framework

Main Entry Point
"""

from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from cli.config import build_config
from cli.parser import parse_arguments
from cli.pipeline import build_pipeline
from core.banner import show_banner
from core.context import ExecutionContext
from core.executor import execute_module
from core.http import create_http_session
from core.logger import divider, error, info, success
from core.plugins.manager import plugin_manager

# ==========================================================
# Context
# ==========================================================


def create_context(
    config: dict[str, Any],
) -> tuple[
    ExecutionContext,
    Any,
    ThreadPoolExecutor,
]:
    """
    Create the shared execution context.
    """

    context = ExecutionContext()

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

    context.performance.set_target_count(
        config.get(
            "target_count",
            1,
        )
    )

    return (
        context,
        session,
        thread_pool,
    )


# ==========================================================
# Execute Module
# ==========================================================


def execute_pipeline_module(
    context: ExecutionContext,
    module: str,
    index: int,
    total: int,
    config: dict[str, Any],
) -> None:
    """
    Execute one framework module.
    """

    if not config["quiet"]:

        info(f"[{index}/{total}] " f"Running {module}...")

    arguments: tuple[Any, ...] = ()

    #
    # Only Passive Enumeration
    # needs the initial target.
    #

    if module == "passive":

        arguments = (config["target"],)

    execute_module(
        context,
        module,
        *arguments,
    )

    if not config["quiet"]:

        success(f"Completed {module}")


# ==========================================================
# Framework Summary
# ==========================================================


def print_summary(
    pipeline: list[str],
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
        f"Modules Executed : {len(pipeline)}",
    )

    info(
        f"Elapsed Time     : {elapsed:.2f} sec",
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
    Display framework performance summary.
    """

    if quiet:

        return

    report = context.performance.markdown()

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
# Cleanup
# ==========================================================


def cleanup(
    context: ExecutionContext,
    session: Any,
    thread_pool: ThreadPoolExecutor,
) -> None:
    """
    Release framework resources.
    """

    plugin_manager.shutdown()

    thread_pool.shutdown(
        wait=True,
    )

    session.close()

    context.clear()


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

    (
        context,
        session,
        thread_pool,
    ) = create_context(
        config,
    )

    #
    # Start framework timer
    #

    context.performance.start()

    #
    # Discover and initialize plugins
    #

    plugin_manager.initialize()

    try:

        total_modules = len(
            pipeline,
        )

        for (
            index,
            module,
        ) in enumerate(
            pipeline,
            start=1,
        ):

            execute_pipeline_module(
                context=context,
                module=module,
                index=index,
                total=total_modules,
                config=config,
            )

        #
        # Stop framework timer
        #

        framework_elapsed = context.performance.stop()

        #
        # Store statistics
        #

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

        #
        # Generate reports
        #

        context.performance.generate_report()

        #
        # Print summaries
        #

        print_summary(
            pipeline=pipeline,
            elapsed=framework_elapsed,
            quiet=config["quiet"],
        )

        print_performance_summary(
            context=context,
            quiet=config["quiet"],
        )

        if not config["quiet"]:

            success("Framework completed in " f"{framework_elapsed:.2f} sec.")

    finally:

        cleanup(
            context=context,
            session=session,
            thread_pool=thread_pool,
        )


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
    "create_context",
    "execute_pipeline_module",
    "print_summary",
    "print_performance_summary",
    "cleanup",
]
