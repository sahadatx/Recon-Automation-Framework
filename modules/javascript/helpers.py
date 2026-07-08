"""
JavaScript Helper Functions

Shared helper functions for the
JavaScript Analysis module.
"""

from pathlib import Path

import requests

from config.config import (
    HTTP_TIMEOUT,
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

            "User-Agent": (
                "ReconAutomationFramework/2.0"
            ),

        }

    )

    return session


# ==========================================================
# Global Session
# ==========================================================

SESSION = create_session()


# ==========================================================
# Create Output Directory
# ==========================================================

def create_output_directory():
    """
    Create JavaScript output directory.

    Returns:
        Path
    """

    output = Path(
        "output/javascript/raw"
    )

    output.mkdir(

        parents=True,

        exist_ok=True,

    )

    return output


# ==========================================================
# Safe Filename
# ==========================================================

def safe_filename(
    url: str,
):
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

    if not filename.endswith(".js"):

        filename += ".js"

    return filename


# ==========================================================
# Save JavaScript
# ==========================================================

def save_javascript(
    filename: str,
    content: str,
):
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

    for attempt in range(3):

        try:

            response = SESSION.get(

                url,

                timeout=HTTP_TIMEOUT,

                allow_redirects=True,

            )

            response.raise_for_status()

            return response

        except requests.RequestException as error:

            debug(

                f"Retry {attempt + 1}: "

                f"{url} ({error})"

            )

    debug(
        f"Failed: {url}"
    )

    return None