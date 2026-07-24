"""
Crawler Constants
"""

from __future__ import annotations

from pathlib import Path

CRAWLER_OUTPUT_DIR = Path(
    "output/crawler"
)

RESULTS_TXT = (
    CRAWLER_OUTPUT_DIR
    / "results.txt"
)

RESULTS_JSON = (
    CRAWLER_OUTPUT_DIR
    / "results.json"
)

RESULTS_CSV = (
    CRAWLER_OUTPUT_DIR
    / "results.csv"
)

SUMMARY_TXT = (
    CRAWLER_OUTPUT_DIR
    / "summary.txt"
)

__all__ = [
    "CRAWLER_OUTPUT_DIR",
    "RESULTS_TXT",
    "RESULTS_JSON",
    "RESULTS_CSV",
    "SUMMARY_TXT",
]