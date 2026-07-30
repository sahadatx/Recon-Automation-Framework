"""
Chaos Module

Passive subdomain enumeration using
ProjectDiscovery Chaos.
"""

from __future__ import annotations

import os

from core.context import (
    ExecutionContext,
)

from config.config import (
    PDCP_API_KEY,
)

from core.logger import (
    error,
)

from modules.passive.helpers import (
    execute_source,
)


def run_chaos(
    context: ExecutionContext,
    domain: str,
) -> list[str]:
    """
    Run ProjectDiscovery Chaos.

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

    if not PDCP_API_KEY:

        error(
            "PDCP_API_KEY is not configured."
        )

        return []

    env = os.environ.copy()

    env["PDCP_API_KEY"] = PDCP_API_KEY

    command = [
        "chaos",
        "-d",
        domain,
        "-silent",
    ]

    return execute_source(
        name="Chaos",
        command=command,
        domain=domain,
        env=env,
    )


__all__ = [
    "run_chaos",
]