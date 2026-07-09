"""
JavaScript Extractors

Generic extraction functions used by the
JavaScript Analysis module.
"""

import re


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
    //.*?$|
    /\*.*?\*/
    """,
    re.MULTILINE | re.DOTALL,
)

STRING_PATTERN = re.compile(
    r"""
    ["']([^"'\\]{4,})["']
    """,
)

SOURCEMAP_PATTERN = re.compile(
    r"""
    [A-Za-z0-9_\-./]+\.map
    """,
    re.IGNORECASE,
)


# ==========================================================
# Normalize
# ==========================================================

def normalize(items):
    """
    Normalize extracted values.

    Args:
        items:
            Iterable of extracted values.

    Returns:
        list
    """

    cleaned = set()

    for item in items:

        item = item.strip()

        if not item:

            continue

        cleaned.add(item)

    return sorted(cleaned)


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


# ==========================================================
# Statistics
# ==========================================================

def generate_statistics(
    urls: list,
    comments: list,
    strings: list,
    source_maps: list,
):
    """
    Generate extraction statistics.

    Returns:
        dict
    """

    return {

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

    }


# ==========================================================
# Parse Content
# ==========================================================

def parse_content(
    content: str,
):
    """
    Parse JavaScript content.

    Returns:
        dict
    """

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

    statistics = generate_statistics(

        urls,

        comments,

        strings,

        source_maps,

    )

    return {

        "urls": urls,

        "comments": comments,

        "strings": strings,

        "source_maps": source_maps,

        "statistics": statistics,

    }