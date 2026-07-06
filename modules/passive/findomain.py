"""
Findomain Module

Passive subdomain enumeration using Findomain.
"""

from modules.passive.helpers import execute_source


def run_findomain(domain: str) -> list[str]:
    """
    Run Findomain.

    Args:
        domain: Target domain.

    Returns:
        List of discovered subdomains.
    """

    command = [
        "findomain",
        "-t",
        domain,
        "-q",
    ]

    return execute_source(
        name="Findomain",
        command=command,
        domain=domain,
    )