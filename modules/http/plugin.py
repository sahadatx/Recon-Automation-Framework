#!/usr/bin/env python3

"""
HTTP Probe Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run

# ==========================================================
# HTTP Probe Plugin
# ==========================================================


class HTTPPlugin(BasePlugin):
    """
    HTTP Probe Plugin.
    """

    name = "http"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Probe HTTP and HTTPS services "
        "to identify live hosts and "
        "collect response metadata."
    )

    depends_on = ("dns",)

    config = {
        "threads": True,
        "output": True,
        "session": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the HTTP Probe plugin.
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
        Export HTTP Probe reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = HTTPPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "HTTPPlugin",
    "plugin",
]
