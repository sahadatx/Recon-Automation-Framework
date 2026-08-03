#!/usr/bin/env python3

"""
Virtual Host Discovery Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all, show_summary
from .manager import run

# ==========================================================
# Virtual Host Discovery Plugin
# ==========================================================


class VHostPlugin(BasePlugin):
    """
    Virtual Host Discovery Plugin.
    """

    name = "vhost"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Discover virtual hosts using "
        "FFUF-based enumeration and "
        "identify interesting responses."
    )

    depends_on = ("http",)

    config = {
        "threads": True,
        "ffuf": True,
        "filters": True,
        "interesting": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Virtual Host Discovery plugin.
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
        Export Virtual Host Discovery reports.
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

plugin = VHostPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "VHostPlugin",
    "plugin",
]
