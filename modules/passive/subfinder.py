"""
Subfinder Module

Passive subdomain enumeration using ProjectDiscovery Subfinder.
"""

from modules.passive.helpers import execute_source


def run_subfinder(domain: str) -> list[str]:
    """
    Run Subfinder.

    Args:
        domain: Target domain.

    Returns:
        List of discovered subdomains.
    """

    command = [
        "subfinder",
        "-silent",
        "-d",
        domain,
    ]

    return execute_source(
        name="Subfinder",
        command=command,
    )