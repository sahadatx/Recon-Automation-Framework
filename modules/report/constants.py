"""
Report Generator Constants

This module defines output directories, filenames,
and report generation settings used by the Report module.
"""

from __future__ import annotations

from pathlib import Path

# ==========================================================
# Output Directories
# ==========================================================

OUTPUT_DIR = Path("output")

REPORT_DIR = OUTPUT_DIR / "reports"

# ==========================================================
# Report Files
# ==========================================================

REPORT_JSON = REPORT_DIR / "report.json"

REPORT_TXT = REPORT_DIR / "report.txt"

REPORT_MD = REPORT_DIR / "report.md"

SUMMARY_TXT = REPORT_DIR / "summary.txt"

# ==========================================================
# Report Settings
# ==========================================================

REPORT_TITLE = "Recon Automation Framework Report"

REPORT_VERSION = "1.0"

DEFAULT_ENCODING = "utf-8"

SEPARATOR = "=" * 80

LINE = "-" * 80

# ==========================================================
# Export Formats
# ==========================================================

EXPORT_JSON = True

EXPORT_TEXT = True

EXPORT_MARKDOWN = True

EXPORT_SUMMARY = True

# ==========================================================
# Metadata
# ==========================================================

AUTHOR = "Recon Automation Framework"

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "OUTPUT_DIR",
    "REPORT_DIR",
    "REPORT_JSON",
    "REPORT_TXT",
    "REPORT_MD",
    "SUMMARY_TXT",
    "REPORT_TITLE",
    "REPORT_VERSION",
    "DEFAULT_ENCODING",
    "SEPARATOR",
    "LINE",
    "EXPORT_JSON",
    "EXPORT_TEXT",
    "EXPORT_MARKDOWN",
    "EXPORT_SUMMARY",
    "AUTHOR",
    "TIMESTAMP_FORMAT",
]
