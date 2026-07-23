"""
Subdomain Takeover Helpers

Reusable helper functions for
Subdomain Takeover Detection.
"""

from __future__ import annotations

import socket

from copy import deepcopy
from typing import Any
from urllib.parse import urlparse

import dns.resolver
import requests

from bs4 import BeautifulSoup

from config.config import HTTP_TIMEOUT

from .constants import (
    DEFAULT_ANALYSIS,
    DEFAULT_HEADERS,
)


# ==========================================================
# Default Result
# ==========================================================

EMPTY_TAKEOVER_RESULT = deepcopy(

    DEFAULT_ANALYSIS,

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

def request_page(
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
# Status Code
# ==========================================================

def extract_status_code(
    response,
):
    """
    Extract HTTP status code.

    Returns:
        int
    """

    if response is None:

        return 0

    return response.status_code


# ==========================================================
# Response Body
# ==========================================================

def extract_body(
    response,
):
    """
    Extract response body.

    Returns:
        str
    """

    if response is None:

        return ""

    return response.text


# ==========================================================
# HTML Title
# ==========================================================

def extract_title(
    response,
):
    """
    Extract HTML title.

    Returns:
        str
    """

    if response is None:

        return ""

    try:

        soup = BeautifulSoup(

            response.text,

            "html.parser",

        )

        if soup.title:

            return soup.title.get_text(

                strip=True,

            )

    except Exception:

        pass

    return ""


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

            answers[0].target,

        ).rstrip(".")

    except Exception:

        return None


# ==========================================================
# Safe Lower
# ==========================================================

def safe_lower(
    value: Any,
):
    """
    Safely convert a value
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
# Fingerprint Detection
# ==========================================================

def contains_fingerprint(
    content: str,
    fingerprints: set[str],
):
    """
    Check whether any
    fingerprint exists.

    Returns:
        str | None
    """

    content = safe_lower(

        content,

    )

    for fingerprint in fingerprints:

        if (

            safe_lower(
                fingerprint,
            )

            in

            content

        ):

            return fingerprint

    return None


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
    Create empty takeover
    result.

    Returns:
        dict
    """

    return deepcopy(

        EMPTY_TAKEOVER_RESULT,

    )


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "EMPTY_TAKEOVER_RESULT",

    "normalize_target",

    "resolve_ipv4",

    "request_page",

    "extract_status_code",

    "extract_body",

    "extract_title",

    "resolve_cname",

    "safe_lower",

    "contains_fingerprint",

    "merge_methods",

    "create_result",

]

