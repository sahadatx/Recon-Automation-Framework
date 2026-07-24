"""
JavaScript Helper Functions

Shared helper functions for the
JavaScript Analysis module.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import requests

from config.config import (
    HTTP_USER_AGENT,
    HTTP_VERIFY_SSL,
)

from modules.javascript.constants import (
    FILES_DIR,
)


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
# Create Session
# ==========================================================

def create_session() -> requests.Session:
    """
    Create reusable HTTP session.

    Returns:
        requests.Session
    """

    session = requests.Session()

    session.headers.update(

        {

            "User-Agent": HTTP_USER_AGENT,

        }

    )

    session.verify = HTTP_VERIFY_SSL

    return session


# ==========================================================
# Global Session
# ==========================================================

SESSION = create_session()


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

    Returns:
        bool
    """

    if not url:

        return False

    try:

        parsed = urlparse(
            url
        )

    except ValueError:

        return False

    return (

        parsed.scheme in {

            "http",

            "https",

        }

        and

        bool(
            parsed.netloc
        )

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

    Returns:
        str
    """

    filename = (

        url

        .replace(
            "https://",
            "",
        )

        .replace(
            "http://",
            "",
        )

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

        ".js"

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

    Returns:
        Path
    """

    filepath = (

        create_output_directory()

        / filename

    )

    filepath.write_text(

        content,

        encoding="utf-8",

        errors="ignore",

    )

    return filepath

from requests.exceptions import (

    ConnectionError,

    ConnectTimeout,

    HTTPError,

    ReadTimeout,

    Timeout,

)

from config.config import (

    HTTP_RETRIES,

    HTTP_TIMEOUT,

)

from core.logger import (

    debug,

)


# ==========================================================
# Retry Policy
# ==========================================================

def should_retry(
    error: Exception,
) -> bool:
    """
    Decide whether a request
    should be retried.

    Returns:
        bool
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

        return (

            response is not None

            and

            response.status_code

            in

            RETRY_STATUS_CODES

        )

    return False


# ==========================================================
# Make Request
# ==========================================================

def make_request(
    url: str,
) -> requests.Response:
    """
    Send HTTP GET request.

    Returns:
        requests.Response
    """

    response = SESSION.get(

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
    url: str,
) -> requests.Response | None:
    """
    Download a JavaScript file.

    Returns:
        requests.Response | None
    """

    if not is_valid_url(url):

        debug(
            f"Invalid URL skipped: {url}"
        )

        return None

    attempts = HTTP_RETRIES + 1

    for attempt in range(attempts):

        try:

            return make_request(
                url
            )

        except requests.exceptions.SSLError as error:

            debug(
                f"SSL Error: {url} ({error})"
            )

            return None

        except ValueError as error:

            debug(
                f"Invalid URL: {url} ({error})"
            )

            return None

        except requests.RequestException as error:

            if not should_retry(error):

                if (

                    isinstance(

                        error,

                        HTTPError,

                    )

                    and

                    error.response is not None

                ):

                    debug(

                        f"HTTP "

                        f"{error.response.status_code}: "

                        f"{url}"

                    )

                else:

                    debug(

                        f"Not retrying: "

                        f"{url} ({error})"

                    )

                return None

            if (

                isinstance(

                    error,

                    HTTPError,

                )

                and

                error.response is not None

            ):

                debug(

                    f"Retry "

                    f"({attempt + 1}/{attempts}) "

                    f"HTTP "

                    f"{error.response.status_code}: "

                    f"{url}"

                )

            else:

                debug(

                    f"Retry "

                    f"({attempt + 1}/{attempts}): "

                    f"{url} ({error})"

                )

    debug(

        f"Failed after "

        f"{attempts} attempts: "

        f"{url}"

    )

    return None


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "SESSION",

    "RETRY_STATUS_CODES",

    "create_session",

    "create_output_directory",

    "is_valid_url",

    "safe_filename",

    "save_javascript",

    "should_retry",

    "make_request",

    "download_file",

]