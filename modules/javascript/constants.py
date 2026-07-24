"""
JavaScript Constants
"""

from __future__ import annotations

from pathlib import Path


JAVASCRIPT_OUTPUT_DIR = Path(
    "output/javascript"
)

RESULTS_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "results.txt"
)

RESULTS_JSON = (
    JAVASCRIPT_OUTPUT_DIR
    / "results.json"
)

RESULTS_CSV = (
    JAVASCRIPT_OUTPUT_DIR
    / "results.csv"
)

SUMMARY_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "summary.txt"
)

JAVASCRIPT_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "javascript.txt"
)

URLS_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "urls.txt"
)

ENDPOINTS_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "endpoints.txt"
)

SOURCE_MAPS_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "source_maps.txt"
)

INTERESTING_FILES_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "interesting_files.txt"
)

INTERESTING_DIRECTORIES_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "interesting_directories.txt"
)

SECRETS_TXT = (
    JAVASCRIPT_OUTPUT_DIR
    / "secrets.txt"
)

FILES_DIR = (
    JAVASCRIPT_OUTPUT_DIR
    / "files"
)

__all__ = [
    "JAVASCRIPT_OUTPUT_DIR",
    "RESULTS_TXT",
    "RESULTS_JSON",
    "RESULTS_CSV",
    "SUMMARY_TXT",
    "JAVASCRIPT_TXT",
    "URLS_TXT",
    "ENDPOINTS_TXT",
    "SOURCE_MAPS_TXT",
    "INTERESTING_FILES_TXT",
    "INTERESTING_DIRECTORIES_TXT",
    "SECRETS_TXT",
    "FILES_DIR",
]