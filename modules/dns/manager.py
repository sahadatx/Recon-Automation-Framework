from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import info, progress_status, success, warning
from modules.dns.analyzer import analyze
from modules.dns.records import resolve_all_records


def resolve_subdomain(
    context: ExecutionContext,
    subdomain: str,
) -> tuple[str, dict[str, list[str]]]:


    if context.has_dns_cache(subdomain):

        return (
            subdomain,
            context.get_dns_cache(
                subdomain,
            ),
        )

    records = resolve_all_records(
        subdomain,
    )

    context.set_dns_cache(
        subdomain,
        records,
    )

    return (
        subdomain,
        records,
    )


def resolve_subdomains(
    context: ExecutionContext,
    subdomains: list[str],
) -> tuple[
    dict[str, dict[str, list[str]]],
    list[str],
]:


    info("Starting DNS Resolution...")

    results: dict[
        str,
        dict[str, list[str]],
    ] = {}

    failed_hosts: list[str] = []

    total = len(
        subdomains,
    )

    completed = 0

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Shared thread pool is not initialized.")

    futures = {
        executor.submit(
            resolve_subdomain,
            context,
            subdomain,
        ): subdomain
        for subdomain in subdomains
    }

    for future in as_completed(
        futures,
    ):

        subdomain = futures[future]

        completed += 1
        failed = False

        try:

            (
                hostname,
                records,
            ) = future.result()

            results[hostname] = records

        except Exception as error:

            failed = True

            warning(f"{subdomain}: {error}")

            failed_hosts.append(
                subdomain,
            )

        status = (
            f"✗ {subdomain} failed"
            if failed
            else f"✓ {subdomain} resolved"
        )

        progress_status(
            completed,
            total,
            status,
        )

    success(f"Resolved {len(results)} hosts.")

    return (
        results,
        sorted(
            failed_hosts,
        ),
    )


def run(
    context: ExecutionContext,
    subdomains: list[str],
) -> dict[str, Any]:


    (
        results,
        failed_hosts,
    ) = resolve_subdomains(
        context,
        subdomains,
    )

    analysis = analyze(
        results=results,
        failed_hosts=failed_hosts,
    )

    context.set_analysis(
        "dns",
        analysis,
    )

    return analysis


__all__ = [
    "run",
]
