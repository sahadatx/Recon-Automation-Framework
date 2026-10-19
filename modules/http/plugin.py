from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class HTTPPlugin(BasePlugin):


    name = "http"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Probe HTTP and HTTPS services "
        "to identify live hosts and "
        "collect response metadata."
    )

    depends_on = ("dns",)

    config = {
        "threads": True,
        "output": True,
        "session": True,
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


plugin = HTTPPlugin()


__all__ = [
    "HTTPPlugin",
    "plugin",
]
