#!/usr/bin/env python3

"""
Recon Automation Framework

Main Entry Point
"""

from __future__ import annotations

import sys

from time import perf_counter
from typing import Any, Callable

from cli.config import build_config
from cli.parser import parse_arguments
from cli.pipeline import build_pipeline

from core.banner import show_banner
from core.context import ExecutionContext
from core.executor import execute_module
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
    [dict[str, Any]],
    None,
]


# ==========================================================
# Exporters
# ==========================================================

EXPORTERS: dict[str, Exporter] = {

    "fuzzing": export_fuzzing_results,

    "nuclei": export_nuclei_results,

    "takeover": export_takeover_results,

}


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
    Execute a framework module
    and export its results if required.
    """

    if not config["quiet"]:

        info(
            f"[{index}/{total}] "
            f"Running {module} module..."
        )

    arguments: tuple[Any, ...] = ()

    if module == "passive":

        arguments = (
            config["target"],
        )

    analysis = execute_module(
        context,
        module,
        *arguments,
    )

    exporter = EXPORTERS.get(
        module,
    )

    if exporter is not None:

        exporter(
            analysis,
        )

    if not config["quiet"]:

        success(
            f"Completed {module} module."
        )


# ==========================================================
# Summary
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
        "Recon Completed"
    )

    info(
        f"Modules Executed : {total_modules}"
    )

    info(
        f"Elapsed Time     : {elapsed:.2f} sec"
    )

    info(
        "Output Directory : output/"
    )

    divider()


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Framework entry point.
    """

    start_time = perf_counter()

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

    total_modules = len(
        pipeline,
    )

    for index, module in enumerate(
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

    elapsed = (
        perf_counter()
        - start_time
    )

    if not config["quiet"]:

        print_summary(
            total_modules=total_modules,
            elapsed=elapsed,
            quiet=config["quiet"],
        )

        success(
            f"Framework completed in {elapsed:.2f} sec."
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
            "Execution interrupted by user."
        )

        sys.exit(
            130,
        )

    except ValueError as exception:

        error(
            str(exception),
        )

        sys.exit(
            1,
        )

    except Exception as exception:

        error(
            f"Unexpected error: {exception}"
        )

        sys.exit(
            1,
        )