#!/usr/bin/env python3

"""
Directory Fuzzing Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


# ==========================================================
# Directory Fuzzing Plugin
# ==========================================================


class FuzzingPlugin(BasePlugin):
    """
    Directory Fuzzing Plugin.
    """

    name = "fuzzing"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Perform directory and file "
        "fuzzing to discover hidden "
        "paths and interesting content."
    )

    depends_on = (
        "http",
    )

    config = {
        "threads": True,
        "output": True,
        "cleanup": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Directory Fuzzing plugin.
        """

        return run(
            context,
            *args,
            **kwargs,
        )

    def after_export(
        self,
        result: dict[str, Any],
    ) -> None:
        """
        Export Directory Fuzzing reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = FuzzingPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "FuzzingPlugin",
    "plugin",
]