from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .constants import DEFAULT_ENCODING, REPORT_DIR, TIMESTAMP_FORMAT


def ensure_output_directory() -> None:


    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def save_json(
    data: dict[str, Any],
    file_path: Path,
) -> None:


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


def save_text(
    text: str,
    file_path: Path,
) -> None:


    file_path.write_text(
        text,
        encoding=DEFAULT_ENCODING,
    )


def save_markdown(
    text: str,
    file_path: Path,
) -> None:


    file_path.write_text(
        text,
        encoding=DEFAULT_ENCODING,
    )


def current_timestamp() -> str:


    return datetime.now().strftime(
        TIMESTAMP_FORMAT,
    )


def format_value(
    value: Any,
) -> str:


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


__all__ = [
    "ensure_output_directory",
    "save_json",
    "save_text",
    "save_markdown",
    "current_timestamp",
    "format_value",
]
