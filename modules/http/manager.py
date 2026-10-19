from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import info, progress_status, success, warning
from modules.http.analyzer import analyze
from modules.http.probe import probe_host


def probe_one_host(
    context: ExecutionContext,
    host: str,
) -> tuple[
    str,
    dict[str, Any] | None,
]:


    session = context.get_http_session()

    if session is None:

        raise RuntimeError("Shared HTTP session " "is not initialized.")

    return (
        host,
        probe_host(
            session=session,
            host=host,
        ),
    )


def probe_hosts(
    context: ExecutionContext,
    hosts: list[str],
) -> tuple[
    dict[str, dict[str, Any]],
    list[str],
]:


    info("Starting HTTP Probe...")

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed_hosts: list[str] = []

    completed = 0

    total = len(
        hosts,
    )

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Shared thread pool " "is not initialized.")

    futures = {
        executor.submit(
            probe_one_host,
            context,
            host,
        ): host
        for host in hosts
    }

    for future in as_completed(
        futures,
    ):

        host = futures[future]

        completed += 1

        try:

            (
                hostname,
                response,
            ) = future.result()

            if response:

                results[hostname] = response

                progress_status(
                    completed,
                    total,
                    (
                        f"✓ {hostname} "
                        f"({response['status']} "
                        f"{response['scheme'].upper()})"
                    ),
                )

            else:

                failed_hosts.append(
                    hostname,
                )

                progress_status(
                    completed,
                    total,
                    f"✗ {hostname}",
                )

        except Exception as error:

            failed_hosts.append(
                host,
            )

            warning(
                f"{host}: {error}",
            )

            progress_status(
                completed,
                total,
                f"✗ {host}",
            )

    success(f"Alive Hosts : {len(results)}")

    success(f"Dead Hosts  : {len(failed_hosts)}")

    return (
        results,
        sorted(
            failed_hosts,
        ),
    )


def run(
    context: ExecutionContext,
    hosts: list[str],
) -> dict[str, Any]:


    (
        results,
        failed_hosts,
    ) = probe_hosts(
        context,
        hosts,
    )

    analysis = analyze(
        results=results,
        failed_hosts=failed_hosts,
    )

    context.set_analysis(
        "http",
        analysis,
    )

    return analysis


__all__ = [
    "run",
]
