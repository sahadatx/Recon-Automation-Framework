from __future__ import annotations

import socket
from copy import deepcopy
from typing import Any
from urllib.parse import urlparse

import dns.resolver
import requests
from bs4 import BeautifulSoup

from config.config import HTTP_TIMEOUT

from .constants import DEFAULT_ANALYSIS, DEFAULT_HEADERS


EMPTY_TAKEOVER_RESULT = deepcopy(
    DEFAULT_ANALYSIS,
)


def normalize_target(
    target: str,
):


    if not target:

        return ""

    target = target.strip()

    if "://" not in target:

        target = f"https://{target}"

    parsed = urlparse(
        target,
    )

    return parsed.hostname or ""


def resolve_ipv4(
    host: str,
):


    try:

        return socket.gethostbyname(
            host,
        )

    except Exception:

        return None


def request_page(
    target: str,
):


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


def extract_status_code(
    response,
):


    if response is None:

        return 0

    return response.status_code


def extract_body(
    response,
):


    if response is None:

        return ""

    return response.text


def extract_title(
    response,
):


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


def resolve_cname(
    host: str,
):


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


def safe_lower(
    value: Any,
):


    if value is None:

        return ""

    return str(
        value,
    ).lower()


def contains_fingerprint(
    content: str,
    fingerprints: set[str],
):


    content = safe_lower(
        content,
    )

    for fingerprint in fingerprints:

        if (
            safe_lower(
                fingerprint,
            )
            in content
        ):

            return fingerprint

    return None


def merge_methods(
    *methods,
):


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


def create_result():


    return deepcopy(
        EMPTY_TAKEOVER_RESULT,
    )


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
