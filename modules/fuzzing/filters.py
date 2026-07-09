"""
Directory Fuzzing Filters

Filters false positives and
normalizes ffuf results.
"""


# ==========================================================
# Default Status Codes
# ==========================================================

DEFAULT_STATUS_CODES = {

    200,

    204,

    301,

    302,

    307,

    401,

    403,

    405,

}


# ==========================================================
# Remove Duplicate URLs
# ==========================================================

def remove_duplicates(
    results: list,
):
    """
    Remove duplicate URLs.

    Returns:
        list
    """

    unique = {}

    for result in results:

        url = result.get(
            "url",
            "",
        )

        if url:

            unique[
                url
            ] = result

    return list(
        unique.values()
    )


# ==========================================================
# Filter Status Codes
# ==========================================================

def filter_status_codes(
    results: list,
    allowed=None,
):
    """
    Keep allowed HTTP status codes.

    Returns:
        list
    """

    if allowed is None:

        allowed = DEFAULT_STATUS_CODES

    return [

        result

        for result in results

        if result.get(
            "status",
            0,
        ) in allowed

    ]


# ==========================================================
# Remove Empty Responses
# ==========================================================

def remove_empty(
    results: list,
):
    """
    Remove empty responses.

    Returns:
        list
    """

    return [

        result

        for result in results

        if result.get(
            "length",
            0,
        ) > 0

    ]


# ==========================================================
# Filter Extensions
# ==========================================================

def filter_extensions(
    results: list,
    blocked=None,
):
    """
    Remove unwanted file extensions.

    Returns:
        list
    """

    if blocked is None:

        blocked = {

            ".png",

            ".jpg",

            ".jpeg",

            ".gif",

            ".svg",

            ".woff",

            ".woff2",

            ".ttf",

            ".ico",

        }

    filtered = []

    for result in results:

        url = result.get(
            "url",
            "",
        ).lower()

        if any(
            url.endswith(
                extension
            )
            for extension in blocked
        ):

            continue

        filtered.append(
            result
        )

    return filtered


# ==========================================================
# Apply Filters
# ==========================================================

def apply_filters(
    results: list,
):
    """
    Apply all filters.

    Returns:
        list
    """

    results = remove_duplicates(
        results
    )

    results = filter_status_codes(
        results
    )

    results = remove_empty(
        results
    )

    results = filter_extensions(
        results
    )

    return results