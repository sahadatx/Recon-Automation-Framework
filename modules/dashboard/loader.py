from __future__ import annotations

import json
from typing import Any

from core.logger import warning

from .constants import REPORT_FILE


def load_report() -> dict[str, Any]:


    if not REPORT_FILE.exists():

        warning(f"Report not found: {REPORT_FILE}")

        return {}

    try:

        with REPORT_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            data: dict[str, Any] = json.load(
                file,
            )

        return data

    except (
        OSError,
        json.JSONDecodeError,
    ) as error:

        warning(f"Failed to load report: {error}")

        return {}


__all__ = [
    "load_report",
]
