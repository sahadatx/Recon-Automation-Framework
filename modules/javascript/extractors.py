"""
JavaScript Extractors

Generic extraction functions used by the
JavaScript Analysis module.
"""

from __future__ import annotations

import re

from urllib.parse import (
    urlparse,
)

from modules.javascript.string_filters import (
    filter_strings,
)

# ==========================================================
# Regex Patterns
# ==========================================================

URL_PATTERN = re.compile(
    r"""
    (?:
        https?://[^\s"'<>]+
        |
        //[^\s"'<>]+
        |
        /[A-Za-z0-9_\-./?=&%]+
    )
    """,
    re.VERBOSE,
)

COMMENT_PATTERN = re.compile(
    r"""
    (?:
        (?<!:)
        //[^\r\n]*
        |
        /\*
        [\s\S]*?
        \*/
    )
    """,
    re.VERBOSE,
)

STRING_PATTERN = re.compile(
    r"""
    (?P<quote>["'])
    (
        (?:
            \\\\.|
            (?! (?P=quote) ).
        )*
    )
    (?P=quote)
    """,
    re.VERBOSE | re.DOTALL,
)

SOURCEMAP_PATTERN = re.compile(
    r"""
    [A-Za-z0-9_\-./]+\.map
    """,
    re.IGNORECASE,
)


# ==========================================================
# URL Validation
# ==========================================================


def is_valid_url(
    url: str,
) -> bool:
    """
    Validate extracted URL.

    Returns:
        bool
    """

    if not url:

        return False

    url = url.strip()

    if url.startswith("/"):

        return True

    if url.startswith("//"):

        return False

    try:

        parsed = urlparse(url)

    except ValueError:

        return False

    return parsed.scheme in {
        "http",
        "https",
    } and bool(parsed.netloc)


# ==========================================================
# Normalize Values
# ==========================================================


def normalize(
    items: list,
) -> list:
    """
    Normalize extracted values.

    Returns:
        list
    """

    return sorted({str(item).strip() for item in items if item and str(item).strip()})


# ==========================================================
# Extract URLs
# ==========================================================


def extract_urls(
    content: str,
) -> list[str]:
    """
    Extract valid URLs.

    Returns:
        list[str]
    """

    return normalize([url for url in URL_PATTERN.findall(content) if is_valid_url(url)])


# ==========================================================
# Extract Comments
# ==========================================================


def extract_comments(
    content: str,
) -> list[str]:
    """
    Extract JavaScript comments.

    Returns:
        list[str]
    """

    comments: list[str] = []

    for match in COMMENT_PATTERN.finditer(content):

        value = match.group(0).strip()

        if value:

            comments.append(value)

    return normalize(comments)


# ==========================================================
# Extract Strings
# ==========================================================


def extract_strings(
    content: str,
) -> list[str]:
    """
    Extract quoted strings.

    Returns:
        list[str]
    """

    strings: list[str] = []

    for match in STRING_PATTERN.finditer(content):

        value = match.group(2).strip()

        if value:

            strings.append(value)

    return filter_strings(normalize(strings))


# ==========================================================
# Extract Source Maps
# ==========================================================


def extract_source_maps(
    content: str,
) -> list[str]:
    """
    Extract source maps.

    Returns:
        list[str]
    """

    return normalize(SOURCEMAP_PATTERN.findall(content))


# ==========================================================
# Generate Statistics
# ==========================================================


def generate_statistics(
    urls: list[str],
    comments: list[str],
    strings: list[str],
    source_maps: list[str],
) -> dict:
    """
    Generate parser statistics.

    Returns:
        dict
    """

    return {
        "urls": len(urls),
        "comments": len(comments),
        "strings": len(strings),
        "source_maps": len(source_maps),
    }


# ==========================================================
# Parse Content
# ==========================================================


def parse_content(
    content: str,
) -> dict:
    """
    Parse JavaScript content.

    Returns:
        dict
    """

    urls = extract_urls(content)

    comments = extract_comments(content)

    strings = extract_strings(content)

    source_maps = extract_source_maps(content)

    return {
        "urls": urls,
        "comments": comments,
        "strings": strings,
        "source_maps": source_maps,
        "statistics": generate_statistics(
            urls,
            comments,
            strings,
            source_maps,
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "extract_urls",
    "extract_comments",
    "extract_strings",
    "extract_source_maps",
    "generate_statistics",
    "parse_content",
]
