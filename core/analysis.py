"""
Analysis Helpers
"""

from __future__ import annotations

from typing import Any


def empty_analysis() -> dict[str, Any]:
    """
    Empty analysis object.
    """

    return {
        "results": {},
        "statistics": {},
    }


def empty_list_analysis() -> dict[str, Any]:
    """
    Empty analysis object
    for list results.
    """

    return {
        "results": [],
        "statistics": {},
    }
