from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all, show_summary
from .manager import run


class JavaScriptPlugin(BasePlugin):


    name = "javascript"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Download and analyze JavaScript "
        "files to discover endpoints, "
        "URLs, source maps, secrets and "
        "interesting resources."
    )

    depends_on = ("crawler",)

    config = {
        "threads": True,
        "download": True,
        "analysis": True,
        "interesting": True,
        "secrets": True,
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


plugin = JavaScriptPlugin()


__all__ = [
    "JavaScriptPlugin",
    "plugin",
]
