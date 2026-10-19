from __future__ import annotations

from core.context import ExecutionContext
from modules.passive.helpers import execute_source


def run_subranger(
    context: ExecutionContext,
    domain: str,
) -> list[str]:


    _ = context

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


__all__ = [
    "run_subranger",
]
