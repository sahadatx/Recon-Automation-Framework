from collections import Counter

from config.config import VHOST_FILTER_DEFAULT_RESPONSES


DEFAULT_STATUS_CODES = {
    200,
    204,
    301,
    302,
    307,
    401,
    403,
}


def remove_duplicates(
    results: list,
):


    unique = {}

    for result in results:

        host = result.get(
            "host",
            "",
        )

        if host:

            unique[host] = result

    return list(unique.values())


def filter_status_codes(
    results: list,
    allowed=None,
):


    if allowed is None:

        allowed = DEFAULT_STATUS_CODES

    return [
        result
        for result in results
        if result.get(
            "status",
            0,
        )
        in allowed
    ]


def remove_invalid(
    results: list,
):


    return [
        result
        for result in results
        if result.get(
            "host",
            "",
        )
    ]


def remove_empty(
    results: list,
):


    return [
        result
        for result in results
        if result.get(
            "length",
            0,
        )
        > 0
    ]


def remove_redirect_loops(
    results: list,
):


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

        if redirect and redirect == url:

            continue

        filtered.append(result)

    return filtered


def remove_default_responses(
    results: list,
):


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

    if count < (len(results) // 2):

        return results

    return [
        result
        for result in results
        if result.get(
            "length",
            0,
        )
        != length
    ]


def apply_filters(
    results: list,
):


    results = remove_duplicates(results)

    results = filter_status_codes(results)

    results = remove_invalid(results)

    results = remove_empty(results)

    results = remove_redirect_loops(results)

    if VHOST_FILTER_DEFAULT_RESPONSES:

        results = remove_default_responses(results)

    return results
