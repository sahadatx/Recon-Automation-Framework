#!/usr/bin/env python3

"""
Report Generator Plugin
"""

from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import (
    export_all,
    show_summary,
)
from .statistics import generate_statistics
from .manager import run

# ==========================================================
# Report Generator Plugin
# ==========================================================


class ReportPlugin(BasePlugin):
    """
    Report Generator Plugin.
    """

    name = "report"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Generate the final reconnaissance "
        "report from all module analyses "
        "and export it in multiple formats."
    )

    depends_on = ("dashboard",)

    config = {
        "json": True,
        "text": True,
        "markdown": True,
        "summary": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the Report Generator plugin.
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
        Export the final report.
        """

        statistics = result.get(
            "statistics",
            generate_statistics(result),
        )

        export_all(
            report=result,
            statistics=statistics,
        )

        show_summary(
            statistics,
        )


# ==========================================================
# Plugin Instance
# ==========================================================

plugin = ReportPlugin()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "ReportPlugin",
    "plugin",
]
