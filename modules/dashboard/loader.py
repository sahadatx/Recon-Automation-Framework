"""
Dashboard Loader

Load the generated report for the Dashboard module.
"""

from __future__ import annotations

import json
from typing import Any

from core.logger import warning

from .constants import REPORT_FILE

# ==========================================================
# Load Report
# ==========================================================


def load_report() -> dict[str, Any]:
    """
    Load the generated report.

    Returns:
        Parsed report data.
    """

    if not REPORT_FILE.exists():

        warning(f"Report not found: {REPORT_FILE}")

        return {}

    try:

        with REPORT_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            data: dict[str, Any] = json.load(
                file,
            )

        return data

    except (
        OSError,
        json.JSONDecodeError,
    ) as error:

        warning(f"Failed to load report: {error}")

        return {}


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "load_report",
]
