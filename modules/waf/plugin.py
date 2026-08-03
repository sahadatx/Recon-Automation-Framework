#!/usr/bin/env python3

"""
WAF Detection Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all, show_summary
from .manager import run

# ==========================================================
# WAF Detection Plugin
# ==========================================================


class WAFPlugin(BasePlugin):
    """
    WAF Detection Plugin.
    """

    name = "waf"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Detect Web Application Firewalls "
        "using HTTP fingerprinting, response "
        "analysis, and vendor-specific "
        "signatures."
    )

    depends_on = ("http",)

    config = {
        "fingerprints": True,
        "http": True,
        "filtering": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the WAF Detection plugin.
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
        Export WAF Detection reports.
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

plugin = WAFPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "WAFPlugin",
    "plugin",
]
