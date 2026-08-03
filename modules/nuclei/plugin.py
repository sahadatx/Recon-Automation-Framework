#!/usr/bin/env python3

"""
Nuclei Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run

# ==========================================================
# Nuclei Plugin
# ==========================================================


class NucleiPlugin(BasePlugin):
    """
    Nuclei Vulnerability Scanner Plugin.
    """

    name = "nuclei"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Perform vulnerability scanning "
        "using Nuclei templates and "
        "generate consolidated findings."
    )

    depends_on = ("http",)

    config = {
        "threads": True,
        "templates": "default",
        "output": True,
        "cleanup": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Nuclei plugin.
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
        Export Nuclei reports.
        """

        export_all(
            result,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = NucleiPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "NucleiPlugin",
    "plugin",
]
