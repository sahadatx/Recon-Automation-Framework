from __future__ import annotations

from core.context import ExecutionContext
from modules.passive.helpers import execute_source


def run_subfinder(
    context: ExecutionContext,
    domain: str,
) -> list[str]:


    _ = context

    command = [
        "subfinder",
        "-silent",
        "-d",
        domain,
    ]

    return execute_source(
        name="Subfinder",
        command=command,
        domain=domain,
    )


__all__ = [
    "run_subfinder",
]
