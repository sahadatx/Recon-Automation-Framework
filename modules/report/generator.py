"""
Report Generator

Build the final report from all module results.
"""

from __future__ import annotations

from typing import Any

from .constants import (
    AUTHOR,
    REPORT_TITLE,
    REPORT_VERSION,
)
from .helpers import (
    current_timestamp,
)


# ==========================================================
# Report Generator
# ==========================================================

def generate_report(
    analyses: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate the master report.

    Args:
        analyses:
            Analysis results from all modules.

    Returns:
        Master report.
    """

    report = {

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        "metadata": {

            "title": REPORT_TITLE,

            "version": REPORT_VERSION,

            "author": AUTHOR,

            "generated_at": current_timestamp(),

        },

        # --------------------------------------------------
        # Module Results
        # --------------------------------------------------

        "modules": analyses,

    }

    return report


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "generate_report",
]