#!/usr/bin/env python3

"""
JavaScript Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all, show_summary
from .manager import run

# ==========================================================
# JavaScript Plugin
# ==========================================================


class JavaScriptPlugin(BasePlugin):
    """
    JavaScript Analysis Plugin.
    """

    name = "javascript"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Download and analyze JavaScript "
        "files to discover endpoints, "
        "URLs, source maps, secrets and "
        "interesting resources."
    )

    depends_on = ("crawler",)

    config = {
        "threads": True,
        "download": True,
        "analysis": True,
        "interesting": True,
        "secrets": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the JavaScript plugin.
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
        Export JavaScript reports.
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

plugin = JavaScriptPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "JavaScriptPlugin",
    "plugin",
]
