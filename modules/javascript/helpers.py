"""
JavaScript Helper Functions

Shared helper functions for the
JavaScript Analysis module.
"""

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

from config.config import (

    HTTP_TIMEOUT,

    HTTP_RETRIES,

    HTTP_USER_AGENT,

    HTTP_VERIFY_SSL,

    JAVASCRIPT_OUTPUT_DIR,

)

from core.logger import (

    debug,

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

def create_session():
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

    JAVASCRIPT_OUTPUT_DIR.mkdir(

        parents=True,

        exist_ok=True,

    )

    return JAVASCRIPT_OUTPUT_DIR


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

    if parsed.scheme not in (

        "http",

        "https",

    ):

        return False

    if not parsed.netloc:

        return False

    return True


# ==========================================================
# Safe Filename
# ==========================================================

def safe_filename(
    url: str,
) -> str:
    """
    Convert JavaScript URL into
    filesystem-safe filename.

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

        .replace(

            "/",

            "_",

        )

        .replace(

            "\\",

            "_",

        )

        .replace(

            "?",

            "_",

        )

        .replace(

            "&",

            "_",

        )

        .replace(

            "=",

            "_",

        )

        .replace(

            ":",

            "_",

        )

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

    output = create_output_directory()

    filepath = output / filename

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
    Decide whether request
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

        if response is None:

            return False

        return (

            response.status_code

            in

            RETRY_STATUS_CODES

        )

    return False


# ==========================================================
# Download File
# ==========================================================

def download_file(
    url: str,
):
    """
    Download JavaScript file.

    Returns:
        requests.Response | None
    """

    if not is_valid_url(

        url

    ):

        debug(

            f"Invalid URL skipped: {url}"

        )

        return None

    for attempt in range(

        HTTP_RETRIES + 1

    ):

        try:

            response = SESSION.get(

                url,

                timeout=HTTP_TIMEOUT,

                allow_redirects=True,

            )

            response.raise_for_status()

            return response

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

            if not should_retry(

                error

            ):

                if isinstance(

                    error,

                    HTTPError,

                ) and error.response is not None:

                    debug(

                        f"HTTP {error.response.status_code}: {url}"

                    )

                else:

                    debug(

                        f"Not retrying: {url} ({error})"

                    )

                return None

            if isinstance(

                error,

                HTTPError,

            ) and error.response is not None:

                debug(

                    f"Retry "

                    f"({attempt + 1}/{HTTP_RETRIES + 1}) "

                    f"HTTP {error.response.status_code}: "

                    f"{url}"

                )

            else:

                debug(

                    f"Retry "

                    f"({attempt + 1}/{HTTP_RETRIES + 1}): "

                    f"{url} ({error})"

                )

    debug(

        f"Failed after "

        f"{HTTP_RETRIES + 1} attempts: "

        f"{url}"

    )

    return None