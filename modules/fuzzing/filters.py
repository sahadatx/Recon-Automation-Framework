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


def remove_duplicates(
    results: list,
):


    unique = {}

    for result in results:

        url = result.get(
            "url",
            "",
        )

        if url:

            unique[url] = result

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


    filtered = []

    for result in results:

        if (
            result.get(
                "status",
                0,
            )
            == 0
        ):

            continue

        filtered.append(result)

    return filtered


def filter_extensions(
    results: list,
    blocked=None,
):


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

        if any(url.endswith(extension) for extension in blocked):

            continue

        filtered.append(result)

    return filtered


def apply_filters(
    results: list,
):


    results = remove_duplicates(results)

    results = filter_status_codes(results)

    results = remove_invalid(results)

    results = filter_extensions(results)

    return results
