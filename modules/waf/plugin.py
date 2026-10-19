from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all, show_summary
from .manager import run


class WAFPlugin(BasePlugin):


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


plugin = WAFPlugin()


__all__ = [
    "WAFPlugin",
    "plugin",
]
