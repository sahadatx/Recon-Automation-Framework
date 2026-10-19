from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all, show_summary
from .manager import run


class ScreenshotPlugin(BasePlugin):


    name = "screenshots"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Capture screenshots of live web "
        "applications and generate visual "
        "reconnaissance reports."
    )

    depends_on = ("http",)

    config = {
        "async": True,
        "browser": "chromium",
        "headless": True,
        "full_page": True,
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


        export_all(
            result,
        )

        show_summary(
            result,
        )


plugin = ScreenshotPlugin()


__all__ = [
    "ScreenshotPlugin",
    "plugin",
]
