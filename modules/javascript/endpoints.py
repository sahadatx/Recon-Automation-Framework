"""
JavaScript Endpoint Discovery

Filters interesting endpoints extracted
from JavaScript files.
"""

from __future__ import annotations

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
) -> str:
    """
    Normalize an endpoint.

    Returns:
        str
    """

    if not endpoint:

        return ""

    endpoint = endpoint.strip()

    if not endpoint:

        return ""

    endpoint = endpoint.split(
        "?",
        1,
    )[0]

    endpoint = endpoint.split(
        "#",
        1,
    )[0]

    return endpoint.rstrip("/")


# ==========================================================
# Interesting Endpoint Check
# ==========================================================


def is_interesting(
    endpoint: str,
) -> bool:
    """
    Check whether an endpoint
    is interesting.

    Returns:
        bool
    """

    endpoint = endpoint.lower()

    return any(keyword in endpoint for keyword in INTERESTING_KEYWORDS)


# ==========================================================
# Filter Endpoints
# ==========================================================


def filter_endpoints(
    urls: list[str],
) -> list[str]:
    """
    Filter interesting endpoints.

    Returns:
        list[str]
    """

    endpoints: set[str] = set()

    for url in urls:

        endpoint = normalize_endpoint(url)

        if not endpoint:

            continue

        if is_interesting(endpoint):

            endpoints.add(endpoint)

    return sorted(endpoints)


# ==========================================================
# API Version Detection
# ==========================================================


def detect_api_versions(
    urls: list[str],
) -> list[str]:
    """
    Detect versioned API endpoints.

    Returns:
        list[str]
    """

    pattern = re.compile(
        r"/v\d+(?:/|$)",
        re.IGNORECASE,
    )

    apis = {normalize_endpoint(url) for url in urls if pattern.search(url)}

    return sorted(apis)


# ==========================================================
# GraphQL Detection
# ==========================================================


def detect_graphql(
    urls: list[str],
) -> list[str]:
    """
    Detect GraphQL endpoints.

    Returns:
        list[str]
    """

    graphql = {normalize_endpoint(url) for url in urls if "graphql" in url.lower()}

    return sorted(graphql)


# ==========================================================
# Extract Endpoints
# ==========================================================


def extract_endpoints(
    urls: list[str],
) -> list[str]:
    """
    Extract interesting endpoints.

    Returns:
        list[str]
    """

    endpoints: set[str] = set()

    endpoints.update(filter_endpoints(urls))

    endpoints.update(detect_api_versions(urls))

    endpoints.update(detect_graphql(urls))

    return sorted(endpoints)


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "INTERESTING_KEYWORDS",
    "normalize_endpoint",
    "is_interesting",
    "filter_endpoints",
    "detect_api_versions",
    "detect_graphql",
    "extract_endpoints",
]
