#!/usr/bin/env python3

"""
Email Security Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run

# ==========================================================
# Email Security Plugin
# ==========================================================


class EmailSecurityPlugin(BasePlugin):
    """
    Email Security Plugin.
    """

    name = "email"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Analyze email security "
        "configuration including SPF, "
        "DKIM, DMARC, DNSSEC, BIMI, "
        "MTA-STS and TLS-RPT."
    )

    depends_on = ("dns",)

    config = {
        "threads": False,
        "output": True,
        "cache": False,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Email Security plugin.
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
        Export Email Security reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = EmailSecurityPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "EmailSecurityPlugin",
    "plugin",
]
