#!/usr/bin/env python3

"""
Subdomain Takeover Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


# ==========================================================
# Subdomain Takeover Plugin
# ==========================================================


class TakeoverPlugin(BasePlugin):
    """
    Subdomain Takeover Detection Plugin.
    """

    name = "takeover"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Detect potential subdomain "
        "takeover vulnerabilities using "
        "DNS, CNAME, HTTP fingerprint "
        "and provider-specific analysis."
    )

    depends_on = (
        "http",
        "dns",
    )

    config = {
        "threads": True,
        "http": True,
        "dns": True,
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
        Execute the Subdomain Takeover plugin.
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
        Export takeover reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = TakeoverPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "TakeoverPlugin",
    "plugin",
]