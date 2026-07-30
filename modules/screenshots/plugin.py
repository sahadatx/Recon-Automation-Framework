#!/usr/bin/env python3

"""
Screenshot Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import (
    export_all,
    show_summary,
)
from .manager import run


# ==========================================================
# Screenshot Plugin
# ==========================================================


class ScreenshotPlugin(BasePlugin):
    """
    Screenshot Capture Plugin.
    """

    name = "screenshots"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Capture screenshots of live web "
        "applications and generate visual "
        "reconnaissance reports."
    )

    depends_on = (
        "http",
    )

    config = {
        "async": True,
        "browser": "chromium",
        "headless": True,
        "full_page": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Screenshot plugin.
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
        Export screenshot reports.
        """

        export_all(
            result,
        )

        show_summary(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = ScreenshotPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "ScreenshotPlugin",
    "plugin",
]