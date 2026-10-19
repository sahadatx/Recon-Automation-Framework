from __future__ import annotations

from typing import Any

from core.context import ExecutionContext

from .generator import generate_report
from .statistics import generate_statistics


def execute(
    context: ExecutionContext,
    analyses: dict[str, Any],
) -> dict[str, Any]:


    report = generate_report(
        analyses,
    )


    statistics = generate_statistics(
        report,
    )

    report["statistics"] = statistics


    context.set_analysis(
        "report",
        report,
    )

    return report


def run(
    context: ExecutionContext,
    analyses: dict[str, Any],
) -> dict[str, Any]:


    return execute(
        context,
        analyses,
    )


__all__ = [
    "run",
    "execute",
]
