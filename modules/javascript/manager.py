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


# ==========================================================
# Process One JavaScript
# ==========================================================

def process_javascript(
    url: str,
):
    """
    Download and analyze one
    JavaScript file.

    Returns:
        tuple(
            url,
            metadata | None,
        )
    """

    if not is_valid_url(

        url

    ):

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

            f"Parse failed: "

            f"{filepath} ({error})"

        )

        analysis = None

    if analysis is None:

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

        )

    except Exception as error:

        warning(

            f"Interesting detection failed: "

            f"{filepath} ({error})"

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

            f"Secret detection failed: "

            f"{filepath} ({error})"

        )

        metadata["secrets"] = None

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
    Generate overall JavaScript
    analysis statistics.

    Args:
        results:
            JavaScript analysis results.

    Returns:
        dict
    """

    statistics = {

        "processed_files": len(

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

        if not metadata:

            continue

        # --------------------------------------------------
        # Parser Statistics
        # --------------------------------------------------

        analysis = metadata.get(

            "analysis"

        ) or {}

        parser_stats = analysis.get(

            "statistics",

            {},

        )

        statistics["urls"] += parser_stats.get(

            "urls",

            0,

        )

        statistics["comments"] += parser_stats.get(

            "comments",

            0,

        )

        statistics["strings"] += parser_stats.get(

            "strings",

            0,

        )

        statistics["source_maps"] += parser_stats.get(

            "source_maps",

            0,

        )

        statistics["endpoints"] += parser_stats.get(

            "endpoints",

            0,

        )

        # --------------------------------------------------
        # Interesting Statistics
        # --------------------------------------------------

        interesting = metadata.get(

            "interesting"

        ) or {}

        interesting_stats = interesting.get(

            "statistics",

            {},

        )

        statistics["interesting_files"] += (

            interesting_stats.get(

                "interesting_files",

                0,

            )

        )

        statistics["interesting_directories"] += (

            interesting_stats.get(

                "interesting_directories",

                0,

            )

        )

        # --------------------------------------------------
        # Secret Statistics
        # --------------------------------------------------

        secrets = metadata.get(

            "secrets"

        ) or {}

        secret_stats = secrets.get(

            "statistics",

            {},

        )

        statistics["secret_types"] += secret_stats.get(

            "secret_types",

            0,

        )

        statistics["total_secrets"] += secret_stats.get(

            "total_secrets",

            0,

        )

    return statistics




# ==========================================================
# Download & Analyze
# ==========================================================

def download_javascript(
    javascript_urls: list[str],
):
    """
    Download and analyze
    JavaScript files.

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

    # ------------------------------------------------------
    # Remove Duplicates & Invalid URLs
    # ------------------------------------------------------

    javascript_urls = sorted({

        url

        for url in javascript_urls

        if is_valid_url(

            url

        )

    })

    if not javascript_urls:

        warning(

            "No valid JavaScript files found."

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

    # ------------------------------------------------------
    # Thread Pool
    # ------------------------------------------------------

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

                if metadata is not None:

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

        f"Processed Files        : "

        f"{statistics['processed_files']}"

    )

    success(

        f"Failed Files           : "

        f"{len(failed)}"

    )

    success(

        f"URLs Found             : "

        f"{statistics['urls']}"

    )

    success(

        f"Endpoints              : "

        f"{statistics['endpoints']}"

    )

    success(

        f"Comments               : "

        f"{statistics['comments']}"

    )

    success(

        f"Strings                : "

        f"{statistics['strings']}"

    )

    success(

        f"Source Maps            : "

        f"{statistics['source_maps']}"

    )

    success(

        f"Interesting Files      : "

        f"{statistics['interesting_files']}"

    )

    success(

        f"Interesting Directories: "

        f"{statistics['interesting_directories']}"

    )

    success(

        f"Secret Types           : "

        f"{statistics['secret_types']}"

    )

    success(

        f"Secrets Found          : "

        f"{statistics['total_secrets']}"

    )

    success(

        f"Elapsed                : "

        f"{elapsed:.2f} sec"

    )

    return (

        results,

        failed,

        elapsed,

    )