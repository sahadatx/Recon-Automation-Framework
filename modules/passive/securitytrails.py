"""
SecurityTrails Module

Passive subdomain enumeration using
SecurityTrails API.
"""

from __future__ import annotations

import requests

from config.config import SECURITYTRAILS_API_KEY
from core.context import ExecutionContext
from core.logger import error, info, success, warning
from modules.passive.helpers import normalize_subdomains, retry_request


@retry_request(max_attempts=3, delay=2)
def run_securitytrails(
    context: ExecutionContext,
    domain: str,
) -> list[str]:
    """
    Query SecurityTrails API.

    Args:
        context:
            Shared execution context.

        domain:
            Target domain.

    Returns:
        Normalized list of discovered
        subdomains.
    """

    info("Running SecurityTrails...")

    if not SECURITYTRAILS_API_KEY:

        warning("SecurityTrails API key not configured.")

        return []

    session = context.get_http_session()

    if session is None:

        raise RuntimeError("HTTP session not initialized.")

    url = f"https://api.securitytrails.com/v1/" f"domain/{domain}/subdomains"

    headers = {
        "APIKEY": SECURITYTRAILS_API_KEY,
    }

    try:

        response = session.get(
            url,
            headers=headers,
            timeout=30,
        )

    except (
        requests.Timeout,
        requests.ConnectionError,
    ):

        warning("SecurityTrails connection failed. " "Retrying...")

        raise

    except requests.RequestException as exc:

        error(f"SecurityTrails request failed: {exc}")

        return []

    if response.status_code == 401:

        error("Invalid SecurityTrails API key.")

        return []

    if response.status_code == 403:

        error("SecurityTrails access denied.")

        return []

    if response.status_code == 404:

        warning(f"No SecurityTrails data for " f"{domain}.")

        return []

    if response.status_code == 429:

        retry_after = response.headers.get("Retry-After")

        if retry_after:

            warning(
                "SecurityTrails rate limit "
                f"exceeded. Retry after "
                f"{retry_after} seconds."
            )

        else:

            warning("SecurityTrails rate limit " "exceeded.")

        return []

    if response.status_code >= 500:

        warning(
            f"SecurityTrails server error " f"({response.status_code}). " "Retrying..."
        )

        raise requests.HTTPError(f"HTTP {response.status_code}")

    try:

        data = response.json()

    except ValueError:

        error("Invalid JSON response from " "SecurityTrails.")

        return []

    subdomains = normalize_subdomains(
        [
            f"{sub}.{domain}"
            for sub in data.get(
                "subdomains",
                [],
            )
        ],
        domain,
    )

    if subdomains:

        success(f"SecurityTrails found " f"{len(subdomains)} subdomains.")

    else:

        warning("SecurityTrails returned " "no results.")

    return subdomains


__all__ = [
    "run_securitytrails",
]
