"""
Assetfinder Module

Passive subdomain enumeration using Assetfinder.
"""

from __future__ import annotations

from core.context import ExecutionContext
from modules.passive.helpers import execute_source


def run_assetfinder(
    context: ExecutionContext,
    domain: str,
) -> list[str]:
    """
    Run Assetfinder.

    Args:
        context:
            Shared execution context.

        domain:
            Target domain.

    Returns:
        List of discovered subdomains.
    """

    # Reserved for future use.
    _ = context

    command = [
        "assetfinder",
        "--subs-only",
        domain,
    ]

    return execute_source(
        name="Assetfinder",
        command=command,
        domain=domain,
    )


__all__ = [
    "run_assetfinder",
]
