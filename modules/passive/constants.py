"""
Passive Enumeration Constants

Shared constants for the Passive Enumeration module.
"""

from pathlib import Path

# ==========================================================
# Output Directory
# ==========================================================

PASSIVE_OUTPUT_DIR = Path("output/passive")

# ==========================================================
# Output Files
# ==========================================================

RESULTS_TXT = PASSIVE_OUTPUT_DIR / "results.txt"

RESULTS_JSON = PASSIVE_OUTPUT_DIR / "results.json"

SUMMARY_TXT = PASSIVE_OUTPUT_DIR / "summary.txt"

SUBDOMAINS_TXT = PASSIVE_OUTPUT_DIR / "subdomains.txt"

RAW_RESULTS_TXT = PASSIVE_OUTPUT_DIR / "raw_results.txt"