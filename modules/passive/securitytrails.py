"""
SecurityTrails Module

Passive subdomain enumeration using
SecurityTrails API.
"""

import requests

from config.config import (
    SECURITYTRAILS_API_KEY,
)

from core.logger import (
    info,
    success,
    warning,
    error,
)

from modules.passive.helpers import (
    retry_request,
    normalize_subdomains,
)


@retry_request(max_attempts=3, delay=2)
def run_securitytrails(
    domain: str,
) -> list[str]:
    """
    Query SecurityTrails API.

    Args:
        domain: Target domain.

    Returns:
        List of discovered subdomains.
    """

    info("Running SecurityTrails...")

    if not SECURITYTRAILS_API_KEY:

        warning(
            "SecurityTrails API key not configured."
        )

        return []

    url = (
        f"https://api.securitytrails.com/v1/"
        f"domain/{domain}/subdomains"
    )

    headers = {
        "APIKEY": SECURITYTRAILS_API_KEY,
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:

        error(
            f"SecurityTrails request failed: {e}"
        )

        return []

    subdomains = []

    for sub in data.get("subdomains", []):

        subdomains.append(
            f"{sub}.{domain}"
        )

    subdomains = normalize_subdomains(
        subdomains
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