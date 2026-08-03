"""
Findomain Module

Passive subdomain enumeration using Findomain.
"""

from __future__ import annotations

from core.context import (
    ExecutionContext,
)

from modules.passive.helpers import (
    execute_source,
)


def run_findomain(
    context: ExecutionContext,
    domain: str,
) -> list[str]:
    """
    Run Findomain.

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


__all__ = [
    "run_findomain",
]
