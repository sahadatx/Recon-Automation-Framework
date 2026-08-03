#!/usr/bin/env python3

"""
HTTP Probe Engine

Probe HTTP and HTTPS services
using the shared HTTP session.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from core.logger import warning
from modules.http.helpers import request_timeout, show_probe

# ==========================================================
# Probe URL
# ==========================================================


def probe_url(
    session: requests.Session,
    url: str,
) -> dict[str, Any] | None:
    """
    Probe a single URL.

    Args:
        session:
            Shared HTTP session.

        url:
            Target URL.

    Returns:
        HTTP response information
        or None when unreachable.
    """

    show_probe(
        url,
    )

    start_time = time.perf_counter()

    try:

        response = session.get(
            url,
            timeout=request_timeout(),
            allow_redirects=True,
        )

    except requests.RequestException:

        return None

    elapsed = round(
        time.perf_counter() - start_time,
        3,
    )

    return {
        # --------------------------------------------------
        # General
        # --------------------------------------------------
        "alive": True,
        "url": response.url,
        "scheme": response.url.split(
            "://",
            1,
        )[0],
        "status": response.status_code,
        "response_time": elapsed,
        "redirect": bool(
            response.history,
        ),
        # --------------------------------------------------
        # Common Headers
        # --------------------------------------------------
        "server": response.headers.get(
            "Server",
            "",
        ),
        "content_type": response.headers.get(
            "Content-Type",
            "",
        ),
        "content_length": response.headers.get(
            "Content-Length",
            "0",
        ),
        # --------------------------------------------------
        # Raw Data
        # --------------------------------------------------
        "headers": dict(
            response.headers,
        ),
        "html": response.text,
    }


# ==========================================================
# Probe HTTP
# ==========================================================


def probe_http(
    session: requests.Session,
    host: str,
) -> dict[str, Any] | None:
    """
    Probe HTTP service.
    """

    return probe_url(
        session=session,
        url=f"http://{host}",
    )


# ==========================================================
# Probe HTTPS
# ==========================================================


def probe_https(
    session: requests.Session,
    host: str,
) -> dict[str, Any] | None:
    """
    Probe HTTPS service.
    """

    return probe_url(
        session=session,
        url=f"https://{host}",
    )


# ==========================================================
# Probe Host
# ==========================================================


def probe_host(
    session: requests.Session,
    host: str,
) -> dict[str, Any] | None:
    """
    Probe one host.

    HTTPS is attempted first.
    If HTTPS is unavailable,
    HTTP is attempted.
    """

    result = probe_https(
        session=session,
        host=host,
    )

    if result is not None:

        return result

    result = probe_http(
        session=session,
        host=host,
    )

    if result is not None:

        return result

    warning(f"{host} is not reachable.")

    return None


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "probe_host",
    "probe_http",
    "probe_https",
    "probe_url",
]
