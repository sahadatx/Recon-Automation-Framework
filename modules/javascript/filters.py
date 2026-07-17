"""
JavaScript Secret Filters

Removes false positives from
detected JavaScript secrets.
"""

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
):
    """
    Empty value.
    """

    return not value.strip()


# ==========================================================
# Placeholder
# ==========================================================

def is_placeholder(
    value: str,
):
    """
    Placeholder value.
    """

    value = value.lower().strip()

    return value in PLACEHOLDERS


# ==========================================================
# Too Short
# ==========================================================

def is_short(
    value: str,
):
    """
    Too short.
    """

    return len(

        value.strip()

    ) < MIN_SECRET_LENGTH


# ==========================================================
# Base64 Noise
# ==========================================================

def is_base64_noise(
    value: str,
):
    """
    Ignore generic Base64 strings.
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
):
    """
    aaaaaaaaaaaaa
    111111111111
    """

    return len(

        set(value)

    ) <= 2


# ==========================================================
# Generic API Key Validation
# ==========================================================

def is_generic_noise(
    value: str,
):
    """
    Generic API key
    false positive.
    """

    has_letter = any(

        c.isalpha()

        for c in value

    )

    has_digit = any(

        c.isdigit()

        for c in value

    )

    return not (

        has_letter

        and

        has_digit

    )


# ==========================================================
# JWT Validation
# ==========================================================

def is_valid_jwt(
    value: str,
):
    """
    JWT must contain
    3 sections.
    """

    return (

        value.count(".")

        == 2

    )


# ==========================================================
# Keep Secret?
# ==========================================================

def keep_secret(
    secret_type: str,
    value: str,
):
    """
    Decide whether a
    secret should be kept.
    """

    if is_empty(

        value

    ):

        return False

    if is_placeholder(

        value

    ):

        return False

    if is_short(

        value

    ):

        return False

    if is_repeated(

        value

    ):

        return False

    if (

        secret_type

        == "jwt"

        and

        not is_valid_jwt(

            value

        )

    ):

        return False

    if (

        secret_type

        == "generic_api_key"

        and

        is_generic_noise(

            value

        )

    ):

        return False

    if (

        secret_type

        == "generic_api_key"

        and

        is_base64_noise(

            value

        )

    ):

        return False

    return True


# ==========================================================
# Filter Findings
# ==========================================================

def filter_findings(
    findings: dict,
):
    """
    Remove false positives.

    Returns:
        dict
    """

    filtered = {}

    for secret_type, values in findings.items():

        kept = [

            value

            for value

            in values

            if keep_secret(

                secret_type,

                value,

            )

        ]

        if kept:

            filtered[

                secret_type

            ] = sorted(

                set(kept)

            )

    return filtered
