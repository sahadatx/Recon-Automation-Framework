from __future__ import annotations

import ipaddress
import re


DOMAIN_PATTERN = re.compile(r"^(?!-)" r"(?:[A-Za-z0-9-]{1,63}\.)+" r"[A-Za-z]{2,63}$")


def _validate_positive(
    value: int,
    name: str,
) -> int:


    if value < 1:

        raise ValueError(f"{name} must be greater than 0.")

    return value


def validate_target(
    target: str,
) -> str:


    target = target.strip()

    if not target:

        raise ValueError("Target cannot be empty.")


    try:

        ipaddress.ip_address(
            target,
        )

        return target

    except ValueError:

        pass


    if DOMAIN_PATTERN.fullmatch(
        target,
    ):

        return target

    raise ValueError(f"Invalid target: {target}")


def validate_threads(
    threads: int,
) -> int:


    return _validate_positive(
        threads,
        "Threads",
    )


def validate_timeout(
    timeout: int,
) -> int:


    return _validate_positive(
        timeout,
        "Timeout",
    )


def validate_retries(
    retries: int,
) -> int:


    if retries < 0:

        raise ValueError("Retries cannot be negative.")

    return retries


__all__ = [
    "validate_target",
    "validate_threads",
    "validate_timeout",
    "validate_retries",
]
