"""
JavaScript Extractors

Generic extraction functions used by the
JavaScript Analysis module.
"""

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
    r'''
    (?P<quote>["'])
    (
        (?:
            \\\\.|
            (?! (?P=quote) ).
        )*
    )
    (?P=quote)
    ''',
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
):
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

        parsed = urlparse(

            url

        )

    except ValueError:

        return False

    return (

        parsed.scheme

        in

        {

            "http",

            "https",

        }

        and

        bool(

            parsed.netloc

        )

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

    return sorted(

        {

            str(item).strip()

            for item

            in items

            if item

            and str(item).strip()

        }

    )


# ==========================================================
# Extract URLs
# ==========================================================

def extract_urls(
    content: str,
):
    """
    Extract valid URLs.

    Returns:
        list
    """

    return normalize(

        [

            url

            for url

            in URL_PATTERN.findall(

                content

            )

            if is_valid_url(

                url

            )

        ]

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

    comments = []

    for match in COMMENT_PATTERN.finditer(

        content

    ):

        value = match.group(

            0

        ).strip()

        if value:

            comments.append(

                value

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

    strings = []

    for match in STRING_PATTERN.finditer(

        content

    ):

        value = match.group(

            2

        ).strip()

        if value:

            strings.append(

                value

            )

    strings = normalize(

        strings

    )

    return filter_strings(

        strings

    )


# ==========================================================
# Extract Source Maps
# ==========================================================

def extract_source_maps(
    content: str,
):
    """
    Extract source maps.

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
    Generate statistics.

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