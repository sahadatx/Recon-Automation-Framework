#!/usr/bin/env python3

"""
Technology Detection Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run

# ==========================================================
# Technology Detection Plugin
# ==========================================================


class TechnologyPlugin(BasePlugin):
    """
    Technology Detection Plugin.
    """

    name = "tech"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Identify web technologies and "
        "security headers used by "
        "discovered web applications."
    )

    depends_on = ("http",)

    config = {
        "threads": True,
        "headers": True,
        "fingerprints": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Technology Detection plugin.
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
        Export Technology Detection reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = TechnologyPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "TechnologyPlugin",
    "plugin",
]
