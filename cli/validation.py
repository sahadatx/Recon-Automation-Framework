"""
CLI Validation

Validate command-line arguments
for the Recon Automation Framework.
"""

from __future__ import annotations

import ipaddress
import re


# ==========================================================
# Constants
# ==========================================================

DOMAIN_PATTERN = re.compile(
    r"^(?!-)"
    r"(?:[A-Za-z0-9-]{1,63}\.)+"
    r"[A-Za-z]{2,63}$"
)


# ==========================================================
# Internal Helpers
# ==========================================================

def _validate_positive(
    value: int,
    name: str,
) -> int:
    """
    Validate that a value is greater than zero.
    """

    if value < 1:

        raise ValueError(
            f"{name} must be greater than 0."
        )

    return value


# ==========================================================
# Validate Target
# ==========================================================

def validate_target(
    target: str,
) -> str:
    """
    Validate a scan target.

    Supports:

        - Domain
        - Hostname
        - IPv4
        - IPv6
    """

    target = target.strip()

    if not target:

        raise ValueError(
            "Target cannot be empty."
        )

    # ------------------------------------------------------
    # IP Address
    # ------------------------------------------------------

    try:

        ipaddress.ip_address(
            target,
        )

        return target

    except ValueError:

        pass

    # ------------------------------------------------------
    # Domain / Hostname
    # ------------------------------------------------------

    if DOMAIN_PATTERN.fullmatch(
        target,
    ):

        return target

    raise ValueError(
        f"Invalid target: {target}"
    )


# ==========================================================
# Validate Threads
# ==========================================================

def validate_threads(
    threads: int,
) -> int:
    """
    Validate worker thread count.
    """

    return _validate_positive(
        threads,
        "Threads",
    )


# ==========================================================
# Validate Timeout
# ==========================================================

def validate_timeout(
    timeout: int,
) -> int:
    """
    Validate request timeout.
    """

    return _validate_positive(
        timeout,
        "Timeout",
    )


# ==========================================================
# Validate Retries
# ==========================================================

def validate_retries(
    retries: int,
) -> int:
    """
    Validate retry attempts.
    """

    if retries < 0:

        raise ValueError(
            "Retries cannot be negative."
        )

    return retries


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "validate_target",

    "validate_threads",

    "validate_timeout",

    "validate_retries",

]