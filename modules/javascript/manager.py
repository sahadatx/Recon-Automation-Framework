from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from core.logger import info, progress_status, success, warning
from modules.javascript.analyzer import analyze
from modules.javascript.detectors import scan_content
from modules.javascript.downloader import download_one
from modules.javascript.helpers import is_valid_url
from modules.javascript.interesting import detect_interesting
from modules.javascript.parser import parse_file


def process_javascript(
    context: ExecutionContext,
    url: str,
) -> tuple[str, dict[str, Any] | None]:


    if not is_valid_url(url):

        warning(f"Invalid JavaScript URL: {url}")

        return (
            url,
            None,
        )

    metadata = download_one(
        context,
        url,
    )

    if metadata is None:

        return (
            url,
            None,
        )

    filepath = metadata.get(
        "path",
    )

    if not filepath:

        metadata.update(
            {
                "analysis": None,
                "interesting": None,
                "secrets": None,
            }
        )

        return (
            url,
            metadata,
        )


    try:

        analysis = parse_file(
            filepath,
        )

    except Exception as error:

        warning(f"Parse failed: {filepath} ({error})")

        analysis = None

    metadata["analysis"] = analysis


    try:

        metadata["interesting"] = (
            detect_interesting(
                analysis.get(
                    "urls",
                    [],
                ),
            )
            if analysis
            else None
        )

    except Exception as error:

        warning(("Interesting detection failed: " f"{filepath} ({error})"))

        metadata["interesting"] = None


    try:

        with open(
            filepath,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            content = file.read()

    except Exception as error:

        warning(f"{filepath}: {error}")

        content = ""

    try:

        metadata["secrets"] = (
            scan_content(
                content,
            )
            if content
            else None
        )

    except Exception as error:

        warning(("Secret detection failed: " f"{filepath} ({error})"))

        metadata["secrets"] = None

    return (
        url,
        metadata,
    )


def collect_results(
    context: ExecutionContext,
    javascript_urls: list[str],
) -> tuple[
    dict[str, dict[str, Any]],
    list[str],
]:


    info("Starting JavaScript analysis...")

    javascript_urls = sorted(
        {
            url
            for url in javascript_urls
            if is_valid_url(
                url,
            )
        }
    )

    if not javascript_urls:

        warning("No valid JavaScript URLs found.")

        return (
            {},
            [],
        )

    executor = context.get_thread_pool()

    if executor is None:

        raise RuntimeError("Shared thread pool is not initialized.")

    results: dict[
        str,
        dict[str, Any],
    ] = {}

    failed: list[str] = []

    total = len(
        javascript_urls,
    )

    completed = 0

    futures = {
        executor.submit(
            process_javascript,
            context,
            url,
        ): url
        for url in javascript_urls
    }

    for future in as_completed(
        futures,
    ):

        url = futures[future]

        completed += 1

        try:

            (
                js_url,
                metadata,
            ) = future.result()

        except Exception as error:

            warning(f"{url}: {error}")

            failed.append(
                url,
            )

            progress_status(
                completed,
                total,
                f"✗ {url}",
            )

            continue

        if metadata is None:

            failed.append(
                js_url,
            )

            progress_status(
                completed,
                total,
                f"✗ {js_url}",
            )

            continue

        results[js_url] = metadata

        progress_status(
            completed,
            total,
            f"✓ {js_url}",
        )

    success(f"Processed {len(results)} JavaScript file(s).")

    return (
        results,
        sorted(
            failed,
        ),
    )


def run(
    context: ExecutionContext,
    javascript_urls: list[str],
) -> dict[str, Any]:


    (
        results,
        failed,
    ) = collect_results(
        context,
        javascript_urls,
    )

    analysis = analyze(
        results=results,
    )

    analysis["failed"] = failed

    context.set_analysis(
        "javascript",
        analysis,
    )

    if failed:

        warning("Failed " f"{len(failed)} " "JavaScript file(s).")

    return analysis


__all__ = [
    "process_javascript",
    "collect_results",
    "run",
]
