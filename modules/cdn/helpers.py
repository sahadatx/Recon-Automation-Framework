"""
CDN Helpers

Reusable helper functions for
CDN Detection.
"""

from __future__ import annotations

import socket

from copy import deepcopy
from typing import Any
from urllib.parse import urlparse

import dns.resolver
import requests

from config.config import HTTP_TIMEOUT

from .constants import (
    DEFAULT_ANALYSIS,
    DEFAULT_HEADERS,
)


# ==========================================================
# Default Result
# ==========================================================

EMPTY_CDN_RESULT = deepcopy(

    DEFAULT_ANALYSIS

)


# ==========================================================
# Normalize Target
# ==========================================================

def normalize_target(
    target: str,
):
    """
    Normalize target into
    hostname.

    Returns:
        str
    """

    if not target:

        return ""

    target = target.strip()

    if "://" not in target:

        target = f"https://{target}"

    parsed = urlparse(

        target,

    )

    return parsed.hostname or ""


# ==========================================================
# Resolve IPv4
# ==========================================================

def resolve_ipv4(
    host: str,
):
    """
    Resolve IPv4 address.

    Returns:
        str | None
    """

    try:

        return socket.gethostbyname(

            host,

        )

    except Exception:

        return None


# ==========================================================
# HTTP Request
# ==========================================================

def request_headers(
    target: str,
):
    """
    Send HTTP request.

    Returns:
        requests.Response | None
    """

    try:

        response = requests.get(

            target,

            headers=DEFAULT_HEADERS,

            timeout=HTTP_TIMEOUT,

            allow_redirects=True,

        )

        return response

    except Exception:

        return None


# ==========================================================
# Response Headers
# ==========================================================

def extract_headers(
    response,
):
    """
    Extract response headers.

    Returns:
        dict
    """

    if response is None:

        return {}

    return dict(

        response.headers

    )


# ==========================================================
# DNS CNAME
# ==========================================================

def resolve_cname(
    host: str,
):
    """
    Resolve CNAME record.

    Returns:
        str | None
    """

    try:

        answers = dns.resolver.resolve(

            host,

            "CNAME",

        )

        return str(

            answers[0].target

        ).rstrip(".")

    except Exception:

        return None


# ==========================================================
# Header Exists
# ==========================================================

def header_exists(
    headers: dict[str, Any],
    header: str,
):
    """
    Check whether a header
    exists.

    Returns:
        bool
    """

    return (

        header.lower()

        in

        {

            key.lower()

            for key in headers

        }

    )


# ==========================================================
# Server Header
# ==========================================================

def get_server_header(
    headers: dict[str, Any],
):
    """
    Extract Server header.

    Returns:
        str
    """

    for key, value in headers.items():

        if key.lower() == "server":

            return str(

                value,

            )

    return ""


# ==========================================================
# Cache Headers
# ==========================================================

def get_cache_headers(
    headers: dict[str, Any],
):
    """
    Extract cache-related
    headers.

    Returns:
        dict
    """

    cache_headers = {}

    for key, value in headers.items():

        key_lower = key.lower()

        if (

            "cache" in key_lower

            or

            key_lower == "age"

            or

            key_lower == "via"

        ):

            cache_headers[key] = value

    return cache_headers


# ==========================================================
# Safe Lower
# ==========================================================

def safe_lower(
    value: Any,
):
    """
    Safely convert value
    to lowercase string.

    Returns:
        str
    """

    if value is None:

        return ""

    return str(

        value,

    ).lower()


# ==========================================================
# Merge Detection Methods
# ==========================================================

def merge_methods(
    *methods,
):
    """
    Merge detection methods
    without duplicates.

    Returns:
        list[str]
    """

    merged = []

    for method_list in methods:

        if not method_list:

            continue

        for method in method_list:

            if method not in merged:

                merged.append(

                    method,

                )

    return merged


# ==========================================================
# Deep Copy Result
# ==========================================================

def create_result():
    """
    Create empty CDN result.

    Returns:
        dict
    """

    return deepcopy(

        EMPTY_CDN_RESULT

    )


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "EMPTY_CDN_RESULT",

    "normalize_target",

    "resolve_ipv4",

    "request_headers",

    "extract_headers",

    "resolve_cname",

    "header_exists",

    "get_server_header",

    "get_cache_headers",

    "safe_lower",

    "merge_methods",

    "create_result",

]