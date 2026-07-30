#!/usr/bin/env python3

"""
Dashboard Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .manager import run


# ==========================================================
# Dashboard Plugin
# ==========================================================


class DashboardPlugin(BasePlugin):
    """
    Dashboard Plugin.
    """

    name = "dashboard"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Generate a unified dashboard "
        "from the framework report."
    )

    depends_on = (
        "report",
    )

    config = {
        "output": True,
        "charts": True,
        "summary": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Dashboard plugin.
        """

        return run(
            context,
            *args,
            **kwargs,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = DashboardPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "DashboardPlugin",
    "plugin",
]