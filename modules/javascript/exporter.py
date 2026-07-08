"""
JavaScript Extractors

Generic extraction functions for
JavaScript analysis.
"""

import re


# ==========================================================
# URL Pattern
# ==========================================================

URL_PATTERN = re.compile(

    r"""(?:
        https?://[^\s"'<>]+
        |
        /[A-Za-z0-9_\-./?=&%]+
    )""",

    re.VERBOSE,

)


# ==========================================================
# Source Map Pattern
# ==========================================================

SOURCEMAP_PATTERN = re.compile(

    r"""[A-Za-z0-9_\-./]+\.map""",

    re.IGNORECASE,

)


# ==========================================================
# String Pattern
# ==========================================================

STRING_PATTERN = re.compile(

    r"""["']([^"'\\]{4,})["']"""

)


# ==========================================================
# Comment Pattern
# ==========================================================

COMMENT_PATTERN = re.compile(

    r"""//.*?$|/\*.*?\*/""",

    re.MULTILINE | re.DOTALL,

)


# ==========================================================
# Normalize
# ==========================================================

def normalize(
    items,
):
    """
    Normalize extracted values.

    Returns:
        list
    """

    cleaned = set()

    for item in items:

        item = item.strip()

        if not item:

            continue

        cleaned.add(
            item
        )

    return sorted(
        cleaned
    )


# ==========================================================
# Extract URLs
# ==========================================================

def extract_urls(
    content: str,
):
    """
    Extract URLs from JavaScript.

    Returns:
        list
    """

    urls = URL_PATTERN.findall(
        content
    )

    return normalize(
        urls
    )


# ==========================================================
# Extract Comments
# ==========================================================

def extract_comments(
    content: str,
):
    """
    Extract JavaScript comments.

    Returns:
        list
    """

    comments = COMMENT_PATTERN.findall(
        content
    )

    return normalize(
        comments
    )


# ==========================================================
# Extract Strings
# ==========================================================

def extract_strings(
    content: str,
):
    """
    Extract quoted strings.

    Returns:
        list
    """

    strings = STRING_PATTERN.findall(
        content
    )

    return normalize(
        strings
    )


# ==========================================================
# Extract Source Maps
# ==========================================================

def extract_source_maps(
    content: str,
):
    """
    Extract source map references.

    Returns:
        list
    """

    maps = SOURCEMAP_PATTERN.findall(
        content
    )

    return normalize(
        maps
    )