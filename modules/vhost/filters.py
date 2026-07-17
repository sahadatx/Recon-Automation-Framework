"""
Virtual Host Discovery Filters

Filters false positives and
normalizes ffuf results.
"""

from collections import Counter

from config.config import (

    VHOST_FILTER_DEFAULT_RESPONSES,

)


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

}


# ==========================================================
# Remove Duplicate Hosts
# ==========================================================

def remove_duplicates(
    results: list,
):
    """
    Remove duplicate
    virtual hosts.
    """

    unique = {}

    for result in results:

        host = result.get(

            "host",

            "",

        )

        if host:

            unique[
                host
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
    Keep allowed
    HTTP status codes.
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
# Remove Invalid Hosts
# ==========================================================

def remove_invalid(
    results: list,
):
    """
    Remove empty hosts.
    """

    return [

        result

        for result in results

        if result.get(

            "host",

            "",

        )

    ]


# ==========================================================
# Remove Empty Responses
# ==========================================================

def remove_empty(
    results: list,
):
    """
    Remove zero-length
    responses.
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
# Remove Redirect Loops
# ==========================================================

def remove_redirect_loops(
    results: list,
):
    """
    Remove self redirects.
    """

    filtered = []

    for result in results:

        url = result.get(

            "url",

            "",

        )

        redirect = result.get(

            "redirect",

            "",

        )

        if (

            redirect

            and

            redirect == url

        ):

            continue

        filtered.append(

            result

        )

    return filtered


# ==========================================================
# Remove Default Responses
# ==========================================================

def remove_default_responses(
    results: list,
):
    """
    Remove dominant default
    responses.

    A response length is removed
    only if it represents at least
    50% of all responses.
    """

    if len(results) < 5:

        return results

    counter = Counter(

        result.get(

            "length",

            0,

        )

        for result in results

    )

    length, count = counter.most_common(1)[0]

    if count < (

        len(results) // 2

    ):

        return results

    return [

        result

        for result in results

        if result.get(

            "length",

            0,

        ) != length

    ]


# ==========================================================
# Apply Filters
# ==========================================================

def apply_filters(
    results: list,
):
    """
    Apply all filters.
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

    results = remove_empty(

        results

    )

    results = remove_redirect_loops(

        results

    )

    if VHOST_FILTER_DEFAULT_RESPONSES:

        results = remove_default_responses(

            results

        )

    return results