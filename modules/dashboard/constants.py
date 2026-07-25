"""
Dashboard Constants

Constants used by the Dashboard module.
"""

from __future__ import annotations

from pathlib import Path

from modules.report.constants import REPORT_JSON


# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIR = Path(
    "output/dashboard"
)


# ==========================================================
# Output Files
# ==========================================================

DASHBOARD_JSON = (
    OUTPUT_DIR / "dashboard.json"
)

DASHBOARD_TXT = (
    OUTPUT_DIR / "dashboard.txt"
)

SUMMARY_FILE = (
    OUTPUT_DIR / "summary.txt"
)


# ==========================================================
# Input Report
# ==========================================================

REPORT_FILE = REPORT_JSON


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "OUTPUT_DIR",
    "DASHBOARD_JSON",
    "DASHBOARD_TXT",
    "SUMMARY_FILE",
    "REPORT_FILE",
]