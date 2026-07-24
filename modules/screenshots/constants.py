"""
Screenshots Constants

Central configuration paths for
the Screenshot module.
"""

from __future__ import annotations

from pathlib import Path


# ==========================================================
# Output Directory
# ==========================================================

SCREENSHOT_OUTPUT_DIR = Path(
    "output/screenshots"
)


# ==========================================================
# Images Directory
# ==========================================================

IMAGES_DIR = (
    SCREENSHOT_OUTPUT_DIR
    / "images"
)


# ==========================================================
# Output Files
# ==========================================================

RESULTS_TXT = (
    SCREENSHOT_OUTPUT_DIR
    / "results.txt"
)


RESULTS_JSON = (
    SCREENSHOT_OUTPUT_DIR
    / "results.json"
)


SUMMARY_TXT = (
    SCREENSHOT_OUTPUT_DIR
    / "summary.txt"
)


# ==========================================================
# Screenshot Configuration
# ==========================================================

SCREENSHOT_WIDTH = 1280

SCREENSHOT_HEIGHT = 800


SCREENSHOT_FULL_PAGE = True


SCREENSHOT_TIMEOUT = 60000


# ==========================================================
# Browser Configuration
# ==========================================================

BROWSER_NAME = "chromium"


HEADLESS = True


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "SCREENSHOT_OUTPUT_DIR",

    "IMAGES_DIR",

    "RESULTS_TXT",

    "RESULTS_JSON",

    "SUMMARY_TXT",

    "SCREENSHOT_WIDTH",

    "SCREENSHOT_HEIGHT",

    "SCREENSHOT_FULL_PAGE",

    "SCREENSHOT_TIMEOUT",

    "BROWSER_NAME",

    "HEADLESS",

]