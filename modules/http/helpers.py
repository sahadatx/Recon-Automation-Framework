from __future__ import annotations

from config.config import HTTP_TIMEOUT, VERBOSE
from core.logger import debug


def show_probe(
    url: str,
) -> None:


    if not VERBOSE:

        return

    debug(f"Probing {url}")


def request_timeout() -> int | float:


    return HTTP_TIMEOUT


__all__ = [
    "request_timeout",
    "show_probe",
]
