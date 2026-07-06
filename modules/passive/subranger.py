"""
Subranger Module

Passive subdomain enumeration using Subranger.
"""

from modules.passive.helpers import execute_source


def run_subranger(domain: str) -> list[str]:
    """
    Run Subranger.

    Args:
        domain: Target domain.

    Returns:
        List of discovered subdomains.
    """

    command = [
        "subranger",
        "-d",
        domain,
    ]

    return execute_source(
        name="Subranger",
        command=command,
        domain=domain,
    )