#!/usr/bin/env python3

"""
Dashboard Manager

Coordinate dashboard analysis.
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext

from .analyzer import analyze
from .loader import load_report


# ==========================================================
# Run Dashboard
# ==========================================================


def run_dashboard(
    context: ExecutionContext,
) -> dict[str, Any]:
    """
    Execute the complete dashboard workflow.

        Load Report
             ↓
        Analyze
             ↓
        Store Context
             ↓
        Return Analysis
    """

    report = load_report()

    analysis = analyze(
        report,
    )

    context.set_analysis(
        "dashboard",
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