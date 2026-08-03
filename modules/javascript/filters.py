"""
JavaScript Secret Filters

Removes false positives from
detected JavaScript secrets.
"""

from __future__ import annotations

import re

# ==========================================================
# Placeholder Values
# ==========================================================

PLACEHOLDERS = {
    "",
    "api_key",
    "apikey",
    "secret",
    "password",
    "token",
    "bearer",
    "your_api_key",
    "your_token",
    "your_secret",
    "change_me",
    "example",
    "sample",
    "dummy",
    "test",
    "null",
    "none",
}


# ==========================================================
# Minimum Secret Length
# ==========================================================

MIN_SECRET_LENGTH = 20


# ==========================================================
# Empty Value
# ==========================================================


def is_empty(
    value: str,
) -> bool:
    """
    Check whether a value is empty.

    Returns:
        bool
    """

    return not value.strip()


# ==========================================================
# Placeholder Value
# ==========================================================


def is_placeholder(
    value: str,
) -> bool:
    """
    Check whether a value is
    a known placeholder.

    Returns:
        bool
    """

    return value.strip().lower() in PLACEHOLDERS


# ==========================================================
# Too Short
# ==========================================================


def is_short(
    value: str,
) -> bool:
    """
    Check whether a value is
    shorter than the minimum
    secret length.

    Returns:
        bool
    """

    return len(value.strip()) < MIN_SECRET_LENGTH


# ==========================================================
# Base64 Noise
# ==========================================================


def is_base64_noise(
    value: str,
) -> bool:
    """
    Ignore generic Base64 strings.

    Returns:
        bool
    """

    return (
        re.fullmatch(
            r"[A-Za-z0-9+/=]+",
            value,
        )
        is not None
    )


# ==========================================================
# Repeated Characters
# ==========================================================


def is_repeated(
    value: str,
) -> bool:
    """
    Detect repeated characters.

    Examples:
        aaaaaaaaaaaaa
        111111111111

    Returns:
        bool
    """

    return len(set(value)) <= 2


# ==========================================================
# Generic API Key Validation
# ==========================================================


def is_generic_noise(
    value: str,
) -> bool:
    """
    Detect weak generic API keys.

    Returns:
        bool
    """

    has_letter = any(char.isalpha() for char in value)

    has_digit = any(char.isdigit() for char in value)

    return not (has_letter and has_digit)


# ==========================================================
# JWT Validation
# ==========================================================


def is_valid_jwt(
    value: str,
) -> bool:
    """
    JWT must contain
    three sections.

    Returns:
        bool
    """

    return value.count(".") == 2


# ==========================================================
# Keep Secret
# ==========================================================


def keep_secret(
    secret_type: str,
    value: str,
) -> bool:
    """
    Decide whether a detected
    secret should be kept.

    Returns:
        bool
    """

    if is_empty(value):

        return False

    if is_placeholder(value):

        return False

    if is_short(value):

        return False

    if is_repeated(value):

        return False

    if secret_type == "jwt" and not is_valid_jwt(value):

        return False

    if secret_type == "generic_api_key" and is_generic_noise(value):

        return False

    if secret_type == "generic_api_key" and is_base64_noise(value):

        return False

    return True


# ==========================================================
# Filter Findings
# ==========================================================


def filter_findings(
    findings: dict[str, list[str]],
) -> dict[str, list[str]]:
    """
    Remove false positives from
    detected secrets.

    Returns:
        dict[str, list[str]]
    """

    filtered: dict[str, list[str]] = {}

    for secret_type, values in findings.items():

        kept = sorted(
            {
                value
                for value in values
                if keep_secret(
                    secret_type,
                    value,
                )
            }
        )

        if kept:

            filtered[secret_type] = kept

    return filtered


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "MIN_SECRET_LENGTH",
    "PLACEHOLDERS",
    "is_empty",
    "is_placeholder",
    "is_short",
    "is_base64_noise",
    "is_repeated",
    "is_generic_noise",
    "is_valid_jwt",
    "keep_secret",
    "filter_findings",
]
