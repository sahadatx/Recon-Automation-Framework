from __future__ import annotations

from typing import Any

from .constants import AUTHOR, REPORT_TITLE, REPORT_VERSION
from .helpers import current_timestamp


def generate_report(
    analyses: dict[str, Any],
) -> dict[str, Any]:


    report = {


        "metadata": {
            "title": REPORT_TITLE,
            "version": REPORT_VERSION,
            "author": AUTHOR,
            "generated_at": current_timestamp(),
        },


        "modules": analyses,
    }

    return report


__all__ = [
    "generate_report",
]
