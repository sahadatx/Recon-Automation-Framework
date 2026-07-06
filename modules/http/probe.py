"""
HTTP Probe Engine

Probe HTTP and HTTPS services for a host.
"""

import time

import requests

from core.logger import (
    warning,
)

from modules.http.helpers import (
    create_session,
    show_probe,
    request_timeout,
)


# ==========================================================
# Probe HTTP
# ==========================================================

def probe_http(
    host: str,
):
    """
    Probe HTTP (port 80).
    """

    url = f"http://{host}"

    return probe_url(url)


# ==========================================================
# Probe HTTPS
# ==========================================================

def probe_https(
    host: str,
):
    """
    Probe HTTPS (port 443).
    """

    url = f"https://{host}"

    return probe_url(url)


# ==========================================================
# Probe URL
# ==========================================================

def probe_url(
    url: str,
):
    """
    Probe a single URL.
    """

    session = create_session()

    show_probe(url)

    start = time.perf_counter()

    try:

        response = session.get(
            url,
            timeout=request_timeout(),
            allow_redirects=True,
        )

        elapsed = round(
            time.perf_counter() - start,
            3,
        )

        return {

            "alive": True,

            "url": response.url,

            "scheme": response.url.split(
                "://"
            )[0],

            "status": response.status_code,

            "server": response.headers.get(
                "Server",
                ""
            ),

            "content_type": response.headers.get(
                "Content-Type",
                ""
            ),

            "content_length": response.headers.get(
                "Content-Length",
                "0",
            ),

            "response_time": elapsed,

            "redirect": (
                response.history != []
            ),

        }

    except requests.RequestException:

        return None


# ==========================================================
# Probe Host
# ==========================================================

def probe_host(
    host: str,
):
    """
    Probe HTTPS first.

    If HTTPS fails,
    try HTTP.
    """

    result = probe_https(host)

    if result:

        return result

    result = probe_http(host)

    if result:

        return result

    warning(
        f"{host} is not reachable."
    )

    return None