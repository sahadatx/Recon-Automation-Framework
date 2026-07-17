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

    generate_statistics,

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
    Read a JavaScript file.

    Returns:
        str | None
    """

    path = Path(filepath)

    if not path.exists():

        warning(

            f"File not found: {path}"

        )

        return None

    try:

        return path.read_text(

            encoding="utf-8",

            errors="ignore",

        )

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

    try:

        urls = extract_urls(

            content

        )

    except Exception as error:

        warning(

            f"{filepath}: URL extraction failed ({error})"

        )

        urls = []

    try:

        comments = extract_comments(

            content

        )

    except Exception as error:

        warning(

            f"{filepath}: Comment extraction failed ({error})"

        )

        comments = []

    try:

        strings = extract_strings(

            content

        )

    except Exception as error:

        warning(

            f"{filepath}: String extraction failed ({error})"

        )

        strings = []

    try:

        source_maps = extract_source_maps(

            content

        )

    except Exception as error:

        warning(

            f"{filepath}: Source map extraction failed ({error})"

        )

        source_maps = []

    try:

        endpoints = extract_endpoints(

            urls

        )

    except Exception as error:

        warning(

            f"{filepath}: Endpoint extraction failed ({error})"

        )

        endpoints = []

    statistics = generate_statistics(

        urls,

        comments,

        strings,

        source_maps,

    )

    statistics["endpoints"] = len(

        endpoints

    )

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

    Returns:
        tuple
    """

    results = {}

    failed = []

    for filepath in files:

        parsed = parse_file(

            filepath

        )

        if parsed is None:

            failed.append(

                filepath

            )

            continue

        results[

            filepath

        ] = parsed

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
    """

    return parse_multiple(

        files

    )