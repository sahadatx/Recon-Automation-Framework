from __future__ import annotations

import re


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


def normalize_endpoint(
    endpoint: str,
) -> str:


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


def is_interesting(
    endpoint: str,
) -> bool:


    endpoint = endpoint.lower()

    return any(keyword in endpoint for keyword in INTERESTING_KEYWORDS)


def filter_endpoints(
    urls: list[str],
) -> list[str]:


    endpoints: set[str] = set()

    for url in urls:

        endpoint = normalize_endpoint(url)

        if not endpoint:

            continue

        if is_interesting(endpoint):

            endpoints.add(endpoint)

    return sorted(endpoints)


def detect_api_versions(
    urls: list[str],
) -> list[str]:


    pattern = re.compile(
        r"/v\d+(?:/|$)",
        re.IGNORECASE,
    )

    apis = {normalize_endpoint(url) for url in urls if pattern.search(url)}

    return sorted(apis)


def detect_graphql(
    urls: list[str],
) -> list[str]:


    graphql = {normalize_endpoint(url) for url in urls if "graphql" in url.lower()}

    return sorted(graphql)


def extract_endpoints(
    urls: list[str],
) -> list[str]:


    endpoints: set[str] = set()

    endpoints.update(filter_endpoints(urls))

    endpoints.update(detect_api_versions(urls))

    endpoints.update(detect_graphql(urls))

    return sorted(endpoints)


__all__ = [
    "INTERESTING_KEYWORDS",
    "normalize_endpoint",
    "is_interesting",
    "filter_endpoints",
    "detect_api_versions",
    "detect_graphql",
    "extract_endpoints",
]
