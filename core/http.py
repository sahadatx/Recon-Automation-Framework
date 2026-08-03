#!/usr/bin/env python3

"""
HTTP Session Utilities

Create and configure the shared
HTTP session used throughout the
Recon Automation Framework.
"""

from __future__ import annotations

import requests

from requests.adapters import HTTPAdapter

from config.config import (
    HTTP_USER_AGENT,
    HTTP_VERIFY_SSL,
)

# ==========================================================
# Create HTTP Session
# ==========================================================


def create_http_session() -> requests.Session:
    """
    Create the shared HTTP session.

    Returns:
        Configured requests.Session.
    """

    session = requests.Session()

    # ------------------------------------------------------
    # SSL Verification
    # ------------------------------------------------------

    session.verify = HTTP_VERIFY_SSL

    # ------------------------------------------------------
    # Default Headers
    # ------------------------------------------------------

    session.headers.update(
        {
            "User-Agent": HTTP_USER_AGENT,
        }
    )

    # ------------------------------------------------------
    # Connection Pool
    # ------------------------------------------------------

    adapter = HTTPAdapter(
        pool_connections=100,
        pool_maxsize=100,
    )

    session.mount(
        "http://",
        adapter,
    )

    session.mount(
        "https://",
        adapter,
    )

    return session


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "create_http_session",
]
