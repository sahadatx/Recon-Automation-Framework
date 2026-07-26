"""
Dashboard Manager

Dashboard workflow manager.
"""

from __future__ import annotations

from typing import Any

from .analyzer import analyze
from .exporter import export_all
from .loader import load_report


# ==========================================================
# Run Dashboard
# ==========================================================

def run_dashboard() -> dict[str, Any]:
    """
    Run the Dashboard module.

    Returns:
        Dashboard analysis.
    """

    report = load_report()

    analysis = analyze(
        report,
    )

    export_all(
        analysis,
    )

    return analysis


# ==========================================================
# Public Entry Point
# ==========================================================

def run() -> dict[str, Any]:
    """
    Public entry point for the Dashboard module.
    """

    return run_dashboard()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run",
    "run_dashboard",
]