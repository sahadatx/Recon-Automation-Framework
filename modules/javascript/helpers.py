"""
JavaScript Helper Functions

Shared helper functions for the
JavaScript Analysis module.
"""

from pathlib import Path

import requests

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
# Safe Filename
# ==========================================================

def safe_filename(
    url: str,
) -> str:
    """
    Convert JavaScript URL into
    filesystem-safe filename.

    Args:
        url:
            JavaScript URL.

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

    Args:
        filename:
            Output filename.

        content:
            JavaScript content.

    Returns:
        Path
    """

    output = create_output_directory()

    filepath = (

        output

        / filename

    )

    filepath.write_text(

        content,

        encoding="utf-8",

        errors="ignore",

    )

    return filepath


# ==========================================================
# Download File
# ==========================================================

def download_file(
    url: str,
):
    """
    Download JavaScript file.

    Args:
        url:
            JavaScript URL.

    Returns:
        requests.Response | None
    """

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

                f"SSL Error "

                f"({attempt + 1}/{HTTP_RETRIES + 1}): "

                f"{url} ({error})"

            )

        except requests.RequestException as error:

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