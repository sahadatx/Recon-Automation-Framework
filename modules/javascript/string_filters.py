"""
JavaScript String Filters

Filters extracted JavaScript strings
to remove noise and false positives.
"""

import re


# ==========================================================
# Configuration
# ==========================================================

MIN_STRING_LENGTH = 3

PLACEHOLDERS = {

    "",

    "null",
    "none",

    "true",
    "false",

    "undefined",

    "nan",

    "api",

    "token",

    "secret",

    "password",

    "key",

    "example",

    "sample",

    "dummy",

    "test",

}


# ==========================================================
# Too Short
# ==========================================================

def is_short(
    value: str,
):
    """
    Ignore very short strings.
    """

    return len(

        value.strip()

    ) < MIN_STRING_LENGTH


# ==========================================================
# Numeric
# ==========================================================

def is_numeric(
    value: str,
):
    """
    Ignore numbers.
    """

    return value.isdigit()


# ==========================================================
# Placeholder
# ==========================================================

def is_placeholder(
    value: str,
):
    """
    Ignore placeholder values.
    """

    return (

        value.lower().strip()

        in

        PLACEHOLDERS

    )


# ==========================================================
# Hex String
# ==========================================================

def is_hex(
    value: str,
):
    """
    Ignore long hexadecimal strings.
    """

    return (

        len(value) >= 16

        and

        re.fullmatch(

            r"[0-9a-fA-F]+",

            value,

        )

        is not None

    )


# ==========================================================
# Base64
# ==========================================================

def is_base64(
    value: str,
):
    """
    Ignore generic Base64 strings.
    """

    return (

        len(value) >= 16

        and

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
    Ignore repeated characters.

    Example:

        aaaaaaaaaaaa

        111111111111
    """

    return len(

        set(value)

    ) <= 2


# ==========================================================
# Junk Characters
# ==========================================================

def is_junk(
    value: str,
):
    """
    Ignore punctuation-only strings.
    """

    return (

        re.fullmatch(

            r"[\W_]+",

            value,

        )

        is not None

    )


# ==========================================================
# Keep String
# ==========================================================

def keep_string(
    value: str,
):
    """
    Decide whether the string
    should be kept.
    """

    value = value.strip()

    if not value:

        return False

    if is_short(

        value

    ):

        return False

    if is_numeric(

        value

    ):

        return False

    if is_placeholder(

        value

    ):

        return False

    if is_hex(

        value

    ):

        return False

    if is_base64(

        value

    ):

        return False

    if is_repeated(

        value

    ):

        return False

    if is_junk(

        value

    ):

        return False

    return True


# ==========================================================
# Filter Strings
# ==========================================================

def filter_strings(
    strings,
):
    """
    Remove noisy strings.

    Returns:
        list
    """

    filtered = {

        string.strip()

        for string

        in strings

        if keep_string(

            string

        )

    }

    return sorted(

        filtered

    )
