"""
Directory Fuzzing Constants

Output paths and
configuration.
"""

from __future__ import annotations

from pathlib import Path

# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIR = Path("output/fuzzing")


# ==========================================================
# Output Files
# ==========================================================

TXT_FILE = OUTPUT_DIR / "fuzzing.txt"

JSON_FILE = OUTPUT_DIR / "fuzzing.json"

CSV_FILE = OUTPUT_DIR / "fuzzing.csv"

SUMMARY_FILE = OUTPUT_DIR / "summary.txt"

INTERESTING_FILE = OUTPUT_DIR / "interesting.txt"


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "OUTPUT_DIR",
    "TXT_FILE",
    "JSON_FILE",
    "CSV_FILE",
    "SUMMARY_FILE",
    "INTERESTING_FILE",
]
