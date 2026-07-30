"""
SecurityTrails Module

Passive subdomain enumeration using
SecurityTrails API.
"""

from __future__ import annotations

from core.context import ExecutionContext

from config.config import (
    SECURITYTRAILS_API_KEY,
)

from core.logger import (
    error,
    info,
    success,
    warning,
)

from modules.passive.helpers import (
    normalize_subdomains,
    retry_request,
)


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
        List of discovered subdomains.
    """

    info("Running SecurityTrails...")

    if not SECURITYTRAILS_API_KEY:

        warning(
            "SecurityTrails API key not configured."
        )

        return []

    session = context.get_http_session()

    if session is None:

        raise RuntimeError(
            "HTTP session not initialized."
        )

    url = (
        f"https://api.securitytrails.com/v1/"
        f"domain/{domain}/subdomains"
    )

    headers = {
        "APIKEY": SECURITYTRAILS_API_KEY,
    }

    try:

        response = session.get(
            url,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

    except Exception as exc:

        if exc.__class__.__name__ == "Timeout":

            error(
                "SecurityTrails request timed out."
            )

        elif exc.__class__.__name__ == "JSONDecodeError":

            error(
                "Invalid JSON response from SecurityTrails."
            )

        else:

            error(
                f"SecurityTrails request failed: {exc}"
            )

        return []

    subdomains: list[str] = []

    for sub in data.get(
        "subdomains",
        [],
    ):

        subdomains.append(
            f"{sub}.{domain}"
        )

    subdomains = normalize_subdomains(
        subdomains=subdomains,
        domain=domain,
    )

    if subdomains:

        success(
            f"SecurityTrails found {len(subdomains)} subdomains."
        )

    else:

        warning(
            "SecurityTrails returned no results."
        )

    return subdomains


__all__ = [
    "run_securitytrails",
]