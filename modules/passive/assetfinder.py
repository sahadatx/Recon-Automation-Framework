"""
Assetfinder Module

Passive subdomain enumeration using Assetfinder.
"""

from modules.passive.helpers import execute_source


def run_assetfinder(domain: str) -> list[str]:
    """
    Run Assetfinder.

    Args:
        domain: Target domain.

    Returns:
        List of discovered subdomains.
    """

    command = [
        "assetfinder",
        "--subs-only",
        domain,
    ]

    return execute_source(
        name="Assetfinder",
        command=command,
    )