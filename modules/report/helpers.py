"""
Report Helper Functions

Reusable helper functions for the Report Generator module.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .constants import (
    DEFAULT_ENCODING,
    REPORT_DIR,
    TIMESTAMP_FORMAT,
)

# ==========================================================
# Directory
# ==========================================================


def ensure_output_directory() -> None:
    """
    Create the report output directory if it does not exist.
    """

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# JSON
# ==========================================================


def save_json(
    data: dict[str, Any],
    file_path: Path,
) -> None:
    """
    Save a dictionary as JSON.
    """

    with file_path.open(
        "w",
        encoding=DEFAULT_ENCODING,
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


# ==========================================================
# Text
# ==========================================================


def save_text(
    text: str,
    file_path: Path,
) -> None:
    """
    Save plain text.
    """

    file_path.write_text(
        text,
        encoding=DEFAULT_ENCODING,
    )


# ==========================================================
# Markdown
# ==========================================================


def save_markdown(
    text: str,
    file_path: Path,
) -> None:
    """
    Save Markdown content.
    """

    file_path.write_text(
        text,
        encoding=DEFAULT_ENCODING,
    )


# ==========================================================
# Time
# ==========================================================


def current_timestamp() -> str:
    """
    Return the current timestamp.
    """

    return datetime.now().strftime(
        TIMESTAMP_FORMAT,
    )


# ==========================================================
# Formatting
# ==========================================================


def format_value(
    value: Any,
) -> str:
    """
    Convert any value into a readable string.
    """

    if value is None:
        return "-"

    if isinstance(
        value,
        bool,
    ):
        return "Yes" if value else "No"

    if isinstance(
        value,
        (list, tuple, set),
    ):
        return ", ".join(
            map(
                str,
                value,
            )
        )

    if isinstance(
        value,
        dict,
    ):
        return json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
        )

    return str(value)


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "ensure_output_directory",
    "save_json",
    "save_text",
    "save_markdown",
    "current_timestamp",
    "format_value",
]