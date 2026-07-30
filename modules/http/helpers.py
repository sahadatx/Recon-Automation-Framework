#!/usr/bin/env python3

"""
HTTP Helper Functions

Shared helper functions used by
the HTTP Probe module.
"""

from __future__ import annotations

from config.config import (
    HTTP_TIMEOUT,
    VERBOSE,
)

from core.logger import (
    debug,
)


# ==========================================================
# Show Probe
# ==========================================================

def show_probe(
    url: str,
) -> None:
    """
    Display probe information.

    Probe messages are only shown
    when verbose mode is enabled.
    """

    if not VERBOSE:

        return

    debug(
        f"Probing {url}"
    )


# ==========================================================
# Request Timeout
# ==========================================================

def request_timeout() -> int | float:
    """
    Return the configured HTTP
    request timeout.
    """

    return HTTP_TIMEOUT


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "request_timeout",
    "show_probe",
]