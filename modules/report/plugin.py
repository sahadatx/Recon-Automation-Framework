from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all, show_summary
from .manager import run
from .statistics import generate_statistics


class ReportPlugin(BasePlugin):


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


        return run(
            context,
            *args,
            **kwargs,
        )

    def after_export(
        self,
        result: dict[str, Any],
    ) -> None:


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


plugin = ReportPlugin()


__all__ = [
    "ReportPlugin",
    "plugin",
]
