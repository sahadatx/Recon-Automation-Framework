"""
crt.sh Module

Passive subdomain enumeration using
Certificate Transparency Logs.
"""

import requests

from core.logger import (
    info,
    success,
    warning,
    error,
)

from modules.passive.helpers import (
    normalize_subdomains,
    retry_request,
)


@retry_request(max_attempts=3, delay=2)
def run_crtsh(domain: str) -> list[str]:
    """
    Query crt.sh for subdomains.

    Args:
        domain: Target domain.

    Returns:
        List of discovered subdomains.
    """

    info("Querying crt.sh...")

    url = (
        f"https://crt.sh/?q=%.{domain}&output=json"
    )

    headers = {
        "User-Agent": "ReconAutomationFramework/2.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.Timeout:

        error("crt.sh request timed out.")

        return []

    except requests.exceptions.RequestException as e:

        error(f"crt.sh request failed: {e}")

        return []

    except ValueError:

        error("Invalid JSON response from crt.sh.")

        return []

    subdomains = []

    for item in data:

        names = item.get(
            "name_value",
            ""
        )

        subdomains.extend(
            names.split("\n")
        )

    subdomains = normalize_subdomains(
        subdomains
    )

    if subdomains:

        success(
            f"crt.sh found {len(subdomains)} subdomains."
        )

    else:

        warning(
            "crt.sh returned no results."
        )

    return subdomains