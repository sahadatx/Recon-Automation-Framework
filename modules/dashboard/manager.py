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
# Public Exports
# ==========================================================

__all__ = [
    "run_dashboard",
]