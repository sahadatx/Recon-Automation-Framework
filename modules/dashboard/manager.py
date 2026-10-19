from __future__ import annotations

from typing import Any

from core.context import ExecutionContext

from .analyzer import analyze
from .exporter import export_all
from .loader import load_report


def run_dashboard(
    context: ExecutionContext,
) -> dict[str, Any]:


    report = load_report()


    analysis = analyze(
        report,
    )


    export_all(
        analysis,
    )


    context.set_analysis(
        "dashboard",
        analysis,
    )


    return analysis


def run(
    context: ExecutionContext,
) -> dict[str, Any]:


    return run_dashboard(
        context,
    )


__all__ = [
    "run",
    "run_dashboard",
]
