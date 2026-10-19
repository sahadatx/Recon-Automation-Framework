import re


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


def is_short(
    value: str,
):


    return len(value.strip()) < MIN_STRING_LENGTH


def is_numeric(
    value: str,
):


    return value.isdigit()


def is_placeholder(
    value: str,
):


    return value.lower().strip() in PLACEHOLDERS


def is_hex(
    value: str,
):


    return (
        len(value) >= 16
        and re.fullmatch(
            r"[0-9a-fA-F]+",
            value,
        )
        is not None
    )


def is_base64(
    value: str,
):


    return (
        len(value) >= 16
        and re.fullmatch(
            r"[A-Za-z0-9+/=]+",
            value,
        )
        is not None
    )


def is_repeated(
    value: str,
):


    return len(set(value)) <= 2


def is_junk(
    value: str,
):


    return (
        re.fullmatch(
            r"[\W_]+",
            value,
        )
        is not None
    )


def keep_string(
    value: str,
):


    value = value.strip()

    if not value:

        return False

    if is_short(value):

        return False

    if is_numeric(value):

        return False

    if is_placeholder(value):

        return False

    if is_hex(value):

        return False

    if is_base64(value):

        return False

    if is_repeated(value):

        return False

    if is_junk(value):

        return False

    return True


def filter_strings(
    strings,
):


    filtered = {string.strip() for string in strings if keep_string(string)}

    return sorted(filtered)
