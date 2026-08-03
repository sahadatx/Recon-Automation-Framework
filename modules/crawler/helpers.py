#!/usr/bin/env python3

"""
Crawler Helper Functions

Shared helper functions used by the
URL Discovery module.
"""

from __future__ import annotations

import time
from urllib.parse import (
    urljoin,
    urlparse,
    urlunparse,
)

import requests
import urllib3

from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    HTTPError,
    ReadTimeout,
    Timeout,
)

from config.config import (
    CRAWLER_RETRIES,
    HTTP_TIMEOUT,
)

from core.logger import (
    debug,
)

# ==========================================================
# Disable SSL Warnings
# ==========================================================

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning,
)

# ==========================================================
# Retryable HTTP Status Codes
# ==========================================================

RETRY_STATUS_CODES: set[int] = {
    500,
    502,
    503,
    504,
}

# ==========================================================
# Normalize URL
# ==========================================================


def normalize_url(
    base_url: str,
    link: str,
) -> str:
    """
    Convert a relative URL into
    a canonical absolute URL.
    """

    url = urljoin(
        base_url,
        link,
    )

    parsed = urlparse(
        url,
    )

    path = parsed.path

    if path == "/":

        path = ""

    elif path.endswith("/"):

        path = path.rstrip("/")

    parsed = parsed._replace(
        path=path,
        fragment="",
    )

    return urlunparse(
        parsed,
    )


# ==========================================================
# Same Domain
# ==========================================================


def same_domain(
    root_url: str,
    url: str,
) -> bool:
    """
    Check whether two URLs
    belong to the same host.
    """

    return urlparse(root_url).netloc == urlparse(url).netloc


# ==========================================================
# HTML Detection
# ==========================================================


def is_html(
    response: requests.Response | None,
) -> bool:
    """
    Determine whether the response
    contains HTML content.
    """

    if response is None:

        return False

    content_type = response.headers.get(
        "Content-Type",
        "",
    ).lower()

    return "text/html" in content_type or "application/xhtml+xml" in content_type


# ==========================================================
# Retry Policy
# ==========================================================


def should_retry(
    error: Exception,
) -> bool:
    """
    Determine whether the failed
    request should be retried.
    """

    if isinstance(
        error,
        (
            Timeout,
            ConnectTimeout,
            ReadTimeout,
            ConnectionError,
        ),
    ):

        return True

    if isinstance(
        error,
        HTTPError,
    ):

        response = getattr(
            error,
            "response",
            None,
        )

        if response is None:

            return False

        return response.status_code in RETRY_STATUS_CODES

    return False


# ==========================================================
# Download Page
# ==========================================================


def download_page(
    session: requests.Session,
    url: str,
) -> requests.Response | None:
    """
    Download an HTML page using the
    shared HTTP session.
    """

    for attempt in range(
        CRAWLER_RETRIES,
    ):

        try:

            start = time.perf_counter()

            response = session.get(
                url,
                timeout=HTTP_TIMEOUT,
                allow_redirects=True,
            )

            response.elapsed_time = round(
                time.perf_counter() - start,
                3,
            )

            response.raise_for_status()

            if not is_html(
                response,
            ):

                debug(
                    f"Skipped non-HTML: {url}",
                )

                return None

            return response

        except requests.exceptions.SSLError as error:

            debug(
                f"SSL Error: {url} ({error})",
            )

            return None

        except requests.RequestException as error:

            if not should_retry(
                error,
            ):

                if (
                    isinstance(
                        error,
                        HTTPError,
                    )
                    and error.response is not None
                ):

                    debug(
                        f"HTTP {error.response.status_code}: {url}",
                    )

                else:

                    debug(
                        f"Not retrying: {url} ({error})",
                    )

                return None

            debug(
                f"Retry ({attempt + 1}/{CRAWLER_RETRIES}): {url}",
            )

            if attempt < (CRAWLER_RETRIES - 1):

                time.sleep(
                    2**attempt,
                )

    debug(
        f"Failed after {CRAWLER_RETRIES} attempts: {url}",
    )

    return None


# ==========================================================
# Extract Domain
# ==========================================================


def get_domain(
    url: str,
) -> str:
    """
    Return the hostname
    from a URL.
    """

    return urlparse(
        url,
    ).netloc


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "download_page",
    "get_domain",
    "is_html",
    "normalize_url",
    "same_domain",
    "should_retry",
]
