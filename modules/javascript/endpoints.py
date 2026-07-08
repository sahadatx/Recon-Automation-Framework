"""
JavaScript Endpoint Discovery

Filters interesting endpoints extracted
from JavaScript files.
"""

import re


# ==========================================================
# Interesting Endpoint Keywords
# ==========================================================

INTERESTING_KEYWORDS = (

    "/api",
    "/v1",
    "/v2",
    "/v3",

    "/graphql",

    "/auth",
    "/login",
    "/logout",
    "/register",
    "/signup",

    "/admin",
    "/dashboard",

    "/upload",
    "/download",

    "/user",
    "/users",

    "/account",
    "/profile",

    "/oauth",
    "/token",

    "/config",
    "/settings",

    "/search",

    "/internal",

    "/debug",

)


# ==========================================================
# Normalize Endpoint
# ==========================================================

def normalize_endpoint(
    endpoint: str,
):
    """
    Normalize endpoint.

    Returns:
        str
    """

    endpoint = endpoint.strip()

    if not endpoint:

        return ""

    endpoint = endpoint.split("?")[0]

    endpoint = endpoint.split("#")[0]

    endpoint = endpoint.rstrip("/")

    return endpoint


# ==========================================================
# Interesting Endpoint Check
# ==========================================================

def is_interesting(
    endpoint: str,
):
    """
    Check whether endpoint is interesting.

    Returns:
        bool
    """

    endpoint = endpoint.lower()

    return any(

        keyword in endpoint

        for keyword

        in INTERESTING_KEYWORDS

    )


# ==========================================================
# Filter Endpoints
# ==========================================================

def filter_endpoints(
    urls: list[str],
):
    """
    Filter interesting endpoints.

    Returns:
        list
    """

    endpoints = set()

    for url in urls:

        endpoint = normalize_endpoint(
            url
        )

        if not endpoint:

            continue

        if is_interesting(
            endpoint
        ):

            endpoints.add(
                endpoint
            )

    return sorted(
        endpoints
    )


# ==========================================================
# API Endpoint Detection
# ==========================================================

def detect_api_versions(
    urls: list[str],
):
    """
    Detect versioned APIs.

    Returns:
        list
    """

    pattern = re.compile(

        r"/v\d+(?:/|$)",

        re.IGNORECASE,

    )

    apis = set()

    for url in urls:

        if pattern.search(
            url
        ):

            apis.add(
                normalize_endpoint(
                    url
                )
            )

    return sorted(
        apis
    )


# ==========================================================
# GraphQL Detection
# ==========================================================

def detect_graphql(
    urls: list[str],
):
    """
    Detect GraphQL endpoints.

    Returns:
        list
    """

    graphql = {

        normalize_endpoint(url)

        for url in urls

        if "graphql"

        in url.lower()

    }

    return sorted(
        graphql
    )


# ==========================================================
# Entry Point
# ==========================================================

def extract_endpoints(
    urls: list[str],
):
    """
    Extract interesting endpoints.

    Returns:
        list
    """

    endpoints = set()

    endpoints.update(

        filter_endpoints(
            urls
        )

    )

    endpoints.update(

        detect_api_versions(
            urls
        )

    )

    endpoints.update(

        detect_graphql(
            urls
        )

    )

    return sorted(
        endpoints
    )