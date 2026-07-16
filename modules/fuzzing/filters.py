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

    201,

    202,

    204,

    301,

    302,

    307,

    308,

    401,

    403,

    405,

    500,

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
    Keep allowed HTTP
    status codes.

    Returns:
        list
    """

    if allowed is None:

        allowed = (
            DEFAULT_STATUS_CODES
        )

    return [

        result

        for result in results

        if result.get(
            "status",
            0,
        ) in allowed

    ]


# ==========================================================
# Remove Invalid Responses
# ==========================================================

def remove_invalid(
    results: list,
):
    """
    Remove invalid
    ffuf responses.

    Responses with a valid
    HTTP status are kept,
    even if response size
    is zero.

    Returns:
        list
    """

    filtered = []

    for result in results:

        if result.get(
            "status",
            0,
        ) == 0:

            continue

        filtered.append(
            result
        )

    return filtered


# ==========================================================
# Filter Extensions
# ==========================================================

def filter_extensions(
    results: list,
    blocked=None,
):
    """
    Remove unwanted
    file extensions.

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

            ".ico",

            ".woff",

            ".woff2",

            ".ttf",

            ".eot",

            ".otf",

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

    results = remove_invalid(
        results
    )

    results = filter_extensions(
        results
    )

    return results