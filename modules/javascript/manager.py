"""
JavaScript Manager

Coordinates JavaScript download,
parsing and security analysis.
"""

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


# ==========================================================
# Process One JavaScript
# ==========================================================

def process_javascript(
    url: str,
):
    """
    Download and analyze one JavaScript file.

    Args:
        url:
            JavaScript URL.

    Returns:
        tuple(
            url,
            metadata | None,
        )
    """

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

        metadata.update({

            "analysis": None,

            "interesting": None,

            "secrets": None,

        })

        return (

            url,

            metadata,

        )

    # ------------------------------------------------------
    # Parse JavaScript
    # ------------------------------------------------------

    analysis = parse_file(
        filepath
    )

    if analysis is None:

        metadata.update({

            "analysis": None,

            "interesting": None,

            "secrets": None,

        })

        return (

            url,

            metadata,

        )

    metadata[
        "analysis"
    ] = analysis

    # ------------------------------------------------------
    # Interesting Files
    # ------------------------------------------------------

    metadata[
        "interesting"
    ] = detect_interesting(

        analysis.get(
            "urls",
            [],
        )

    )

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

    metadata[
        "secrets"
    ] = (

        scan_content(
            content
        )

        if content

        else None

    )

    return (

        url,

        metadata,

    )


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    results: dict,
):
    """
    Generate overall statistics.

    Args:
        results:
            JavaScript analysis results.

    Returns:
        dict
    """

    stats = {

        "javascript": len(
            results
        ),

        "urls": 0,

        "comments": 0,

        "strings": 0,

        "source_maps": 0,

        "endpoints": 0,

        "interesting_files": 0,

        "interesting_directories": 0,

        "secret_types": 0,

        "total_secrets": 0,

    }

    for metadata in results.values():

        analysis = metadata.get(
            "analysis"
        ) or {}

        parser_stats = analysis.get(
            "statistics",
            {},
        )

        for key in (

            "urls",

            "comments",

            "strings",

            "source_maps",

            "endpoints",

        ):

            stats[key] += parser_stats.get(
                key,
                0,
            )

        interesting = metadata.get(
            "interesting"
        ) or {}

        interesting_stats = interesting.get(
            "statistics",
            {},
        )

        stats["interesting_files"] += interesting_stats.get(
            "interesting_files",
            0,
        )

        stats["interesting_directories"] += interesting_stats.get(
            "interesting_directories",
            0,
        )

        secrets = metadata.get(
            "secrets"
        ) or {}

        secret_stats = secrets.get(
            "statistics",
            {},
        )

        stats["secret_types"] += secret_stats.get(
            "secret_types",
            0,
        )

        stats["total_secrets"] += secret_stats.get(
            "total_secrets",
            0,
        )

    return stats

# ==========================================================
# Download & Analyze
# ==========================================================

def download_javascript(
    javascript_urls: list[str],
):
    """
    Download and analyze JavaScript files.

    Args:
        javascript_urls:
            List of JavaScript URLs.

    Returns:
        tuple(
            results,
            failed,
            elapsed,
        )
    """

    info(
        "Starting JavaScript Analysis..."
    )

    javascript_urls = sorted(
        set(
            javascript_urls
        )
    )

    if not javascript_urls:

        warning(
            "No JavaScript files found."
        )

        return (

            {},

            [],

            0.0,

        )

    results = {}

    failed = []

    completed = 0

    total = len(
        javascript_urls
    )

    start_time = time.perf_counter()

    with ThreadPoolExecutor(

        max_workers=MAX_WORKERS,

    ) as executor:

        futures = {

            executor.submit(

                process_javascript,

                url,

            ): url

            for url in javascript_urls

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

                if metadata:

                    results[
                        js_url
                    ] = metadata

                    progress_status(

                        completed,

                        total,

                        f"✓ {js_url}",

                    )

                else:

                    failed.append(
                        js_url
                    )

                    progress_status(

                        completed,

                        total,

                        f"✗ {js_url}",

                    )

            except Exception as error:

                failed.append(
                    url
                )

                warning(
                    f"{url}: {error}"
                )

                progress_status(

                    completed,

                    total,

                    f"✗ {url}",

                )

    elapsed = round(

        time.perf_counter()

        - start_time,

        2,

    )

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    statistics = generate_statistics(
        results
    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    success(
        f"JavaScript Files        : {statistics['javascript']}"
    )

    success(
        f"Failed Downloads        : {len(failed)}"
    )

    success(
        f"URLs Found              : {statistics['urls']}"
    )

    success(
        f"Endpoints               : {statistics['endpoints']}"
    )

    success(
        f"Comments                : {statistics['comments']}"
    )

    success(
        f"Strings                 : {statistics['strings']}"
    )

    success(
        f"Source Maps             : {statistics['source_maps']}"
    )

    success(
        f"Interesting Files       : {statistics['interesting_files']}"
    )

    success(
        f"Interesting Directories : {statistics['interesting_directories']}"
    )

    success(
        f"Secret Types            : {statistics['secret_types']}"
    )

    success(
        f"Secrets Found           : {statistics['total_secrets']}"
    )

    success(
        f"Elapsed                 : {elapsed:.2f} sec"
    )

    return (

        results,

        failed,

        elapsed,

    )