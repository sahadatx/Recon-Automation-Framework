#!/usr/bin/env python3

"""
DNS Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run

# ==========================================================
# DNS Plugin
# ==========================================================


class DNSPlugin(BasePlugin):
    """
    DNS Enumeration Plugin.
    """

    name = "dns"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Perform DNS enumeration and " "collect DNS records for " "target domains."
    )

    depends_on = ("passive",)

    config = {
        "output": True,
        "threads": True,
        "resolver": "system",
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the DNS plugin.
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
        Export DNS reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = DNSPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "DNSPlugin",
    "plugin",
]
