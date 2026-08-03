"""
Technology Detection Constants
"""

from __future__ import annotations

from pathlib import Path

# ==========================================================
# Output Directory
# ==========================================================

TECH_OUTPUT_DIR = Path("output/technology")


# ==========================================================
# Output Files
# ==========================================================

RESULTS_TXT = TECH_OUTPUT_DIR / "results.txt"

RESULTS_JSON = TECH_OUTPUT_DIR / "results.json"

RESULTS_CSV = TECH_OUTPUT_DIR / "results.csv"

SUMMARY_TXT = TECH_OUTPUT_DIR / "summary.txt"

TECHNOLOGIES_TXT = TECH_OUTPUT_DIR / "technologies.txt"


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "TECH_OUTPUT_DIR",
    "RESULTS_TXT",
    "RESULTS_JSON",
    "RESULTS_CSV",
    "SUMMARY_TXT",
    "TECHNOLOGIES_TXT",
]
