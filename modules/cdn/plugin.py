#!/usr/bin/env python3

"""
CDN Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


# ==========================================================
# CDN Plugin
# ==========================================================


class CDNPlugin(BasePlugin):
    """
    CDN Detection Plugin.
    """

    name = "cdn"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Detect Content Delivery Networks "
        "using HTTP, DNS, CNAME and IP "
        "fingerprints."
    )

    depends_on = (
        "http",
    )

    config = {
        "http": True,
        "threads": False,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the CDN plugin.
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
        Export CDN reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = CDNPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "CDNPlugin",
    "plugin",
]