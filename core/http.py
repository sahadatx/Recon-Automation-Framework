from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter

from config.config import HTTP_USER_AGENT, HTTP_VERIFY_SSL


def create_http_session() -> requests.Session:


    session = requests.Session()


    session.verify = HTTP_VERIFY_SSL


    session.headers.update(
        {
            "User-Agent": HTTP_USER_AGENT,
        }
    )


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


__all__ = [
    "create_http_session",
]
