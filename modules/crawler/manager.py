from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import info, progress_status, success, warning
from modules.crawler.analyzer import analyze
from modules.crawler.crawler import crawl_host


def crawl_one_host(
    context: ExecutionContext,
    host: str,
) -> tuple[str, dict[str, Any] | None]:


    return (
        host,
        crawl_host(
            context=context,
            host=host,
        ),
    )


def crawl_hosts(
    context: ExecutionContext,
    hosts: list[str],
) -> dict[str, dict[str, Any]]:


    info("Starting URL Crawling...")

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Thread pool not initialized.")

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    completed = 0

    total = len(
        hosts,
    )

    futures = {
        executor.submit(
            crawl_one_host,
            context,
            host,
        ): host
        for host in hosts
    }

    for future in as_completed(
        futures,
    ):

        completed += 1

        host = futures[future]

        try:

            (
                hostname,
                result,
            ) = future.result()

            if result is not None:

                results[hostname] = result

                pages = result["statistics"]["pages"]

                progress_status(
                    completed,
                    total,
                    (f"✓ {hostname} " f"({pages} pages)"),
                )

            else:

                progress_status(
                    completed,
                    total,
                    f"✗ {hostname}",
                )

        except Exception as exception:

            warning(
                f"{host}: {exception}",
            )

            progress_status(
                completed,
                total,
                f"✗ {host}",
            )

    success(
        f"Hosts Crawled : {len(results)}",
    )

    return results


def run(
    context: ExecutionContext,
    hosts: list[str],
) -> dict[str, Any]:


    results = crawl_hosts(
        context=context,
        hosts=hosts,
    )

    analysis = analyze(
        results=results,
    )

    context.set_analysis(
        "crawler",
        analysis,
    )

    return analysis


__all__ = [
    "run",
]
