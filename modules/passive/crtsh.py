"""
crt.sh Module

Passive subdomain enumeration using
Certificate Transparency Logs.
"""

from __future__ import annotations

from core.context import ExecutionContext
from core.logger import error, info, success, warning
from modules.passive.helpers import normalize_subdomains, retry_request


@retry_request(max_attempts=3, delay=2)
def run_crtsh(
    context: ExecutionContext,
    domain: str,
) -> list[str]:
    """
    Query crt.sh for subdomains.

    Args:
        context:
            Shared execution context.

        domain:
            Target domain.

    Returns:
        List of discovered subdomains.
    """

    info("Querying crt.sh...")

    session = context.get_http_session()

    if session is None:
        raise RuntimeError("HTTP session not initialized.")

    url = f"https://crt.sh/?q=%.{domain}&output=json"

    headers = {
        "User-Agent": "ReconAutomationFramework/2.0",
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

            error("crt.sh request timed out.")

        elif exc.__class__.__name__ == "JSONDecodeError":

            error("Invalid JSON response from crt.sh.")

        else:

            error(f"crt.sh request failed: {exc}")

        return []

    subdomains: list[str] = []

    for item in data:

        names = item.get(
            "name_value",
            "",
        )

        subdomains.extend(names.split("\n"))

    subdomains = normalize_subdomains(
        subdomains=subdomains,
        domain=domain,
    )

    if subdomains:

        success(f"crt.sh found {len(subdomains)} subdomains.")

    else:

        warning("crt.sh returned no results.")

    return subdomains


__all__ = [
    "run_crtsh",
]
