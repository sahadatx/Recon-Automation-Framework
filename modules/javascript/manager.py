"""
JavaScript Manager

Coordinates JavaScript analysis workflow.
"""

from __future__ import annotations

import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from config.config import (
    MAX_WORKERS,
)

from core.logger import (
    info,
    success,
    warning,
    progress_status,
)

from modules.javascript.helpers import (
    is_valid_url,
)

from modules.javascript.downloader import (
    download_one,
)

from modules.javascript.parser import (
    parse_file,
)

from modules.javascript.detectors import (
    scan_content,
)

from modules.javascript.interesting import (
    detect_interesting,
)

from modules.javascript.analyzer import (
    analyze,
)

from modules.javascript.exporter import (
    export_all,
    show_summary,
)


# ==========================================================
# Process One JavaScript
# ==========================================================

def process_javascript(
    url: str,
) -> tuple[str, dict | None]:
    """
    Download and analyze one JavaScript file.

    Returns:
        tuple(
            url,
            metadata | None,
        )
    """

    if not is_valid_url(url):

        warning(
            f"Invalid JavaScript URL: {url}"
        )

        return (
            url,
            None,
        )

    metadata = download_one(
        url
    )

    if metadata is None:

        return (
            url,
            None,
        )

    filepath = metadata.get(
        "path"
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

    # ------------------------------------------------------
    # Parse JavaScript
    # ------------------------------------------------------

    try:

        analysis = parse_file(
            filepath
        )

    except Exception as error:

        warning(
            f"Parse failed: {filepath} ({error})"
        )

        analysis = None

    metadata["analysis"] = analysis

    # ------------------------------------------------------
    # Interesting Detection
    # ------------------------------------------------------

    try:

        metadata["interesting"] = (
            detect_interesting(
                analysis.get(
                    "urls",
                    [],
                )
            )
            if analysis
            else None
        )

    except Exception as error:

        warning(
            f"Interesting detection failed: {filepath} ({error})"
        )

        metadata["interesting"] = None

    # ------------------------------------------------------
    # Secret Detection
    # ------------------------------------------------------

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            content = file.read()

    except Exception as error:

        warning(
            f"{filepath}: {error}"
        )

        content = ""

    try:

        metadata["secrets"] = (
            scan_content(
                content
            )
            if content
            else None
        )

    except Exception as error:

        warning(
            f"Secret detection failed: {filepath} ({error})"
        )

        metadata["secrets"] = None

    return (
        url,
        metadata,
    )

# ==========================================================
# Collect Results
# ==========================================================

def collect_results(
    javascript_urls: list[str],
) -> tuple[
    dict,
    list[str],
    float,
]:
    """
    Download and analyze all
    JavaScript files.

    Returns:
        tuple(
            results,
            failed,
            elapsed,
        )
    """

    info(
        "Starting JavaScript analysis..."
    )

    javascript_urls = sorted(
        {
            url
            for url in javascript_urls
            if is_valid_url(url)
        }
    )

    if not javascript_urls:

        warning(
            "No valid JavaScript URLs found."
        )

        return (
            {},
            [],
            0.0,
        )

    results: dict = {}

    failed: list[str] = []

    total = len(
        javascript_urls
    )

    completed = 0

    start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = {

            executor.submit(
                process_javascript,
                url,
            ): url

            for url
            in javascript_urls

        }

        for future in as_completed(
            futures
        ):

            url = futures[
                future
            ]

            completed += 1

            try:

                js_url, metadata = (
                    future.result()
                )

            except Exception as error:

                warning(
                    f"{url}: {error}"
                )

                failed.append(
                    url
                )

                progress_status(

                    completed,

                    total,

                    f"✗ {url}",

                )

                continue

            if metadata is None:

                failed.append(
                    js_url
                )

                progress_status(

                    completed,

                    total,

                    f"✗ {js_url}",

                )

                continue

            results[
                js_url
            ] = metadata

            progress_status(

                completed,

                total,

                f"✓ {js_url}",

            )

    elapsed = round(

        time.perf_counter()

        - start,

        2,

    )

    return (

        results,

        failed,

        elapsed,

    )

# ==========================================================
# Run JavaScript Analysis
# ==========================================================

def run(
    javascript_urls: list[str],
) -> dict:
    """
    Run JavaScript analysis pipeline.

    Workflow

        Download
            ↓
        Parse
            ↓
        Interesting Detection
            ↓
        Secret Detection
            ↓
        Analyze
            ↓
        Export
            ↓
        Summary
    """

    results, failed, elapsed = (
        collect_results(
            javascript_urls
        )
    )

    analysis = analyze(

        results=results,

        elapsed=elapsed,

    )

    analysis["failed"] = failed

    export_all(
        analysis
    )

    show_summary(
        analysis
    )

    success(

        f"Processed "
        f"{analysis['processed_files']} "
        f"JavaScript file(s)."

    )

    if failed:

        warning(

            f"Failed "
            f"{len(failed)} "
            f"JavaScript file(s)."

        )

    return analysis


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "process_javascript",

    "collect_results",

    "run",

]