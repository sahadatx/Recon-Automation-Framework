from __future__ import annotations

import re


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


MIN_SECRET_LENGTH = 20


def is_empty(
    value: str,
) -> bool:


    return not value.strip()


def is_placeholder(
    value: str,
) -> bool:


    return value.strip().lower() in PLACEHOLDERS


def is_short(
    value: str,
) -> bool:


    return len(value.strip()) < MIN_SECRET_LENGTH


def is_base64_noise(
    value: str,
) -> bool:


    return (
        re.fullmatch(
            r"[A-Za-z0-9+/=]+",
            value,
        )
        is not None
    )


def is_repeated(
    value: str,
) -> bool:


    return len(set(value)) <= 2


def is_generic_noise(
    value: str,
) -> bool:


    has_letter = any(char.isalpha() for char in value)

    has_digit = any(char.isdigit() for char in value)

    return not (has_letter and has_digit)


def is_valid_jwt(
    value: str,
) -> bool:


    return value.count(".") == 2


def keep_secret(
    secret_type: str,
    value: str,
) -> bool:


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


def filter_findings(
    findings: dict[str, list[str]],
) -> dict[str, list[str]]:


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
