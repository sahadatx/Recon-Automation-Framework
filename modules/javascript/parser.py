"""
JavaScript Parser

Reads downloaded JavaScript files and
coordinates the extraction pipeline.
"""

from pathlib import Path

from core.logger import (
    debug,
    warning,
)

from modules.javascript.extractors import (
    extract_urls,
    extract_comments,
    extract_strings,
    extract_source_maps,
)

from modules.javascript.endpoints import (
    extract_endpoints,
)


# ==========================================================
# Read JavaScript File
# ==========================================================

def read_javascript(
    filepath: str | Path,
) -> str | None:
    """
    Read JavaScript file.

    Args:
        filepath:
            JavaScript file path.

    Returns:
        File content or None.
    """

    path = Path(
        filepath
    )

    if not path.exists():

        warning(
            f"File not found: {path}"
        )

        return None

    try:

        content = path.read_text(

            encoding="utf-8",

            errors="ignore",

        )

        return content

    except Exception as error:

        warning(
            f"{path}: {error}"
        )

        return None


# ==========================================================
# Parse One File
# ==========================================================

def parse_file(
    filepath: str | Path,
):
    """
    Parse one JavaScript file.

    Args:
        filepath:
            JavaScript file.

    Returns:
        dict | None
    """

    debug(
        f"Parsing {filepath}"
    )

    content = read_javascript(
        filepath
    )

    if content is None:

        return None

    # ------------------------------------------------------
    # Generic Extraction
    # ------------------------------------------------------

    urls = extract_urls(
        content
    )

    comments = extract_comments(
        content
    )

    strings = extract_strings(
        content
    )

    source_maps = extract_source_maps(
        content
    )

    # ------------------------------------------------------
    # Endpoint Discovery
    # ------------------------------------------------------

    endpoints = extract_endpoints(
        urls
    )

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    statistics = {

        "urls": len(
            urls
        ),

        "comments": len(
            comments
        ),

        "strings": len(
            strings
        ),

        "source_maps": len(
            source_maps
        ),

        "endpoints": len(
            endpoints
        ),

    }

    return {

        "file": str(
            filepath
        ),

        "urls": urls,

        "comments": comments,

        "strings": strings,

        "source_maps": source_maps,

        "endpoints": endpoints,

        "statistics": statistics,

    }


# ==========================================================
# Parse Multiple Files
# ==========================================================

def parse_multiple(
    files: list[str],
):
    """
    Parse multiple JavaScript files.

    Args:
        files:
            List of JavaScript files.

    Returns:
        tuple(
            results,
            failed,
        )
    """

    results = {}

    failed = []

    for filepath in files:

        parsed = parse_file(
            filepath
        )

        if parsed:

            results[
                filepath
            ] = parsed

        else:

            failed.append(
                filepath
            )

    return (

        results,

        failed,

    )


# ==========================================================
# Entry Point
# ==========================================================

def parse_javascript(
    files: list[str],
):
    """
    JavaScript parser entry point.

    Args:
        files:
            JavaScript file paths.

    Returns:
        tuple(
            results,
            failed,
        )
    """

    return parse_multiple(
        files
    )