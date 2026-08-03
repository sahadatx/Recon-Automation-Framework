"""
JavaScript Helper Functions

Shared helper functions for the
JavaScript Analysis module.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    HTTPError,
    ReadTimeout,
    Timeout,
)

from config.config import HTTP_RETRIES, HTTP_TIMEOUT
from core.context import ExecutionContext
from core.logger import debug
from modules.javascript.constants import FILES_DIR

# ==========================================================
# Retryable HTTP Status Codes
# ==========================================================

RETRY_STATUS_CODES = {
    500,
    502,
    503,
    504,
}


# ==========================================================
# Create Output Directory
# ==========================================================


def create_output_directory() -> Path:
    """
    Create JavaScript output directory.

    Returns:
        Path
    """

    FILES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return FILES_DIR


# ==========================================================
# URL Validation
# ==========================================================


def is_valid_url(
    url: str,
) -> bool:
    """
    Validate JavaScript URL.
    """

    if not url:
        return False

    try:
        parsed = urlparse(
            url,
        )

    except ValueError:
        return False

    return parsed.scheme in {
        "http",
        "https",
    } and bool(
        parsed.netloc,
    )


# ==========================================================
# Safe Filename
# ==========================================================


def safe_filename(
    url: str,
) -> str:
    """
    Convert JavaScript URL into
    a filesystem-safe filename.
    """

    filename = url.replace(
        "https://",
        "",
    ).replace(
        "http://",
        "",
    )

    for character in (
        "/",
        "\\",
        "?",
        "&",
        "=",
        ":",
    ):
        filename = filename.replace(
            character,
            "_",
        )

    if not filename.endswith(
        ".js",
    ):
        filename += ".js"

    return filename


# ==========================================================
# Save JavaScript
# ==========================================================


def save_javascript(
    filename: str,
    content: str,
) -> Path:
    """
    Save JavaScript file.
    """

    filepath = create_output_directory() / filename

    filepath.write_text(
        content,
        encoding="utf-8",
        errors="ignore",
    )

    return filepath


# ==========================================================
# Retry Policy
# ==========================================================


def should_retry(
    error: Exception,
) -> bool:
    """
    Decide whether a request
    should be retried.
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

        return response is not None and response.status_code in RETRY_STATUS_CODES

    return False


# ==========================================================
# Make Request
# ==========================================================


def make_request(
    context: ExecutionContext,
    url: str,
) -> requests.Response:
    """
    Send HTTP GET request.
    """

    session = context.get_http_session()

    if session is None:
        raise RuntimeError("Shared HTTP session is not initialized.")

    response = session.get(
        url,
        timeout=HTTP_TIMEOUT,
        allow_redirects=True,
    )

    response.raise_for_status()

    return response


# ==========================================================
# Download File
# ==========================================================


def download_file(
    context: ExecutionContext,
    url: str,
) -> requests.Response | None:
    """
    Download a JavaScript file.
    """

    if not is_valid_url(
        url,
    ):

        debug(f"Invalid URL skipped: {url}")

        return None

    attempts = HTTP_RETRIES + 1

    for attempt in range(
        attempts,
    ):

        try:

            return make_request(
                context,
                url,
            )

        except requests.exceptions.SSLError as error:

            debug(f"SSL Error: {url} ({error})")

            return None

        except ValueError as error:

            debug(f"Invalid URL: {url} ({error})")

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

                    debug(f"HTTP {error.response.status_code}: {url}")

                else:

                    debug(f"Not retrying: {url} ({error})")

                return None

            if (
                isinstance(
                    error,
                    HTTPError,
                )
                and error.response is not None
            ):

                debug(
                    f"Retry ({attempt + 1}/{attempts}) "
                    f"HTTP {error.response.status_code}: {url}"
                )

            else:

                debug(f"Retry ({attempt + 1}/{attempts}): " f"{url} ({error})")

    debug(f"Failed after {attempts} attempts: {url}")

    return None


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "RETRY_STATUS_CODES",
    "create_output_directory",
    "is_valid_url",
    "safe_filename",
    "save_javascript",
    "should_retry",
    "make_request",
    "download_file",
]
