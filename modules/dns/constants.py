"""
DNS Resolution Constants

Shared constants used by the DNS Resolution module.
"""

from __future__ import annotations

from pathlib import Path

# ==========================================================
# Output Directory
# ==========================================================

DNS_OUTPUT_DIR = Path("output/dns")


# ==========================================================
# Output Files
# ==========================================================

RESULTS_TXT = DNS_OUTPUT_DIR / "results.txt"

RESULTS_JSON = DNS_OUTPUT_DIR / "results.json"

SUMMARY_TXT = DNS_OUTPUT_DIR / "summary.txt"

UNRESOLVED_TXT = DNS_OUTPUT_DIR / "unresolved.txt"


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "DNS_OUTPUT_DIR",
    "RESULTS_TXT",
    "RESULTS_JSON",
    "SUMMARY_TXT",
    "UNRESOLVED_TXT",
]
