from __future__ import annotations

import socket
from copy import deepcopy
from typing import Any
from urllib.parse import urlparse

import dns.resolver

from config.config import HTTP_TIMEOUT
from core.context import ExecutionContext

from .constants import DEFAULT_ANALYSIS, DEFAULT_HEADERS


EMPTY_CDN_RESULT = deepcopy(DEFAULT_ANALYSIS)


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


def request_headers(
    context: ExecutionContext,
    target: str,
):


    session = context.get_http_session()

    if session is None:
        raise RuntimeError("Shared HTTP session is not initialized.")

    try:

        response = session.get(
            target,
            headers=DEFAULT_HEADERS,
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )

        return response

    except Exception:

        return None


def extract_headers(
    response,
):


    if response is None:

        return {}

    return dict(response.headers)


def resolve_cname(
    host: str,
):


    try:

        answers = dns.resolver.resolve(
            host,
            "CNAME",
        )

        return str(answers[0].target).rstrip(".")

    except Exception:

        return None


def header_exists(
    headers: dict[str, Any],
    header: str,
):


    return header.lower() in {key.lower() for key in headers}


def get_server_header(
    headers: dict[str, Any],
):


    for key, value in headers.items():

        if key.lower() == "server":

            return str(
                value,
            )

    return ""


def get_cache_headers(
    headers: dict[str, Any],
):


    cache_headers = {}

    for key, value in headers.items():

        key_lower = key.lower()

        if "cache" in key_lower or key_lower == "age" or key_lower == "via":

            cache_headers[key] = value

    return cache_headers


def safe_lower(
    value: Any,
):


    if value is None:

        return ""

    return str(
        value,
    ).lower()


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


    return deepcopy(EMPTY_CDN_RESULT)


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
