from __future__ import annotations

from pathlib import Path


DNS_OUTPUT_DIR = Path("output/dns")


RESULTS_TXT = DNS_OUTPUT_DIR / "results.txt"

RESULTS_JSON = DNS_OUTPUT_DIR / "results.json"

SUMMARY_TXT = DNS_OUTPUT_DIR / "summary.txt"

UNRESOLVED_TXT = DNS_OUTPUT_DIR / "unresolved.txt"


__all__ = [
    "DNS_OUTPUT_DIR",
    "RESULTS_TXT",
    "RESULTS_JSON",
    "SUMMARY_TXT",
    "UNRESOLVED_TXT",
]
