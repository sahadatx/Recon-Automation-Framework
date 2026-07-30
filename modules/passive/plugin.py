#!/usr/bin/env python3

"""
Passive Enumeration Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


# ==========================================================
# Passive Enumeration Plugin
# ==========================================================


class PassivePlugin(BasePlugin):
    """
    Passive Enumeration Plugin.
    """

    name = "passive"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Collect subdomains from multiple "
        "passive intelligence sources and "
        "merge, normalize, and analyze the "
        "results."
    )

    depends_on = ()

    config = {
        "threads": True,
        "retry": True,
        "merge": True,
        "normalize": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Passive Enumeration plugin.
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
        Export Passive Enumeration reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = PassivePlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "PassivePlugin",
    "plugin",
]