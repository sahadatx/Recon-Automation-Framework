from __future__ import annotations

from core.context import ExecutionContext
from modules.passive.helpers import execute_source


def run_assetfinder(
    context: ExecutionContext,
    domain: str,
) -> list[str]:


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
