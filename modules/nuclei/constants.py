"""
Nuclei Constants
"""

from __future__ import annotations

from pathlib import Path

# ==========================================================
# Module
# ==========================================================

MODULE_NAME = "nuclei"

# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIR = Path("output") / MODULE_NAME

JSON_FILE = OUTPUT_DIR / f"{MODULE_NAME}.json"
TXT_FILE = OUTPUT_DIR / f"{MODULE_NAME}.txt"
CSV_FILE = OUTPUT_DIR / f"{MODULE_NAME}.csv"
MARKDOWN_FILE = OUTPUT_DIR / f"{MODULE_NAME}.md"

SUMMARY_FILE = OUTPUT_DIR / "summary.txt"

HIGH_FILE = OUTPUT_DIR / "high.txt"
CRITICAL_FILE = OUTPUT_DIR / "critical.txt"

# ==========================================================
# Risk Levels
# ==========================================================

CRITICAL = "critical"
HIGH = "high"
MEDIUM = "medium"
LOW = "low"
INFO = "info"
UNKNOWN = "unknown"

RISK_LEVELS = (
    CRITICAL,
    HIGH,
    MEDIUM,
    LOW,
    INFO,
    UNKNOWN,
)

# ==========================================================
# Severity Order
# ==========================================================

SEVERITY_ORDER = {
    INFO: 0,
    LOW: 1,
    MEDIUM: 2,
    HIGH: 3,
    CRITICAL: 4,
    UNKNOWN: 5,
}

# ==========================================================
# Exports
# ==========================================================

__all__ = [
    "MODULE_NAME",
    "OUTPUT_DIR",
    "JSON_FILE",
    "TXT_FILE",
    "CSV_FILE",
    "MARKDOWN_FILE",
    "SUMMARY_FILE",
    "HIGH_FILE",
    "CRITICAL_FILE",
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFO",
    "UNKNOWN",
    "RISK_LEVELS",
    "SEVERITY_ORDER",
]