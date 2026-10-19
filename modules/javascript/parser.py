from __future__ import annotations

from pathlib import Path

from core.logger import debug, warning
from modules.javascript.endpoints import extract_endpoints
from modules.javascript.extractors import (
    extract_comments,
    extract_source_maps,
    extract_strings,
    extract_urls,
    generate_statistics,
)


def read_javascript(
    filepath: str | Path,
) -> str | None:


    path = Path(filepath)

    if not path.exists():

        warning(f"File not found: {path}")

        return None

    try:

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    except Exception as error:

        warning(f"{path}: {error}")

        return None


def parse_file(
    filepath: str | Path,
) -> dict | None:


    debug(f"Parsing {filepath}")

    content = read_javascript(filepath)

    if content is None:

        return None


    try:

        urls = extract_urls(content)

    except Exception as error:

        warning(f"{filepath}: URL extraction failed ({error})")

        urls = []


    try:

        comments = extract_comments(content)

    except Exception as error:

        warning(f"{filepath}: Comment extraction failed ({error})")

        comments = []


    try:

        strings = extract_strings(content)

    except Exception as error:

        warning(f"{filepath}: String extraction failed ({error})")

        strings = []


    try:

        source_maps = extract_source_maps(content)

    except Exception as error:

        warning(f"{filepath}: Source map extraction failed ({error})")

        source_maps = []


    try:

        endpoints = extract_endpoints(urls)

    except Exception as error:

        warning(f"{filepath}: Endpoint extraction failed ({error})")

        endpoints = []

    statistics = generate_statistics(
        urls,
        comments,
        strings,
        source_maps,
    )

    statistics["endpoints"] = len(endpoints)

    return {
        "file": str(filepath),
        "urls": urls,
        "comments": comments,
        "strings": strings,
        "source_maps": source_maps,
        "endpoints": endpoints,
        "statistics": statistics,
    }


def parse_multiple(
    files: list[str | Path],
) -> tuple[
    dict[str, dict],
    list[str | Path],
]:


    results: dict[str, dict] = {}

    failed: list[str | Path] = []

    for filepath in files:

        parsed = parse_file(filepath)

        if parsed is None:

            failed.append(filepath)

            continue

        results[str(filepath)] = parsed

    return (
        results,
        failed,
    )


def parse_javascript(
    files: list[str | Path],
) -> tuple[
    dict[str, dict],
    list[str | Path],
]:


    return parse_multiple(files)


__all__ = [
    "read_javascript",
    "parse_file",
    "parse_multiple",
    "parse_javascript",
]
