#!/usr/bin/env python3

"""
Dashboard Manager

Coordinate dashboard analysis and export.
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
    Execute the complete dashboard workflow.

        Load Report
             ↓
        Analyze Report
             ↓
        Export Dashboard
             ↓
        Store Context
             ↓
        Return Analysis
    """

    # ------------------------------------------------------
    # Load Report
    # ------------------------------------------------------

    report = load_report()

    # ------------------------------------------------------
    # Analyze Report
    # ------------------------------------------------------

    analysis = analyze(
        report,
    )

    # ------------------------------------------------------
    # Export Dashboard Files
    # ------------------------------------------------------

    export_all(
        analysis,
    )

    # ------------------------------------------------------
    # Store Analysis
    # ------------------------------------------------------

    context.set_analysis(
        "dashboard",
        analysis,
    )

    # ------------------------------------------------------
    # Return Analysis
    # ------------------------------------------------------

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================

def run(
    context: ExecutionContext,
) -> dict[str, Any]:
    """
    Execute the Dashboard module.
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