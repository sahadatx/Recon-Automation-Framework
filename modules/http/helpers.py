"""
HTTP Helper Functions

Shared helper functions used by the
HTTP Probe module.
"""

import requests

from config.config import (
    HTTP_TIMEOUT,
    HTTP_VERIFY_SSL,
    HTTP_USER_AGENT,
    VERBOSE,
)

from core.logger import (
    debug,
)

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()


# ==========================================================
# Create Session
# ==========================================================

def create_session():
    """
    Create and configure an HTTP session.

    Returns:
        requests.Session
    """

    session = requests.Session()

    session.verify = HTTP_VERIFY_SSL

    session.headers.update(
        {
            "User-Agent": HTTP_USER_AGENT,
        }
    )

    return session


# ==========================================================
# Show Probe
# ==========================================================

def show_probe(
    url: str,
):
    """
    Display probe information.

    Only shown when VERBOSE mode is enabled.
    """

    if VERBOSE:

        debug(
            f"Probing {url}"
        )


# ==========================================================
# Request Timeout
# ==========================================================

def request_timeout():
    """
    Return configured HTTP timeout.
    """

    return HTTP_TIMEOUT