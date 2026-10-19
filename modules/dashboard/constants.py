from __future__ import annotations

from pathlib import Path

from modules.report.constants import REPORT_JSON


OUTPUT_DIR = Path("output")

DASHBOARD_DIR = OUTPUT_DIR / "dashboard"


DASHBOARD_HTML = DASHBOARD_DIR / "index.html"

DASHBOARD_JSON = DASHBOARD_DIR / "dashboard.json"

DASHBOARD_TXT = DASHBOARD_DIR / "dashboard.txt"

DASHBOARD_SUMMARY = DASHBOARD_DIR / "summary.txt"


REPORT_FILE = REPORT_JSON


__all__ = (
    "OUTPUT_DIR",
    "DASHBOARD_DIR",
    "DASHBOARD_HTML",
    "DASHBOARD_JSON",
    "DASHBOARD_TXT",
    "DASHBOARD_SUMMARY",
    "REPORT_FILE",
)
