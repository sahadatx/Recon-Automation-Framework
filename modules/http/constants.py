"""
HTTP Probe Constants

Shared constants used by the HTTP Probe module.
"""

from __future__ import annotations

from pathlib import Path


# ==========================================================
# Output Directory
# ==========================================================

HTTP_OUTPUT_DIR = Path(
    "output/http"
)


# ==========================================================
# Output Files
# ==========================================================

RESULTS_TXT = (
    HTTP_OUTPUT_DIR
    / "results.txt"
)

RESULTS_JSON = (
    HTTP_OUTPUT_DIR
    / "results.json"
)

SUMMARY_TXT = (
    HTTP_OUTPUT_DIR
    / "summary.txt"
)

ALIVE_TXT = (
    HTTP_OUTPUT_DIR
    / "alive.txt"
)

DEAD_TXT = (
    HTTP_OUTPUT_DIR
    / "dead.txt"
)


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "HTTP_OUTPUT_DIR",
    "RESULTS_TXT",
    "RESULTS_JSON",
    "SUMMARY_TXT",
    "ALIVE_TXT",
    "DEAD_TXT",
]