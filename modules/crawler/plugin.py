#!/usr/bin/env python3

"""
Crawler Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


# ==========================================================
# Crawler Plugin
# ==========================================================


class CrawlerPlugin(BasePlugin):
    """
    Web Crawler Plugin.
    """

    name = "crawler"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Crawl web applications and "
        "discover URLs, endpoints, "
        "parameters and assets."
    )

    depends_on = (
        "http",
    )

    config = {
        "http": True,
        "threads": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the crawler plugin.
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
        Export crawler reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = CrawlerPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "CrawlerPlugin",
    "plugin",
]