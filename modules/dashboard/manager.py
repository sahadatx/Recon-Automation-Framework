"""
Dashboard Manager

Dashboard workflow manager.
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext

from .analyzer import analyze
from .exporter import export_all
from .loader import load_report


# ==========================================================
# Run Dashboard
# ==========================================================


def run_dashboard(
    context: ExecutionContext,
) -> dict[str, Any]:
    """
    Run the Dashboard module.

    Returns:
        Dashboard analysis.
    """

    report = load_report()

    analysis = analyze(
        report,
    )

    context.set_analysis(
        "dashboard",
        analysis,
    )

    export_all(
        analysis,
    )

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================


def run(
    context: ExecutionContext,
) -> dict[str, Any]:
    """
    Public entry point for the
    Dashboard module.
    """

    return run_dashboard(
        context,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_dashboard",
]