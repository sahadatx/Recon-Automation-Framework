#!/usr/bin/env python3

"""
TLS Analysis Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


# ==========================================================
# TLS Analysis Plugin
# ==========================================================


class TLSPlugin(BasePlugin):
    """
    TLS Analysis Plugin.
    """

    name = "tls"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Analyze TLS/SSL configurations, "
        "certificate validity, supported "
        "protocols, ciphers, and overall "
        "security posture."
    )

    depends_on = (
        "http",
    )

    config = {
        "certificate": True,
        "protocols": True,
        "ciphers": True,
        "risk_analysis": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the TLS Analysis plugin.
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
        Export TLS analysis reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = TLSPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "TLSPlugin",
    "plugin",
]