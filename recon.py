from __future__ import annotations

import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cli.config import build_config
from cli.parser import parse_arguments
from cli.pipeline import build_pipeline
from core.banner import show_banner
from core.context import ExecutionContext
from core.executor import execute_module
from core.http import create_http_session
from core.logger import console, divider, error, success
from core.plugins.manager import plugin_manager


def create_context(
    config: dict[str, Any],
) -> tuple[
    ExecutionContext,
    Any,
    ThreadPoolExecutor,
]:


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


def execute_pipeline_module(
    context: ExecutionContext,
    module: str,
    index: int,
    total: int,
    config: dict[str, Any],
) -> None:


    if not config["quiet"]:

        console.print()
        stage = Table.grid(expand=True, padding=(0, 1))
        stage.add_column(ratio=1)
        stage.add_column(justify="right")
        stage.add_row(
            Text(f"{module.upper()}  ·  RUNNING", style="bold bright_cyan"),
            Text(f"MODULE {index:02}/{total:02}", style="bold white"),
        )

        filled = round(24 * index / total) if total else 0
        bar = Text("━" * filled, style="bright_cyan")
        bar.append("━" * (24 - filled), style="grey30")
        percent = f"  {index * 100 / total:.0f}%" if total else "  0%"
        bar.append(percent, style="bold white")

        stage.add_row(bar, Text("PIPELINE", style="dim"))
        console.print(
            Panel(
                stage,
                border_style="bright_blue",
                box=box.ROUNDED,
                padding=(0, 1),
            )
        )

    arguments: tuple[Any, ...] = ()


    if module == "passive":

        arguments = (config["target"],)

    started_at = time.perf_counter()
    analysis = execute_module(
        context,
        module,
        *arguments,
    )
    elapsed = time.perf_counter() - started_at

    if not config["quiet"]:

        summary = Table(
            box=box.ROUNDED,
            header_style="bold bright_blue",
            border_style="grey50",
            padding=(0, 1),
        )
        summary.add_column("SCAN METRIC", style="bold white")
        summary.add_column("VALUE", style="bright_cyan", justify="right")
        summary.add_row("Runtime", f"{elapsed:.2f} sec")

        results = analysis.get("results")
        if isinstance(results, (dict, list, tuple, set)):
            summary.add_row("Results collected", str(len(results)))

        failed = analysis.get("failed_hosts")
        if isinstance(failed, (dict, list, tuple, set)):
            summary.add_row("Failed targets", str(len(failed)))

        console.print(
            Panel(
                summary,
                title=f"[bold green]✓ {module.upper()} COMPLETE[/bold green]",
                border_style="green",
                box=box.ROUNDED,
                padding=(0, 2),
            )
        )


def print_summary(
    pipeline: list[str],
    elapsed: float,
    quiet: bool,
) -> None:


    if quiet:

        return

    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="bold bright_blue", justify="right")
    summary.add_column(style="white")
    summary.add_row("Modules", str(len(pipeline)))
    summary.add_row("Runtime", f"{elapsed:.2f} sec")
    summary.add_row("Output", "output/")

    console.print(
        Panel(
            summary,
            title="[bold green]✓ RECON COMPLETE[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )


def print_performance_summary(
    context: ExecutionContext,
    quiet: bool,
) -> None:


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


def cleanup(
    context: ExecutionContext,
    session: Any,
    thread_pool: ThreadPoolExecutor,
) -> None:


    plugin_manager.shutdown()

    thread_pool.shutdown(
        wait=True,
    )

    session.close()

    context.clear()


def main() -> None:


    arguments = parse_arguments()

    config = build_config(
        arguments,
    )

    pipeline = build_pipeline(
        config,
    )

    if not config["quiet"]:

        show_banner(
            target=config["target"],
            module_count=len(pipeline),
        )

    (
        context,
        session,
        thread_pool,
    ) = create_context(
        config,
    )


    context.performance.start()


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


        framework_elapsed = context.performance.stop()


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
            pipeline=pipeline,
            elapsed=framework_elapsed,
            quiet=config["quiet"],
        )

        print_performance_summary(
            context=context,
            quiet=config["quiet"],
        )

    finally:

        cleanup(
            context=context,
            session=session,
            thread_pool=thread_pool,
        )


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


__all__ = [
    "main",
    "create_context",
    "execute_pipeline_module",
    "print_summary",
    "print_performance_summary",
    "cleanup",
]
